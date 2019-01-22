/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './templates/task-group-objects.stache';
import {DEFERRED_MAP_OBJECTS} from '../../../events/eventTypes';
import {
  mapObjects,
  unmapObjects,
} from '../../../plugins/utils/mapper-utils';
import {notifier} from '../../../plugins/utils/notifiers-utils';
import {
  loadObjectsByStubs,
  loadObjectsByTypes,
} from '../../../plugins/utils/query-api-utils';

import Stub from '../../../models/stub';
import Mappings from '../../../models/mappers/mappings';

const requiredObjectsFields = ['id', 'type', 'title'];

const viewModel = can.Map.extend({
  canEdit: false,
  taskGroup: null,
  items: [],
  addToList(objects) {
    const newItems = objects.map((object) => this.convertToListItem(object));
    this.attr('items').push(...newItems);
  },
  convertToListItem(object) {
    return {
      stub: new Stub(object),
      title: object.title,
      iconClass: `fa-${_.snakeCase(object.type)}`,
      disabled: false,
    };
  },
  async initTaskGroupItems() {
    const mappingTypes = Mappings.getMappingList('TaskGroup');
    const mappedObjects = await loadObjectsByTypes(
      this.attr('taskGroup'),
      mappingTypes,
      requiredObjectsFields
    );
    this.addToList(mappedObjects);
  },
  async map(stubs) {
    await mapObjects(this.attr('taskGroup'), stubs);
    const loadedObjects = await loadObjectsByStubs(
      stubs,
      requiredObjectsFields
    );
    this.addToList(loadedObjects);
  },
  async unmapByItemIndex(itemIndex) {
    const items = this.attr('items');
    const item = items[itemIndex];

    item.attr('disabled', true);
    await unmapObjects(this.attr('taskGroup'), [item.attr('stub')]);
    item.attr('disabled', false);

    // remove unmapped object from the list
    // Need to get updated index because
    // "items" collection can be changed
    // in case when the user unmaps several objects -
    // "itemIndex" will store old index of item.
    items.splice(items.indexOf(item), 1);
    notifier('success', 'Unmap successful.');
  },
});

const events = {
  inserted() {
    // Pass taskGroup into object-mapper via "deferred_to"
    // data attribute
    this.element.find('[data-toggle="unified-mapper"]')
      .data('deferred_to', {
        instance: this.viewModel.attr('taskGroup'),
      });
  },
  [`{viewModel.taskGroup} ${DEFERRED_MAP_OBJECTS.type}`](el, {objects}) {
    this.viewModel.map(objects);
  },
  '.task-group-objects__unmap click'(el) {
    this.viewModel.unmapByItemIndex(el.attr('data-item-index'));
  },
};

const init = function () {
  this.viewModel.initTaskGroupItems();
};

export default can.Component({
  tag: 'task-group-objects',
  template: can.stache(template),
  leakScope: true,
  viewModel,
  events,
  init,
});
