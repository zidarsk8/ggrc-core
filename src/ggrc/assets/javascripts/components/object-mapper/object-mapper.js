/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $) {
  'use strict';

  var DEFAULT_OBJECT_MAP = {
    Assessment: 'Control',
    Objective: 'Control',
    Section: 'Objective',
    Regulation: 'Section',
    Product: 'System',
    Standard: 'Section',
    Contract: 'Clause'
  };

  /**
   * A component implementing a modal for mapping objects to other objects,
   * taking the object type mapping constraints into account.
   */
  GGRC.Components('objectMapper', {
    tag: 'object-mapper',
    template: can.view(GGRC.mustache_path +
      '/components/object-mapper/object-mapper.mustache'),
    viewModel: function (attrs, parentViewModel, el) {
      var $el = $(el);
      var data = {};
      var id = Number($el.attr('join-object-id'));
      var object = $el.attr('object');
      var type = $el.attr('type');
      var isNew = parentViewModel.attr('is_new');
      var treeView = GGRC.tree_view.sub_tree_for[object];

      if (object) {
        data.object = object;
      }

      type = CMS.Models[type] && type;
      if (type) {
        data.type = type;
      } else {
        data.type = DEFAULT_OBJECT_MAP[object];
        if (!data.type) {
          data.type = treeView ? treeView.display_list[0] : 'Control';
        }
      }

      if (isNew) {
        data.join_object_id = null;
      } else if (id || GGRC.page_instance()) {
        data.join_object_id = id || GGRC.page_instance().id;
      }

      return {
        isLoadingOrSaving: function () {
          return this.attr('mapper.is_saving') ||
          //  disable changing of object type while loading
          //  to prevent errors while speedily selecting different types
          this.attr('mapper.is_loading');
        },
        mapper: new GGRC.Models.MapperModel(can.extend(data, {
          relevantTo: parentViewModel.attr('relevantTo')
        }))
      };
    },

    events: {
      '.create-control modal:success': function (el, ev, model) {
        this.viewModel.attr('mapper.newEntries').push(model);
        this.element.find('mapper-results').viewModel().showNewEntries();
      },
      '.create-control modal:added': function (el, ev, model) {
        this.viewModel.attr('mapper.newEntries').push(model);
      },
      '.create-control click': function () {
        // reset new entries
        this.viewModel.attr('mapper.newEntries', []);
      },
      '{window} modal:dismiss': function (el, ev, options) {
        var joinObjectId = this.viewModel.attr('mapper.join_object_id');

        // mapper sets uniqueId for modal-ajax.
        // we can check using unique id which modal-ajax is closing
        if (options.uniqueId &&
          joinObjectId === options.uniqueId &&
          this.viewModel.attr('mapper.newEntries').length > 0) {
          this.element.find('mapper-results').viewModel().showNewEntries();
        }
      },
      inserted: function () {
        var self = this;
        var deferredToList;
        this.viewModel.attr('mapper.selected').replace([]);
        this.viewModel.attr('mapper.entries').replace([]);

        this.setModel();

        if (this.viewModel.attr('deferred_to') &&
          this.viewModel.attr('deferred_to').list) {
          deferredToList = this.viewModel.attr('deferred_to').list
            .map(function (item) {
              return {
                id: item.id,
                type: item.type
              };
            });
          this.viewModel.attr('mapper.deferred_list', deferredToList);
        }

        self.viewModel.attr('mapper').afterShown();
      },
      closeModal: function () {
        this.viewModel.attr('mapper.is_saving', false);

        // TODO: Find proper way to dismiss the modal
        this.element.find('.modal-dismiss').trigger('click');
      },
      deferredSave: function () {
        var source = this.viewModel.attr('deferred_to').instance ||
          this.viewModel.attr('mapper.object');
        var data = {};

        data = {
          multi_map: true,
          arr: _.compact(_.map(
            this.viewModel.attr('mapper.selected'),
            function (desination) {
              var isAllowed = GGRC.Utils.allowed_to_map(source, desination);
              var instance =
                can.makeArray(this.viewModel.attr('mapper.entries'))
                  .map(function (entry) {
                    return entry.instance || entry;
                  })
                  .find(function (instance) {
                    return instance.id === desination.id &&
                      instance.type === desination.type;
                  });
              if (instance && isAllowed) {
                return instance;
              }
            }.bind(this)
          ))
        };

        this.viewModel.attr('deferred_to').controller.element.trigger(
          'defer:add', [data, {map_and_save: true}]);
        this.closeModal();
      },
      '.modal-footer .btn-map click': function (el, ev) {
        var type = this.viewModel.attr('mapper.type');
        var object = this.viewModel.attr('mapper.object');
        var instance = CMS.Models[object].findInCacheById(
          this.viewModel.attr('mapper.join_object_id'));
        var mapping;
        var Model;
        var data = {};
        var defer = [];
        var que = new RefreshQueue();

        ev.preventDefault();
        if (el.hasClass('disabled') ||
          this.viewModel.attr('mapper.is_saving')) {
          return;
        }

        // TODO: Figure out nicer / proper way to handle deferred save
        if (this.viewModel.attr('deferred')) {
          return this.deferredSave();
        }
        this.viewModel.attr('mapper.is_saving', true);

        que.enqueue(instance).trigger().done(function (inst) {
          data.context = instance.context || null;
          this.viewModel.attr('mapper.selected').forEach(
          function (destination) {
            var modelInstance;
            var isMapped;
            var isAllowed;
            var isPersonMapping = type === 'Person';
            // Use simple Relationship Model to map Snapshot
            if (this.viewModel.attr('mapper.useSnapshots')) {
              modelInstance = new CMS.Models.Relationship({
                context: data.context,
                source: instance,
                destination: {
                  href: '/api/snapshots/' + destination.id,
                  type: 'Snapshot',
                  id: destination.id
                }
              });

              return defer.push(modelInstance.save());
            }

            isMapped = GGRC.Utils.is_mapped(instance, destination);
            isAllowed = GGRC.Utils.allowed_to_map(instance, destination);

            if ((!isPersonMapping && isMapped) || !isAllowed) {
              return;
            }
            mapping = GGRC.Mappings.get_canonical_mapping(object, type);
            Model = CMS.Models[mapping.model_name];
            data[mapping.object_attr] = {
              href: instance.href,
              type: instance.type,
              id: instance.id
            };
            data[mapping.option_attr] = destination;
            modelInstance = new Model(data);
            defer.push(modelInstance.save());
          }.bind(this));

          $.when.apply($, defer)
            .fail(function (response, message) {
              $('body').trigger('ajax:flash', {error: message});
            })
            .always(function () {
              this.viewModel.attr('mapper.is_saving', false);
              this.closeModal();
            }.bind(this))
            .done(function () {
              if (instance && instance.dispatch) {
                instance.dispatch('refreshInstance');
              }
              // This Method should be modified to event
              GGRC.Utils.CurrentPage.refreshCounts();

              _.each($('sub-tree-wrapper'), function (wrapper) {
                var vm = $(wrapper).viewModel();

                if (vm.attr('parent') === instance) {
                  if (vm.attr('isOpen') && vm.attr('dataIsReady')) {
                    vm.loadItems();
                  } else {
                    // remove old data
                    // new data will be loaded after sub-tree is expanded
                    vm.attr('dataIsReady', null);
                  }

                  return false;
                }
              });
            });
        }.bind(this));
      },
      setModel: function () {
        var type = this.viewModel.attr('mapper.type');

        this.viewModel.attr(
          'mapper.model', this.viewModel.mapper.modelFromType(type));
      },
      '{mapper} type': function () {
        var mapper = this.viewModel.attr('mapper');
        mapper.attr('filter', '');
        mapper.attr('afterSearch', false);
        // Edge case for objects that are not in Snapshot scope
        if (!GGRC.Utils.Snapshots.isInScopeModel(
          mapper.attr('object'))) {
          mapper.attr('relevant').replace([]);
        }
        this.setModel();

        setTimeout(mapper.onSubmit.bind(mapper));
      }
    },

    helpers: {
      get_title: function (options) {
        var instance = this.attr('mapper.parentInstance');
        return (
          (instance && instance.title) ?
            instance.title :
            this.attr('mapper.object')
        );
      },
      get_object: function (options) {
        var type = CMS.Models[this.attr('mapper.type')];
        if (type && type.title_plural) {
          return type.title_plural;
        }
        return 'Objects';
      }
    }
  });
})(window.can, window.can.$);
