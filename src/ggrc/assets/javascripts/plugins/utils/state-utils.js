/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC) {
  'use strict';
  /**
   * Utils for state.
   */
  GGRC.Utils.State = (function () {
    var statesModels = [
      {
        models: [
          'AccessGroup', 'Clause', 'Contract',
          'Control', 'DataAsset', 'Facility', 'Issue', 'Market',
          'Objective', 'OrgGroup', 'Policy', 'Process', 'Product', 'Program',
          'Project', 'Regulation', 'Risk', 'Section', 'Standard', 'System',
          'Threat', 'Vendor', 'Issue'
        ],
        states: ['Active', 'Draft', 'Deprecated']
      },
      {
        models: ['Assessment'],
        states: [
          'Not Started', 'In Progress', 'Ready for Review',
          'Verified', 'Completed'
        ]
      },
      {
        models: ['Audit'],
        states: [
          'Planned', 'In Progress', 'Manager Review',
          'Ready for External Review', 'Completed'
        ]
      },
      {
        models: [
          'Person', 'CycleTaskGroupObjectTask',
          'AssessmentTemplate', 'Workflow',
          'TaskGroup', 'Cycle'
        ],
        states: []
      }
    ];

    /**
     * Check if model has state.
     * @param {String} model - The model name
     * @return {Boolean} True or False
     */
    function hasState(model) {
      var pair = getStatesModelsPair(model);

      if (!pair) {
        return false;
      }

      return pair.states.length > 0;
    }

    /**
     * Check if model should have filter by state.
     * @param {String} model - The model name
     * @return {Boolean} True or False
     */
    function hasFilter(model) {
      return hasState(model);
    }

    /**
     * Get States-Models pair.
     * @param {String} model - The model name
     * @return {Object} object with 'models' and 'states' properties
     */
    function getStatesModelsPair(model) {
      var pairs = statesModels.filter(function (item) {
        return item.models.indexOf(model) > -1;
      });

      return pairs.length > 0 ? pairs[0] : null;
    }

     /**
     * Get states for model.
     * @param {String} model - The model name
     * @return {Array} array of strings
     */
    function getStatesForModel(model) {
      var pair = getStatesModelsPair(model);
      return pair ? pair.states : [];
    }

    /**
     * Transform query for objects into query which filter them by state.
     * @param {Array} statuses - array of active statuses
     * @param {String} filterString - original query string
     * @return {String} The transformed query
     */
    function statusFilter(statuses, filterString) {
      var filter = statuses
        .map(function (item) {
          return 'Status=' + item;
        }).join(' Or ');

      filterString = filterString || '';
      if (filter !== '') {
        if (filterString !== '') {
          return filterString + ' And ' + filter;
        }
        return filter;
      }

      return filterString;
    }

    return {
      hasState: hasState,
      hasFilter: hasFilter,
      statusFilter: statusFilter,
      getStatesForModel: getStatesForModel
    };
  })();
})(window.GGRC);
