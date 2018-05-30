/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {
  toObject,
  isSnapshotType,
} from '../plugins/utils/snapshot-utils';

(function (can, $) {
  /*
   Below this line we're defining a can.Component, which is in this file
   because it works in tandem with the modals form controller.

   The purpose of this component is to allow for pending adds/removes of connected
   objects while the modal is visible.  On save, the actual pending actions will
   be resolved and we won't worry about the transient state we use anymore.
   */
  GGRC.Components('modalConnector', {
    tag: 'ggrc-modal-connector',
    // <content> in a component template will be replaced with whatever is contained
    //  within the component tag.  Since the views for the original uses of these components
    //  were already created with content, we just used <content> instead of making
    //  new view template files.
    template: '<isolate-form><content/></isolate-form>',
    viewModel: {
      define: {
        customRelatedLoader: {
          type: Boolean,
          value: false,
        },
      },
      instance: null,
      source_mapping: '@',
      default_mappings: [], // expects array of objects
      mapping: '@',
      newInstance: false,
      list: [],
      // the following are just for the case when we have no object to start with,
      changes: [],
    },
    events: {
      init: function () {
        let that = this;
        let vm = this.viewModel;
        vm.attr('controller', this);
        if (vm.instance.reify) {
          vm.attr('instance', vm.instance.reify());
        }

        const instance = vm.attr('instance');
        vm.default_mappings.forEach(function (defaultMapping) {
          let model;
          let objectToAdd;
          if (defaultMapping.id && defaultMapping.type) {
            model = CMS.Models[defaultMapping.type];
            objectToAdd = model.findInCacheById(defaultMapping.id);
            instance
              .mark_for_addition('related_objects_as_source', objectToAdd, {});
            that.addListItem(objectToAdd);
          }
        });

        if (!vm.source_mapping) {
          vm.attr('source_mapping', vm.mapping);
        }

        if (!vm.attr('customRelatedLoader')) {
          instance.get_binding(vm.source_mapping)
            .refresh_instances()
            .then(function (list) {
              this.setListItems(list);
            }.bind(this));
        }

        this.on();
      },
      setListItems: function (list) {
        let currentList = this.viewModel.attr('list');
        this.viewModel.attr('list', currentList.concat(can.map(list,
          function (binding) {
            return binding.instance || binding;
          })));
      },
      '{viewModel} list': function () {
        let person;
        // Workaround so we render pre-defined users.
        if (~['owners'].indexOf(this.viewModel.mapping) &&
          this.viewModel.list && !this.viewModel.list.length) {
          person = CMS.Models.Person.findInCacheById(GGRC.current_user.id);
          this.viewModel.instance
            .mark_for_addition(this.viewModel.mapping, person, {});
          this.addListItem(person);
        }
      },
      deferred_update: function () {
        let changes = this.viewModel.changes;
        let instance = this.viewModel.instance;

        if (!changes.length) {
          if (instance && instance._pending_joins &&
            instance._pending_joins.length) {
            instance.delay_resolving_save_until(instance.constructor
              .resolve_deferred_bindings(instance));
          }
          return;
        }
        // Add pending operations
        can.each(changes, function (item) {
          let mapping = this.viewModel.mapping ||
              GGRC.Mappings.get_canonical_mapping_name(
                this.viewModel.instance.constructor.shortName,
                item.what.constructor.shortName);
          if (item.how === 'add') {
            this.viewModel.instance
              .mark_for_addition(mapping, item.what, item.extra);
          } else {
            this.viewModel.instance.mark_for_deletion(mapping, item.what);
          }
        }.bind(this)
        );
        this.viewModel.instance
          .delay_resolving_save_until(
            this.viewModel.instance.constructor
              .resolve_deferred_bindings(this.viewModel.instance));
      },
      '{instance} updated': 'deferred_update',
      '{instance} created': 'deferred_update',
      '[data-toggle=unmap] click': function (el, ev) {
        ev.stopPropagation();

        can.map(el.find('.result'), function (resultEl) {
          let obj = $(resultEl).data('result');
          let len = this.viewModel.list.length;

          this.viewModel.changes.push({what: obj, how: 'remove'});
          for (; len >= 0; len--) {
            if (this.viewModel.list[len] === obj) {
              this.viewModel.list.splice(len, 1);
            }
          }
        }.bind(this));
      },
      'a[data-object-source] modal:success': 'addMapings',
      'defer:add': 'addMapings',
      addMapings: function (el, ev, data) {
        ev.stopPropagation();

        can.each(data.arr || [data], function (obj) {
          this.viewModel.changes.push({what: obj, how: 'add'});
          this.addListItem(obj);
        }, this);
      },
      addListItem: function (item) {
        let snapshotObject;

        if (isSnapshotType(item) &&
          item.snapshotObject) {
          snapshotObject = item.snapshotObject;
          item.attr('title', snapshotObject.title);
          item.attr('description', snapshotObject.description);
          item.attr('class', snapshotObject.class);
          item.attr('snapshot_object_class', 'snapshot-object');
          item.attr('viewLink', snapshotObject.originalLink);
        } else if (!isSnapshotType(item) && item.reify) {
          // add full item object from cache
          // if it isn't snapshot
          item = item.reify();
        }

        this.viewModel.list.push(item);
      },
    },
  });
})(window.can, window.can.$);
