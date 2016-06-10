/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/
(function ($) {
  'use strict';
  var MAX_RESULTS = 20;
  var SEARCH_DEBOUNCE = 50;

  $.widget('ggrc.autocomplete', $.ui.autocomplete, {
    options: {
      // Ensure that the input.change event still occurs
      change: function (event, ui) {
        if (!$(event.target).parents(document.body).length) {
          console.warn('autocomplete menu change event is coming from detached nodes');
        }
        $(event.target).trigger('change');
      },
      minLength: 0,
      source: _.debounce(function (request, response) {
        // Search based on the term
        var query = request.term || '';
        var queue = new RefreshQueue();
        var isNextPage = _.isNumber(request.start);
        var dfd;

        if (query.indexOf('@') > -1) {
          query = '"' + query + '"';
        }

        this.last_request = request;
        if (isNextPage) {
          dfd = $.when(this.last_stubs);
        } else {
          request.start = 0;
          dfd = this.options.source_for_refreshable_objects.call(this, request);
        }

        dfd.then(function (objects) {
          this.last_stubs = objects;
          can.each(objects.slice(request.start, request.start + MAX_RESULTS), function (object) {
            queue.enqueue(object);
          });
          queue.trigger().then(function (objs) {
            objs = this.options.apply_filter(objs, request);
            if (objs.length || isNextPage) {
              // Envelope the object to not break model instance due to
              // shallow copy done by jQuery in `response()`
              objs = can.map(objs, function (obj) {
                return {
                  item: obj
                };
              });
              response(objs);
            } else {
              // show the no-results option iff no results come through here,
              //  and not merely showing paging.
              this._suggest([]);
              this._trigger('open');
            }
          }.bind(this));
        }.bind(this));

        if (this.options.controller) {
          this.options.controller.bindXHRToButton(dfd,
            $(this.element), null, false);
        }
      }, SEARCH_DEBOUNCE),

      apply_filter: function (objects) {
        return objects;
      },

      source_for_refreshable_objects: function (request) {
        var that = this;

        if (this.options.searchlist) {
          this.options.searchlist.then(function () {
            var filteredList = [];
            return $.map(arguments, function (item) {
              var searchAttr;
              var term;
              if (!item) {
                return;
              }
              searchAttr = item.title || '';
              term = request.term.toLowerCase();

              // Filter out duplicates:
              if (filteredList.indexOf(item._cid) > -1) {
                return;
              }
              filteredList.push(item._cid);

              // Perform search based on term:
              if (searchAttr.toLowerCase().indexOf(term) === -1) {
                return;
              }
              return item;
            });
          });
          return this.options.searchlist;
        }

        return GGRC.Models.Search.search_for_types(
          request.term || '',
          this.options.searchtypes,
          this.options.search_params
        )
        .then(function (searchResult) {
          var objects = [];

          can.each(that.options.searchtypes, function (searchtype) {
            objects.push.apply(objects,
              searchResult.getResultsForType(searchtype));
          });
          return objects;
        });
      },

      select: function (ev, ui) {
        var original_event;
        var $this = $(this);
        var widgetName = $this.data('autocomplete-widget-name');
        var ctl = $this.data(widgetName).options.controller;
        var widget_name;

        if (ui.item) {
          $this.trigger('autocomplete:select', [ui]);
          if (ctl) {
            if (ctl.scope && ctl.scope.autocomplete_select) {
              return ctl.scope.autocomplete_select($this, ev, ui);
            } else if (ctl.autocomplete_select) {
              return ctl.autocomplete_select($this, ev, ui);
            }
          }
        } else {
          original_event = ev;
          $(document.body)
            .off('.autocomplete')
            .one('modal:success.autocomplete', function (_ev, new_obj) {
              if (ctl) {
                if (ctl.scope && ctl.scope.autocomplete_select) {
                  return ctl.scope.autocomplete_select(
                    $this, original_event, {item: new_obj});
                } else if (ctl.autocomplete_select) {
                  return ctl.autocomplete_select(
                    $this, original_event, {item: new_obj});
                }
              }
              $this.trigger('autocomplete:select', [{
                item: new_obj
              }]);
              $this.trigger('modal:success', new_obj);
            })
            .one('hidden', function () {
              setTimeout(function () {
                $(this).off('.autocomplete');
              }, 100);
            });

          while ((original_event = original_event.originalEvent)) {
            if (original_event.type === 'keydown') {
              // This selection event was generated from a keydown, so click the add new link.
              widget_name = el.data('autocompleteWidgetName');
              el.data(widget_name).menu.active.find('a').click();
              break;
            }
          }
          return false;
        }
      },

      close: function () {
        this.scroll_op_in_progress = undefined;
      }
    },
    _create: function () {
      var that = this;
      var $that = $(this.element);
      var base_search = $that.data('lookup');
      var from_list = $that.data('from-list');
      var search_params = $that.data('params');
      var permission = $that.data('permission-type');
      var searchtypes;

      this._super.apply(this, arguments);
      this.options.search_params = {
        extra_params: search_params
      };
      if (permission) {
        this.options.search_params.__permission_type = permission;
      }

      $that.data('autocomplete-widget-name', this.widgetFullName);

      $that.focus(function () {
        $(this).data(that.widgetFullName).search($(this).val());
      });

      if (from_list) {
        this.options.searchlist = $.when.apply(this, $.map(from_list.list, function (item) {
          var props = base_search.trim().split('.');
          return item.instance.refresh_all.apply(item.instance, props);
        }));
      } else if (base_search) {
        base_search = base_search.trim();
        if (base_search.indexOf('__mappable') === 0 || base_search.indexOf('__all') === 0) {
          searchtypes = GGRC.Mappings.get_canonical_mappings_for(
            this.options.parent_instance.constructor.shortName
          );
          if (base_search.indexOf('__mappable') === 0) {
            searchtypes = can.map(searchtypes, function (mapping) {
              return mapping instanceof GGRC.ListLoaders.ProxyListLoader ? mapping : undefined;
            });
          }
          if (base_search.indexOf('_except:')) {
            can.each(base_search.substr(base_search.indexOf('_except:') + 8).split(','), function (remove) {
              delete searchtypes[remove];
            });
          }
          searchtypes = Object.keys(searchtypes);
        } else {
          searchtypes = base_search.split(',');
        }

        this.options.searchtypes = can.map(searchtypes, function (t) {
          return CMS.Models[t].model_singular;
        });
      }
    },

    _setup_menu_context: function (items) {
      var modelClass = this.element.data('lookup');
      var dataModel = this.element.data('model');
      var model = CMS.Models[modelClass || dataModel] ||
                  GGRC.Models[modelClass || dataModel];

      return {
        model_class: modelClass,
        model: model,
        // Reverse the enveloping we did 25 lines up
        items: can.map(items, function (item) {
          return item.item;
        })
      };
    },

    _renderMenu: function (ul, items) {
      var template = this.element.data('template');
      var context = new can.Observe(this._setup_menu_context(items));
      var model = context.model;
      var $ul = $(ul);

      if (!template) {
        if (model && GGRC.Templates[model.table_plural + '/autocomplete_result']) {
          template = '/' + model.table_plural + '/autocomplete_result.mustache';
        } else {
          template = '/base_objects/autocomplete_result.mustache';
        }
      }

      $ul.unbind('scrollNext')
        .bind('scrollNext', function (ev, data) {
          if (context.attr('scroll_op_in_progress') ||
              context.attr('oldLen') === context.attr('items').length) {
            return;
          }

          this.last_request = this.last_request || {};
          this.last_request.start = this.last_request.start || 0;
          this.last_request.start += MAX_RESULTS;
          context.attr('scroll_op_in_progress', true);
          context.attr('items_loading', true);
          this.source(this.last_request, function (items) {
            var listItems = context.attr('items');
            context.attr('oldLen', listItems.length);
            listItems.push.apply(listItems, can.map(items, function (item) {
              return item.item;
            }));
            context.removeAttr('items_loading');
            _.defer(function () {
              context.attr('scroll_op_in_progress', false);
            });
          });
        }.bind(this));

      can.view.render(GGRC.mustache_path + template,
        context, function (frag) {
          $ul.html(frag);
          $ul.cms_controllers_lhn_tooltips().cms_controllers_infinite_scroll();
          can.view.hookup(ul);
        });
    }
  });

  $.widget.bridge('ggrc_autocomplete', $.ggrc.autocomplete);
  $.widget('ggrc.mapping_autocomplete', $.ggrc.autocomplete, {
    options: {
      source_for_refreshable_objects: function (request) {
        var mapping = this.options.controller.options;

        if (mapping.scope) {
          mapping = mapping.scope.source_mapping;
        }

        return $.when(can.map(mapping || [], function (binding) {
          return binding.instance;
        }));
      },
      apply_filter: function (objects, request) {
        return can.map(objects, function (object) {
          if (!request.term || object.title && ~object.title.indexOf(request.term)) {
            return object;
          }
          return undefined;
        });
      }
    },
    _setup_menu_context: function (items) {
      return $.extend(this._super(items), {
        mapping: _.isUndefined(this.options.mapping) ? this.element.data('mapping') : this.options.mapping
      });
    }
  });

  $.widget.bridge('ggrc_mapping_autocomplete', $.ggrc.mapping_autocomplete);

  $.cms_autocomplete = function (el) {
    var ctl = this;
    // Add autocomplete to the owner field
    if (!el) {
      el = this.element.find('input[data-lookup]');
    } else {
      el = $(el);
    }
    el.filter("[name][name!='']")
      .ggrc_autocomplete({
        controller: ctl
      });
  };
})(jQuery);
