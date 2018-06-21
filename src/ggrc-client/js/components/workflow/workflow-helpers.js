/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {confirm} from '../../plugins/utils/modals';

/**
 * A set of properties which describe minimum information
 * about cycle.
 * @typedef {Object} CycleStub
 * @property {number} id - cycle id.
 * @property {string} type - cycle type.
 * @example
 * // stub for cycle
 * const cycleStub = {
 *  id: 123,
 *  type: "Cycle",
 * };
 */

export default {
  /**
   * Creates cycle instance.
   * @param {CMS.Models.Workflow} workflow - a workflow instance.
   * @return {CMS.Models.Cycle} - a new cycle based on workflow.
   */
  createCycle(workflow) {
    return new CMS.Models.Cycle({
      context: workflow.context.stub(),
      workflow: {id: workflow.id, type: 'Workflow'},
      autogenerate: true,
    });
  },
  /**
   * Redirects to cycle with certain id.
   * @param {CMS.Models.Cycle|CycleStub} cycle - an object containing cycle id.
   * @param {number} id - cycle id.
   */
  redirectToCycle({id}) {
    window.location.hash = `current/cycle/${id}`;
  },
  generateCycle: function (workflow) {
    let dfd = new $.Deferred();
    let cycle;

    confirm({
      modal_title: 'Confirm',
      modal_confirm: 'Proceed',
      skip_refresh: true,
      button_view: GGRC.mustache_path +
        '/workflows/confirm_start_buttons.mustache',
      content_view: GGRC.mustache_path +
        '/workflows/confirm_start.mustache',
      instance: workflow,
    }, (params, option) => {
      let data = {};

      can.each(params, function (item) {
        data[item.name] = item.value;
      });

      cycle = this.createCycle(workflow);

      cycle.save().then((cycle) => {
        // Cycle created. Workflow started.
        setTimeout(() => {
          dfd.resolve();
          this.redirectToCycle(cycle);
        }, 250);
      });
    }, function () {
      dfd.reject();
    });
    return dfd;
  },
  async updateStatus(instance, status) {
    // we refresh the instance, because without this
    // the server will return us 409 error
    const refreshed = await instance.refresh();
    refreshed.attr('status', status);
    return refreshed.save();
  },
};
