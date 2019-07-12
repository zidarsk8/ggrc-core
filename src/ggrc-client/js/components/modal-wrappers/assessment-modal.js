/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import '../assessment-template-attributes/assessment-template-attributes';
import '../assessment-templates/assessment-templates-dropdown/assessment-templates-dropdown';
import canMap from 'can-map';
import canComponent from 'can-component';
import {
  toObject,
  extendSnapshot,
} from '../../plugins/utils/snapshot-utils';
import {loadObjectsByStubs} from '../../plugins/utils/query-api-utils';
import {notifier} from '../../plugins/utils/notifiers-utils';
import {getAjaxErrorInfo} from '../../plugins/utils/errors-utils';

export default canComponent.extend({
  tag: 'assessment-modal',
  leakScope: true,
  viewModel: canMap.extend({
    instance: null,
    isNewInstance: false,
    mappedObjects: [],
    assessmentTemplate: null,
    isAttributesLoading: false,
    loadData() {
      return this.attr('instance').getRelatedObjects()
        .then((data) => {
          let snapshots = data.Snapshot.map((snapshot) => {
            let snapshotObject = toObject(snapshot);
            return extendSnapshot(snapshot, snapshotObject);
          });

          this.attr('mappedObjects', snapshots);
        });
    },
    async setAssessmentTemplate(templateId) {
      const instance = this.attr('instance');
      const audit = instance.attr('audit');
      const templateStub = {
        id: templateId,
        type: 'AssessmentTemplate',
      };

      this.attr('isAttributesLoading', true);
      try {
        const [loadedTemplate] = await loadObjectsByStubs(
          [templateStub],
          ['custom_attribute_definitions'],
          {
            type: audit.attr('type'),
            id: audit.attr('id'),
          },
        );

        instance.attr('template', templateStub);
        this.attr('assessmentTemplate', loadedTemplate);
      } catch (xhr) {
        notifier('error', getAjaxErrorInfo(xhr).details);
      } finally {
        this.attr('isAttributesLoading', false);
      }
    },
    onAssessmentTemplateChanged({template}) {
      if (!template) {
        this.attr('assessmentTemplate', null);
        this.attr('instance.template', null);
      } else {
        this.setAssessmentTemplate(template.id);
      }
    },
  }),
  events: {
    inserted() {
      let vm = this.viewModel;
      if (!vm.attr('isNewInstance')) {
        vm.loadData();
      }
    },
  },
});
