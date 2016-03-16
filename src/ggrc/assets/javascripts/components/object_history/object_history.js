/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: peter@reciprocitylabs.com
  Maintained By: peter@reciprocitylabs.com
*/

(function (GGRC, can) {
  'use strict';

  /**
   * A helper function for computing the difference between the two Revisions
   * of an object.
   *
   * The function assumes that the given revisions are two distinct Revisions
   * of the same object (application entity).
   *
   * NOTE: The object fields that do not have a user-friendly alias defined are
   * considered "internal", and are thus not included in the resulting diff
   * objects, because they are not meant to be shown to the end user.
   *
   * @param {CMS.Models.Revision} rev1 - the older of the two revisions
   * @param {CMS.Models.Revision} rev2 - the newer of the two revisions
   *
   * @return {Array} - A "diff" object describing the changes between the
   *   revisions. The object has the following attributes:
   *   - madeBy: the user who made the changes
   *   - updatedAt: the time when the changes have been made
   *   - changes:
   *       A list of objects describing the modified attributes of the
   *       instance`, with each object having the following attributes:
   *         - fieldName: the name of the changed`instance` attribute
   *         - origVal: the attribute's original value
   *         - newVal: the attribute's new (modified) value
   */
  function revisionDiff(rev1, rev2) {
    var diff = {
      madeBy: null,
      updatedAt: null,
      changes: []
    };
    var attrDefs = GGRC.model_attr_defs[rev2.resource_type];

    diff.madeBy = 'User ' + rev2.modified_by.id;
    diff.updatedAt = rev2.updated_at;

    can.each(rev2.content, function (value, fieldName) {
      var origVal = rev1.content[fieldName];
      var displayName;
      if (attrDefs) {
        displayName = (_.find(attrDefs, function (attr) {
          return attr.attr_name === fieldName;
        }) || {}).display_name;
      } else {
        displayName = fieldName;
      }

      if (displayName && value !== origVal) {
        diff.changes.push({
          fieldName: displayName,
          origVal: origVal,
          newVal: value
        });
      }
    });

    return diff;
  }

  /**
   * Compute the the history of changes for the given object.
   *
   * The computed list of changes is sorted from oldest to newest (the helper
   * assumes that the `instance`'s revision history is also sorted
   * chronologically with the oldest Revision first).
   *
   * The helper creates a new Mustache context containing the `objectChanges`
   * attribute. That attribute is list of "diff" objects representing the
   * differences between the pairs of two successive Revisions of the
   * `instance`. The diff objects follow the format returned by the
   * `caclulateDiff` helper function.
   *
   * Example usage of the helper in a mustache template:
   *
   *   {{#revisions_diff instance}}
   *     {{#objectChanges}}
   *       ...
   *     {{/objectChanges}}
   *   {{/revision_diff}}
   *
   * @param {can.Model.Cacheable} instance - an application entity instance
   * @param {Object} options - a CanJS options argument passed to every helper
   *
   * @return {String} - the rendered instance history log
   *
   */
  function calculateRevisionsDiff(instance, options) {
    var diff;
    var diffList = [];
    var i;
    var newContext;

    var instResolved = Mustache.resolve(instance);

    var revisions = instResolved.get_mapping('revision_history');
    revisions = _.map(revisions, 'instance');

    // Only operate on the list if the Revision history has been fully
    // fetched from the server (and not just the Revision objects stubs).
    if ((revisions.length > 0) && revisions[0].content) {
      for (i = 1; i < revisions.length; i++) {
        diff = revisionDiff(revisions[i - 1], revisions[i]);
        diffList.push(diff);
      }
    }

    newContext = options.contexts.add({
      objectChanges: diffList
    });

    return options.fn(newContext);
  }

  /**
   * A component that calculates and renders the given Model object's revision
   * history.
   */
  GGRC.Components('objectHistory', {
    tag: 'revision-log',

    template: can.view(
      GGRC.mustache_path +
      '/components/object_history/object_history.mustache'
    ),

    // TODO: tests for the default values
    scope: {
      instance: null,
      objectChanges: new can.List(),
      mappingsChanges: new can.List()
    },

    helpers: {
      revisions_diff: calculateRevisionsDiff
    },

    // the type of the object the component is operating on
    _INSTANCE_TYPE: null,

    /**
     * The component's entry point. Invoked when a new component instance has
     * been created.
     */
    init: function () {
      // TODO: check and raise error if instance not set! must be passed to it!

      this._INSTANCE_TYPE = this.scope.instance.type;

      this._fetchRevisionsData(
        this.scope.instance
      )
      .then(function (revisions) {
        // var objChanges = computeObjectChanges(revisions.object);
        var mappingsChanges = this._computeMappingChanges(revisions.mappings);

        // this.scope.attr('objectChanges', objChanges);
        this.scope.attr('mappingChanges', mappingsChanges);
      }.bind(this));
    },

    /**
     * Fetch the instance's Revisions data from the server, including the
     * Revisions of the instance's mappings.
     *
     * The `instance` here refers to the instance of an object currently being
     * handled by the component.
     *
     * @return {can.Deferred} - an object representing the async operation of
     *   fetching the data from the server. On success it is resolved with an
     *   object containing the following:
     *   - {can.List} object - the list of Revisions of the instance itself,
     *   - {can.List} mappings - the list of Revisions of all the instance's
     *      mappings
     */
    _fetchRevisionsData: function () {
      // TODO: tests
      //
      // TODO: add fail handler
      // TODO: run run when there is a change of the instance?
      // TODO: this seems to always run when the UI tab is switched - is there
      //       an easy way to cache the results? And for how long?
      var Revision = CMS.Models.Revision;

      var instance = this.scope.instance;

      // TODO: make sure to order by! oldest to newest probably...
      // __sort: "field1, field2" ... kako pa sicer? - spredaj da je obratno?
      // AND document in the docstring!
      var dfd = Revision.findAll({
        resource_type: this._INSTANCE_TYPE,
        resource_id: instance.id
      });

      var dfd2 = Revision.findAll({
        source_type: this._INSTANCE_TYPE,
        source_id: instance.id
      });

      var dfd3 = Revision.findAll({
        destination_type: this._INSTANCE_TYPE,
        destination_id: instance.id
      });

      var dfdResults = can.when(
        dfd, dfd2, dfd3
      ).then(function (objRevisions, mappingsSrc, mappingsDest) {
        var revisions = {
          object: objRevisions,
          mappings: mappingsSrc.concat(mappingsDest)
        };
        return revisions;
      });

      return dfdResults;
    },

    /**
     * Compute the instance's object mapping-related changes from the list of
     * mapping revisions.
     *
     * @param {can.List} revisions - the list of instance mappings' revision
     *   history, sorted from oldest to newest.
     *
     * @return {can.List} - the history of instance mappings' changes. Each
     *   element follows the format returned by the `_mappingChange` helper
     *   method.
     */
    _computeMappingChanges: function (revisions) {
      // TODO: tests
      var result = _.map(revisions, this._mappingChange.bind(this));
      return new can.List(result);
    },

    /**
     * A helper function for extracting the mapping change information from a
     * Revision object.
     *
     * @param {CMS.Models.Revision} rev - a Revision object describing a
     *   mapping between the object instance the component is handling, and an
     *   external object
     *
     * @return {can.Map} - A "change" object describing a single modification
     *   of a mapping. The object has the following attributes:
     *   - madeBy: the user who made the changes
     *   - updatedAt: the time when the changes have been made
     *   - mapping:
     *       Information about the changed mapping containing the following:
     *         - action: the mapping action that was performed by a user,
     *             can be either "Create" or "Delete"
     *         - relatedObjId: the ID of the object at the other end of the
     *             mapping (*)
     *         - relatedObjType: the type of the object at the other end of the
     *             mapping (*)
     *
     *         (*) The object on "this" side of the mapping is of course the
     *             instance the component is handling.
     */
    _mappingChange: function (rev) {
      // TODO: tests
      var change = {
        madeBy: null,
        updatedAt: null,
        mapping: {}
      };

      change.madeBy = 'User ' + rev.modified_by.id;
      change.updatedAt = rev.updated_at;

      change.mapping.action = _.capitalize(rev.action);

      // The instance the component is handling can be on either side of the
      // mapping, i.e. source or destination, but we are interested in the
      // object on the "other" end of the mapping.
      if (rev.destination_type === this._INSTANCE_TYPE) {
        change.mapping.relatedObjId = rev.source_id;
        change.mapping.relatedObjType = rev.source_type;
      } else {
        change.mapping.relatedObjId = rev.destination_id;
        change.mapping.relatedObjType = rev.destination_type;
      }

      return new can.Map(change);
    }
  });
})(window.GGRC, window.can);
