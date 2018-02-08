/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../sortable-column/sortable-column';
import '../object-list/object-list';
import '../object-list-item/business-object-list-item';
import '../object-list-item/document-object-list-item';
import '../object-popover/related-assessment-popover';
import '../reusable-objects/reusable-objects-item';
import '../state-colors-map/state-colors-map';
import '../spinner/spinner';
import '../tree_pagination/tree_pagination';
import Pagination from '../base-objects/pagination';
import template from './templates/related-assessments.mustache';
import {prepareCustomAttributes} from '../../plugins/utils/ca-utils';

let mapper = {
  mapObjects: function (source, destination) {
    return new CMS.Models.Relationship({
      context: source.context || {id: null},
      source: source,
      destination: destination,
    });
  },
};

const defaultOrderBy = [
  {field: 'finished_date', direction: 'desc'},
  {field: 'created_at', direction: 'desc'},
];

export default can.Component.extend({
  tag: 'related-assessments',
  template,
  viewModel: {
    define: {
      baseInstanceDocuments: {
        get: function () {
          return this.attr('urls').concat(this.attr('evidences'));
        },
      },
      hasSelected: {
        get: function () {
          return this.attr('documentList.length');
        },
      },
      needReuse: {
        type: 'boolean',
        value: true,
      },
      relatedObjectType: {
        get: function () {
          // Get related object type based on assessment or the instance itself
          // 'instance.assessment_type' is used for object in "Related assessments" in
          // assessments info pane.
          // 'instance.type' is used when we are getting related assessment for
          // a snapshot.
          return this.attr('instance.assessment_type') ||
                 this.attr('instance.type');
        },
      },
      mappedSnapshots: {
        type: 'boolean',
        value: true,
      },
      relatedObjectsFilter: {
        get: function () {
          return {
            only: [this.attr('relatedObjectType')],
            exclude: [],
          };
        },
      },
      relatedObjectsTitle: {
        get: function () {
          const relObjType = this.attr('relatedObjectType');

          const objectName = CMS.Models[relObjType].model_plural;
          return `Related ${objectName}`;
        },
      },
      paging: {
        value: function () {
          return new Pagination({pageSizeSelect: [5, 10, 15]});
        },
      },
    },
    evidences: [],
    urls: [],
    instance: {},
    documentList: [],
    orderBy: {},
    isSaving: false,
    loading: false,
    needReuse: '@',
    baseInstanceDocuments: [],
    relatedAssessments: [],
    selectedItem: {},
    objectSelectorEl: '.grid-data__action-column button',
    noRelatedObjectsMessage: 'No Related Assessments were found',
    getMapObjects: function (source, list) {
      return list
        .filter(function (item, index) {
          return index === list.indexOf(item);
        })
        // Get Array of mapped models
        .map(function (destination) {
          return mapper
            .mapObjects(source, destination)
            .save();
        });
    },
    reuseSelected: function () {
      let reusedObjectList =
        this.getMapObjects(
          this.attr('instance'),
          this.attr('documentList'));
      this.attr('isSaving', true);

      can.when.apply(can, reusedObjectList)
        .always(this.restoreDefaults.bind(this));
    },
    restoreDefaults: function () {
      this.attr('documentList').replace([]);
      this.attr('isSaving', false);
      this.dispatch('afterObjectReused');
      this.attr('instance').dispatch('refreshInstance');
    },
    loadRelatedAssessments() {
      const limits = this.attr('paging.limits');
      const orderBy = this.attr('orderBy');
      let currentOrder = [];

      if (!orderBy.attr('field')) {
        currentOrder = defaultOrderBy;
      } else {
        currentOrder = [orderBy];
      }

      this.attr('loading', true);

      return this.attr('instance').getRelatedAssessments(limits, currentOrder)
        .then((response) => {
          const assessments = response.data.map((assessment) => {
            let values = assessment.custom_attribute_values || [];
            let definitions = assessment.custom_attribute_definitions || [];

            if (definitions.length) {
              assessment.custom_attribute_values =
                prepareCustomAttributes(definitions, values);
            }

            return {
              instance: assessment,
            };
          });

          this.attr('paging.total', response.total);
          this.attr('relatedAssessments').replace(assessments);

          this.attr('loading', false);
        }, () => {
          this.attr('loading', false);
        });
    },
  },
  init() {
    this.viewModel.loadRelatedAssessments();
  },
  events: {
    '{viewModel.paging} current'() {
      this.viewModel.loadRelatedAssessments();
    },
    '{viewModel.paging} pageSize'() {
      this.viewModel.loadRelatedAssessments();
    },
    '{viewModel.orderBy} changed'() {
      this.viewModel.loadRelatedAssessments();
    },
  },
});
