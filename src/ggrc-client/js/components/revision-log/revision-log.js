/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../tree_pagination/tree_pagination';
import '../paginate/paginate';
import './revision-page';
import RefreshQueue from '../../models/refresh_queue';
import template from './revision-log.stache';
import tracker from '../../tracker';
import Revision from '../../models/service-models/revision';
import Stub from '../../models/stub';
import {reify as reifyUtil, isReifiable} from '../../plugins/utils/reify-utils';

import {
  buildParam,
  batchRequests,
} from '../../plugins/utils/query-api-utils';
import QueryParser from '../../generated/ggrc_filter_query_parser';
import Pagination from '../base-objects/pagination';

export default can.Component.extend({
  tag: 'revision-log',
  template,
  leakScope: true,
  viewModel: {
    define: {
      showFilter: {
        get() {
          return (this.attr('review.status') === 'Unreviewed') &&
            !!this.attr('review.last_reviewed_by');
        },
      },
      pageInfo: {
        value: function () {
          return new Pagination({
            pageSizeSelect: [10, 25, 50],
            pageSize: 10,
          });
        },
      },
      showLastReviewUpdates: {
        get() {
          const review = this.attr('review');

          return (review && review.getShowLastReviewUpdates) ?
            review.getShowLastReviewUpdates() :
            false;
        },
      },
    },
    instance: null,
    review: null,
    isLoading: false,
    revisions: null,
    getOriginRevision() {
      const instance = this.attr('instance');
      const filter = QueryParser.parse(
        `resource_type = ${instance.type} AND
         resource_id = ${instance.id}`);
      const page = {
        current: 1,
        pageSize: 2,
        sort: [{
          direction: 'desc',
          key: 'created_at',
        }],
      };
      let params = buildParam(
        'Revision',
        page,
        null,
        null,
        filter
      );

      return batchRequests(params).then((data) => {
        return this.makeRevisionModels(data.Revision);
      });
    },
    getAllRevisions() {
      const instance = this.attr('instance');
      const filter = QueryParser.parse(
        `resource_type = ${instance.type} AND
         resource_id = ${instance.id} OR
         source_type = ${instance.type} AND
         source_id = ${instance.id} OR
         destination_type = ${instance.type} AND
         destination_id = ${instance.id}`);
      let pageInfo = this.attr('pageInfo');
      const page = {
        current: pageInfo.current,
        pageSize: pageInfo.pageSize,
        sort: [{
          direction: 'desc',
          key: 'created_at',
        }],
      };
      let params = buildParam(
        'Revision',
        page,
        null,
        null,
        filter
      );

      return batchRequests(params).then((data) => {
        data = data.Revision;
        const total = data.total;
        this.attr('pageInfo.total', total);

        return this.makeRevisionModels(data);
      });
    },
    getAfterReviewRevisions() {
      const instance = this.attr('instance');
      const reviewDate = moment(this.attr('review.last_reviewed_at'))
        .format('YYYY-MM-DD HH:mm:ss');
      const filter = QueryParser.parse(
        `resource_type = ${instance.type} AND
         resource_id = ${instance.id} AND
         created_at >= ${reviewDate} OR
         source_type = ${instance.type} AND
         source_id = ${instance.id} AND
         created_at >= ${reviewDate} OR
         destination_type = ${instance.type} AND
         destination_id = ${instance.id} AND
         created_at >= ${reviewDate}`);
      let pageInfo = this.attr('pageInfo');
      const page = {
        current: pageInfo.current,
        pageSize: pageInfo.pageSize,
        sort: [{
          direction: 'desc',
          key: 'created_at',
        }],
      };
      let params = buildParam(
        'Revision',
        page,
        null,
        null,
        filter
      );

      return batchRequests(params).then((data) => {
        data = data.Revision;
        const total = data.total;
        this.attr('pageInfo.total', total);

        return this.makeRevisionModels(data);
      });
    },
    makeRevisionModels(data) {
      let revisions = data.values;
      revisions = revisions.map(function (source) {
        return Revision.model(source, 'Revision');
      });

      return revisions;
    },

    fetchItems: function () {
      this.attr('isLoading', true);
      this.attr('revisions', null);

      const stopFn = tracker.start(
        this.attr('instance.type'),
        tracker.USER_JOURNEY_KEYS.LOADING,
        tracker.USER_ACTIONS.CHANGE_LOG);

      return this._fetchRevisionsDataByQuery()
        .done((revisions) => {
          this.attr('revisions', revisions);
          stopFn();
        })
        .fail(function () {
          stopFn(true);
          $('body').trigger(
            'ajax:flash',
            {error: 'Failed to fetch revision history data.'});
        })
        .always(function () {
          this.attr('isLoading', false);
        }.bind(this));
    },
    _fetchAdditionalInfoForRevisions(refreshQueue, revisions) {
      _.forEach(revisions, (revision) => {
        if (revision.modified_by) {
          refreshQueue.enqueue(revision.modified_by);
        }
        if (revision.destination_type && revision.destination_id) {
          revision.destination = new Stub({
            id: revision.destination_id,
            type: revision.destination_type,
          });
          refreshQueue.enqueue(revision.destination);
        }
        if (revision.source_type && revision.source_id) {
          revision.source = new Stub({
            id: revision.source_id,
            type: revision.source_type,
          });
          refreshQueue.enqueue(revision.source);
        }
      });
    },
    /**
     * Fetch the instance's Revisions data from the server, including the
     * Revisions of the instance's mappings.
     *
     * The `instance` here refers to the instance of an object currently being
     * handled by the component.
     *
     * @return {$.Deferred} - an object representing the async operation of
     *   fetching the data from the server. On success it is resolved with an
     *   object containing the following Revision data, order by date from
     *   oldest to newest:
     *   - {Array} object - the list of Revisions of the instance itself,
     *   - {Array} mappings - the list of Revisions of all the instance's
     *      mappings
     */
    _fetchRevisionsData: function () {
      let findAll = function (attr) {
        let query = {__sort: 'updated_at'};
        query[attr + '_type'] = this.attr('instance.type');
        query[attr + '_id'] = this.attr('instance.id');
        return Revision.findAll(query);
      }.bind(this);

      return $.when(
        findAll('resource'), findAll('source'), findAll('destination')
      ).then(function (objRevisions, mappingsSrc, mappingsDest) {
        // manually include people for modified_by since using __include would
        // result in a lot of duplication
        let rq = new RefreshQueue();
        _.forEach(objRevisions.concat(mappingsSrc, mappingsDest),
          function (revision) {
            if (revision.modified_by) {
              rq.enqueue(revision.modified_by);
            }
          });
        _.forEach(mappingsSrc, function (revision) {
          if (revision.destination_type && revision.destination_id) {
            revision.destination = new Stub({
              id: revision.destination_id,
              type: revision.destination_type,
            });
            rq.enqueue(revision.destination);
          }
        });
        _.forEach(mappingsDest, function (revision) {
          if (revision.source_type && revision.source_id) {
            revision.source = new Stub({
              id: revision.source_id,
              type: revision.source_type,
            });
            rq.enqueue(revision.source);
          }
        });
        return this._fetchEmbeddedRevisionData(rq.objects, rq)
          .then(function (embedded) {
            return rq.trigger().then(function () {
              let reify = function (revision) {
                _.forEach(['modified_by', 'source', 'destination'],
                  function (field) {
                    if (revision[field] && isReifiable(revision[field])) {
                      revision.attr(field, reifyUtil(revision[field]));
                    }
                  });
                return revision;
              };
              let mappings = mappingsSrc.concat(mappingsDest, embedded);
              return {
                object: _.map(objRevisions, reify),
                mappings: _.map(mappings, reify),
              };
            });
          });
      }.bind(this));
    },
    _reifyRevision(revision) {
      _.forEach(['modified_by', 'source', 'destination'],
        function (field) {
          if (revision[field] && revision[field].reify) {
            revision.attr(field, revision[field].reify());
          }
        });
      return revision;
    },
    _fetchRevisionsDataByQuery() {
      let fetchRevisions = this.attr('showLastReviewUpdates') ?
        this.getAfterReviewRevisions.bind(this) :
        this.getAllRevisions.bind(this);

      return $.when(fetchRevisions(), this.getOriginRevision()).then(
        (revisions, originalRevisions) => {
          let rq = new RefreshQueue();

          this._fetchAdditionalInfoForRevisions(rq, revisions);
          this._fetchAdditionalInfoForRevisions(rq, originalRevisions);

          return rq.trigger().then(function () {
            let objRevisions = [];
            let mappings = [];
            _.forEach(revisions, (revision) => {
              if (revision.destination || revision.source) {
                mappings.push(revision);
              } else {
                objRevisions.push(revision);
              }
            });

            return {
              object: _.map(objRevisions, this._reifyRevision),
              mappings: _.map(mappings, this._reifyRevision),
              originalRevisions: _.map(originalRevisions, this._reifyRevision),
            };
          });
        });
    },
    /**
     * Fetch revisions of indirect mappings.
     *
     * @param {Array} mappedObjects - the list of object instances to fetch
     *   mappings to (objects mapped to the current instance).
     *
     * @param {RefreshQueue} rq - current refresh queue to use for fetching
     *   full objects.
     *
     * @return {Deferred} - A deferred that will resolve into a array of
     *   revisons of the indirect mappings.
     */
    _fetchEmbeddedRevisionData: function (mappedObjects, rq) {
      let instance = this.attr('instance');
      let id = this.attr('instance.id');
      let type = this.attr('instance.type');
      let filterElegible = function (obj) {
        return _.includes(this.attr('_EMBED_MAPPINGS')[type], obj.type);
      }.bind(this);
      let dfds;

      function fetchRevisions(obj) {
        return [
          Revision.findAll({
            source_type: obj.type,
            source_id: obj.id,
            __sort: 'updated_at',
          }).then(function (revisions) {
            return _.map(revisions, function (revision) {
              revision = new can.Map(revision.serialize());
              revision.attr({
                updated_at: new Date(revision.updated_at),
                source_type: type,
                source_id: id,
                source: instance,
                destination: new Stub({
                  type: revision.destination_type,
                  id: revision.destination_id,
                }),
              });
              rq.enqueue(revision.destination);
              return revision;
            });
          }),
          Revision.findAll({
            destination_type: obj.type,
            destination_id: obj.id,
            __sort: 'updated_at',
          }).then(function (revisions) {
            return _.map(revisions, function (revision) {
              revision = new can.Map(revision.serialize());
              revision.attr({
                updated_at: new Date(revision.updated_at),
                destination_type: type,
                destination_id: id,
                destination: instance,
                source: new Stub({
                  type: revision.source_type,
                  id: revision.source_id,
                }),
              });
              rq.enqueue(revision.source);
              return revision;
            });
          }),
        ];
      }

      dfds = _.chain(mappedObjects).filter(filterElegible)
        .map(fetchRevisions)
        .flatten()
        .value();
      return $.when(...dfds).then(function () {
        return _.filter(_.flatten(arguments), function (revision) {
          // revisions where source == destination will be introduced when
          // spoofing the obj <-> instance mapping
          return revision.source.href !== revision.destination.href;
        });
      });
    },
    changeLastUpdatesFilter(element) {
      const isChecked = element.checked;

      const review = this.attr('review');
      if (review) {
        review.setShowLastReviewUpdates(isChecked);
      }
      this.attr('pageInfo.current', 1);
      this.loadPage();
    },
    getLastUpdatesFlag() {
      return this.attr('showFilter') &&
        this.attr('showLastReviewUpdates');
    },
    resetLastUpdatesFlag() {
      const review = this.attr('review');

      if (review) {
        review.setShowLastReviewUpdates(false);
      }
    },
    initObjectReview() {
      const review = this.attr('instance.review');

      if (review) {
        this.attr('review', reifyUtil(review));
      }
    },
    loadPage() {
      this.fetchItems()
        .then(() => {
          const fullHistory = this.attr('fullHistory');
          this.attr('changeHistory', fullHistory);
        });
    },
  },
  /**
   * The component's entry point. Invoked when a new component instance has
   * been created.
   */
  init: function () {
    const viewModel = this.viewModel;

    viewModel.initObjectReview();

    this.viewModel.loadPage();
  },
  events: {
    '{viewModel.instance} refreshInstance': function () {
      this.viewModel.fetchItems();
    },
    '{viewModel.pageInfo} current'() {
      this.viewModel.loadPage();
    },
    '{viewModel.pageInfo} pageSize'() {
      this.viewModel.loadPage();
    },
    removed() {
      this.viewModel.resetLastUpdatesFlag();
    },
  },
});
