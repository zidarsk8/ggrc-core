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
      parent_instance: null,
      instance: null,
      instance_attr: '@',
      source_mapping: '@',
      default_mappings: [], // expects array of objects
      mapping: '@',
      deferred: '@',
      attributes: {},
      newInstance: false,
      list: [],
      // the following are just for the case when we have no object to start with,
      changes: [],
    },
    events: {
      init: function () {
        let that = this;
        let key;
        let instance;
        let vm = this.viewModel;
        vm.attr('controller', this);
        if (!vm.instance) {
          vm.attr('deferred', true);
        } else if (vm.instance.reify) {
          vm.attr('instance', vm.instance.reify());
        }

        vm.default_mappings.forEach(function (defaultMapping) {
          let model;
          let objectToAdd;
          if (defaultMapping.id && defaultMapping.type) {
            model = CMS.Models[defaultMapping.type];
            objectToAdd = model.findInCacheById(defaultMapping.id);
            that.viewModel.instance
              .mark_for_addition('related_objects_as_source', objectToAdd, {});
            that.addListItem(objectToAdd);
          }
        });

        if (!vm.source_mapping) {
          vm.attr('source_mapping', vm.mapping);
        }

        instance = vm.attr('instance');

        if (instance) {
          if (!vm.attr('customRelatedLoader')) {
            instance.get_binding(vm.source_mapping)
              .refresh_instances()
              .then(function (list) {
                this.setListItems(list);
              }.bind(this));
          }
        } else {
          key = vm.instance_attr + '_' + (vm.mapping || vm.source_mapping);
          if (!vm.parent_instance._transient[key]) {
            vm.attr('list', []);
            vm.parent_instance.attr('_transient.' + key, vm.list);
          } else {
            vm.attr('list', vm.parent_instance._transient[key]);
          }
        }

        this.options.parent_instance = vm.parent_instance;
        this.options.instance = vm.instance;
        this.on();
      },
      destroy: function () {
        this.viewModel.parent_instance.removeAttr('_changes');
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
        this.viewModel.attr('instance', this.viewModel.attr('parent_instance')
          .attr(this.viewModel.instance_attr).reify());
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
      '{parent_instance} updated': 'deferred_update',
      '{parent_instance} created': 'deferred_update',

      // this works like autocomplete_select on all modal forms and
      // descendant class objects.
      autocomplete_select: function (el, event, ui) {
        let mapping;
        let extraAttrs;
        if (!this.element) {
          return;
        }
        extraAttrs = can.reduce(
          this.element.find('input:not([data-mapping], [data-lookup])').get(),
          function (attrs, el) {
            attrs[$(el).attr('name')] = $(el).val();
            return attrs;
          }, {});
        if (this.viewModel.attr('deferred')) {
          this.viewModel.changes.push({
            what: ui.item,
            how: 'add',
            extra: extraAttrs,
          });
          this.viewModel.parent_instance.attr('_changes',
            this.viewModel.changes);
        } else {
          mapping = this.viewModel.mapping ||
            GGRC.Mappings.get_canonical_mapping_name(
              this.viewModel.instance.constructor.shortName,
              ui.item.constructor.shortName);
          this.viewModel.instance
            .mark_for_addition(mapping, ui.item, extraAttrs);
        }
        function doesExist(arr, owner) {
          if (!arr || !arr.length) {
            return false;
          }
          return !!~can.inArray(owner.id, $.map(arr, function (item) {
            return item.id;
          }));
        }

        // If it's owners and user isn't pre-added
        if (!(~['owners'].indexOf(this.viewModel.mapping) &&
          doesExist(this.viewModel.list, ui.item))) {
          this.addListItem(ui.item);
        }
        this.viewModel.attr('show_new_object_form', false);
      },
      '[data-toggle=unmap] click': function (el, ev) {
        ev.stopPropagation();

        can.map(el.find('.result'), function (resultEl) {
          let obj = $(resultEl).data('result');
          let len = this.viewModel.list.length;
          let mapping;

          if (this.viewModel.attr('deferred')) {
            this.viewModel.changes.push({what: obj, how: 'remove'});
            this.viewModel.parent_instance.attr('_changes',
              this.viewModel.changes);
          } else {
            mapping = this.viewModel.mapping ||
              GGRC.Mappings.get_canonical_mapping_name(
                this.viewModel.instance.constructor.shortName,
                obj.constructor.shortName);
            this.viewModel.instance.mark_for_deletion(mapping, obj);
          }
          for (; len >= 0; len--) {
            if (this.viewModel.list[len] === obj) {
              this.viewModel.list.splice(len, 1);
            }
          }
        }.bind(this));
      },
      'input[null-if-empty] change': function (el) {
        if (!el.val()) {
          this.viewModel.attributes.attr(el.attr('name'), null);
        }
      },
      'input keyup': function (el, ev) {
        ev.stopPropagation();
      },
      'input, textarea, select change': function (el, ev) {
        this.viewModel.attributes.attr(el.attr('name'), el.val());
      },

      'input:not([data-lookup], [data-mapping]), textarea keyup':
        function (el, ev) {
          if (el.prop('value').length === 0 ||
            (typeof el.attr('value') !== 'undefined' &&
            el.attr('value').length === 0)) {
            this.viewModel.attributes.attr(el.attr('name'), el.val());
          }
        },
      'a[data-toggle=submit]:not(.disabled) click': function (el, ev) {
        let obj;
        let mapping;
        let that = this;
        let binding = this.viewModel.instance
          .get_binding(this.viewModel.mapping);
        let extraAttrs = can.reduce(
          this.element.find('input:not([data-mapping], [data-lookup])').get(),
          function (attrs, el) {
            if ($(el).attr('model')) {
              attrs[$(el).attr('name')] =
                CMS.Models[$(el).attr('model')].findInCacheById($(el).val());
            } else {
              attrs[$(el).attr('name')] = $(el).val();
            }
            return attrs;
          }, {});

        ev.stopPropagation();

        extraAttrs[binding.loader.object_attr] = this.viewModel.instance;
        if (binding.loader instanceof GGRC.ListLoaders.DirectListLoader) {
          obj = new CMS.Models[binding.loader.model_name](extraAttrs);
        } else {
          obj = new CMS.Models[binding.loader.option_model_name](extraAttrs);
        }

        if (that.viewModel.attr('deferred')) {
          that.viewModel.changes
            .push({what: obj, how: 'add', extra: extraAttrs});
        } else {
          mapping = that.viewModel.mapping ||
            GGRC.Mappings.get_canonical_mapping_name(
              that.viewModel.instance.constructor.shortName,
              obj.constructor.shortName);
          that.viewModel.instance.mark_for_addition(mapping, obj, extraAttrs);
        }
        that.addListItem(obj);
        that.viewModel.attr('attributes', {});
      },
      'a[data-object-source] modal:success': 'addMapings',
      'defer:add': 'addMapings',
      addMapings: function (el, ev, data) {
        let mapping;
        ev.stopPropagation();

        can.each(data.arr || [data], function (obj) {
          if (this.viewModel.attr('deferred')) {
            this.viewModel.changes.push({what: obj, how: 'add'});
            this.viewModel.parent_instance.attr('_changes',
              this.viewModel.changes);
          } else {
            mapping = this.viewModel.mapping ||
              GGRC.Mappings.get_canonical_mapping_name(
                this.viewModel.instance.constructor.shortName,
                obj.constructor.shortName);
            this.viewModel.instance.mark_for_addition(mapping, obj);
          }
          this.addListItem(obj);
        }, this);
      },
      '.ui-autocomplete-input modal:success': function (el, ev, data, options) {
        let that = this;
        let extraAttrs = can.reduce(this.element
            .find('input:not([data-mapping], [data-lookup])').get(),
          function (attrs, el) {
            if ($(el).attr('model')) {
              attrs[$(el).attr('name')] = CMS.Models[$(el).attr('model')]
                .findInCacheById($(el).val());
            } else {
              attrs[$(el).attr('name')] = $(el).val();
            }
            return attrs;
          }, {});

        can.each(data.arr || [data], function (obj) {
          let mapping;
          if (that.viewModel.attr('deferred')) {
            that.viewModel.changes
              .push({what: obj, how: 'add', extra: extraAttrs});
          } else {
            mapping = that.viewModel.mapping ||
              GGRC.Mappings.get_canonical_mapping_name(
                that.viewModel.instance.constructor.shortName,
                obj.constructor.shortName);
            that.viewModel.instance.mark_for_addition(mapping, obj, extraAttrs);
          }
          that.addListItem(obj);
          that.viewModel.attr('attributes', {});
        });
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
    helpers: {
      // Mapping-based autocomplete selectors use this helper to
      //  attach the mapping autocomplete ui widget.  These elements should
      //  be decorated with data-mapping attributes.
      mapping_autocomplete: function (options) {
        return function (el) {
          let $el = $(el);
          $el.ggrc_mapping_autocomplete({
            controller: options.contexts.attr('controller'),
            model: $el.data('model'),
            mapping: false,
          });
        };
      },
    },
  });
})(window.can, window.can.$);
