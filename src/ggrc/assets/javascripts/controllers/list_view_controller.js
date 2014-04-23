/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/
//= require tree-view-controller.js

(function(can, $) {

function model_list_loader(controller, extra_params) {
  var list = new can.Observe.List();

  function insert_instance(instance) {
    if (list.indexOf(instance) == -1) {
      list.unshift(instance);
    }
  }

  function remove_instance(instance) {
    var index = list.indexOf(instance);

    if (index > -1)
      list.splice(index, 1);
  }

  controller.options.model.bind("created", function(ev, instance) {
    if (instance.constructor == controller.options.model) {
      insert_instance(instance);
    }
  });

  return controller.options.model.findAll(extra_params).then(function(instances) {
    can.each(instances.reverse(), function(instance) {
      if (instance.constructor == controller.options.model)
        insert_instance(instance);
    });
    return list;
  });
}

CMS.Controllers.TreeLoader("GGRC.Controllers.ListView", {
  defaults : {
    is_related : false
    , model : null
    , extra_params : null
    , search_query : ""
    , search_params : null
    , parent_instance : null
    , object_type : null
    , parent_type : null
    , object_display : null
    , parent_display : null
    , header_view : null
    , list_view : "/static/mustache/dashboard/object_list.mustache"
    , list_objects : null
    , list_loader : null
    , tooltip_view : "/static/mustache/dashboard/object_tooltip.mustache"
  }
}, {

  init : function() {
    var that = this;
    !this.options.extra_params && (this.options.extra_params = {});
    !this.options.search_params && (this.options.search_params = {});
    this.options.state = new can.Observe();

    if(this.options.is_related) {
      if (!this.options.parent_instance)
        this.options.parent_instance = GGRC.page_instance();
      if(!this.options.parent_type)
        this.options.parent_type = this.options.parent_instance.constructor.shortName;

      if(this.options.parent_id == null)
        this.options.parent_id = this.options.parent_instance.id;
    } else {
      this.on();  //set up created listener for model
    }

    if(this.options.is_related) {
      if(this.options.object_type !== "system_process") {
        this.options.object_display =
          this.options.object_route.split("_").map(can.capitalize).join(" ");
      }
      this.options.object_type =
        this.options.object_type.split("_").map(can.capitalize).join("");
      this.options.parent_display =
        this.options.parent_type.split("_").map(can.capitalize).join(" ");
    }

    this.context = new can.Observe({
      // FIXME: Needed?  Default `pager` to avoid binding issues.
      pager: { has_next: function() { return false; } }
    });
    this.context.attr("has_next_page", can.compute(function() {
      var pager = that.context.attr("pager");
      return pager && pager.has_next && pager.has_next();
    }));
    this.context.attr("has_prev_page", can.compute(function() {
      var pager = that.context.attr("pager");
      return pager && pager.has_prev && pager.has_prev();
    }));
    this.context.attr(this.options);

    if(this.options.header_view) {
      can.view(this.options.header_view, $.when(this.context)).then(function(frag) {
        if (that.element) {
          that.element.prepend(frag);
        }
      });
    }

    if (this.options.list) {
      this.element.trigger("updateCount", this.options.list.length);
    } else {
      if (!this.options.list_loader) {
        if (this.options.is_related) {
          this.options.list_loader = related_model_list_loader;
        } else if (this.options.model.list_view_options.find_function) {
          var that = this;
          this.options.list_loader = function(controller) {
            var list = new can.Observe.List();

            function insert_instance(instance) {
              if (list.indexOf(instance) == -1) {
                list.unshift(instance);
              }
            }

            function remove_instance(instance) {
              var index = list.indexOf(instance);

              if (index > -1)
                list.splice(index, 1);
            }

            controller.options.model.bind("created", function(ev, instance) {
              if (instance.constructor == controller.options.model) {
                insert_instance(instance);
              }
            });

            var collection_name = that.options.model.root_collection+"_collection"
              , find_function = that.options.model.list_view_options.find_function
              , find_params = can.extend({}, that.options.extra_params, that.options.model.list_view_options.find_params || {})
              ;
            return that.options.model[find_function](find_params).then(function(result) {
              can.each(result[collection_name], function(instance) {
                if (instance.constructor == controller.options.model)
                  insert_instance(instance);
              });
              that.options.pager = result.paging;
              that.context.attr("pager", result.paging);
              return result[collection_name];
            });
          };
        } else {
          this.options.list_loader = model_list_loader;
        }
      }
      //this.fetch_list({});
    }
  }

  , prepare : function() {
    var that = this;
    this.element.trigger("updateCount", 0)

    this.options.list_loader(this, this.options.extra_params || {}).done(function(list) {
      that.element.trigger("updateCount", list.length)
    });

    return $.when();
  }

  , fetch_list : function(params) {
    // Assemble extra search params
    var extra_params = this.options.extra_params || {}
      , search_params = this.options.search_params
      , that = this
      , page
      ;

    this.element.trigger("loading");
    this.reset_sticky_clone();

    if(this.options.list)
      this.options.list.replace([]);

    if (search_params.search_ids || search_params.user_role_ids) {
      var model = this.options.model
        , ids = search_params.search_ids || search_params.user_role_ids || []
        , that = this
        , pager
        ;

      // If there is a search for both a query an user roles,
      // only use the ids in both lists.
      if (search_params.search_ids && search_params.user_role_ids) {
        var found = {};
        ids = [];
        can.each([].concat(search_params.search_ids, search_params.user_role_ids), function(id) {
          if (found[''+id]) {
            ids.push(id);
          }
          else {
            found[''+id] = true;
          }
        });
      }
      // Create a new pager class to paginate over the ids:
      pager = {
        count: 100
        , current: 0
        , total: ids.length
        , first: function(){
          pager.current = 0;
          return pager.fetch();
        }
        , prev: function(){
          pager.current--;
          return pager.fetch();
        }
        , next: function(){
          pager.current++;
          return pager.fetch();
        }
        , fetch: function(){
          var rq = new RefreshQueue();
          window.scrollTo(0, 0);
          can.each(ids.slice(pager.count*pager.current, pager.count*(pager.current+1)), function(id) {
            rq.enqueue(CMS.Models.get_instance(model.shortName, id));
          });
          return rq.trigger().then(function(instances) {
            that.context.attr('pager', that.options.pager);
            return new can.Observe.List(instances);
          }).then(that.proxy("draw_list"));
        }
        , has_next: function() { return pager.count*(pager.current+1) < ids.length; }
        , has_prev: function() { return pager.count*(pager.current) > 0; }
      };
      // Load the first page:
      page = pager.first();
      this.options.pager = pager;
      this.context.attr('pager', this.options.pager);
      this.element.trigger("updateCount", ids.length);
      return page;
    } else {
      return this.options.list_loader(this, extra_params).done(function(list) {
        that.element.trigger("updateCount", list.length);
      });
    }
  }

  , draw_list : function(list) {
    if (list && this.options.fetch_post_process) {
      list = this.options.fetch_post_process(list);
    }

    var that = this;
    if(list) {
      if(!this.options.list){
        this.options.list = new can.Observe.List();
        list.on('add', function(list, item, index){
          that.enqueue_items(item);
        }).on('remove', function(list, item, index){
          that.options.list.splice(index, 1);
          that.element.find('ul.tree-open').removeClass('tree-open');
        });
      }
      else{
        this.options.list.splice();
      }
      this.enqueue_items(list);
      this.on();
    }

    this.context.attr(this.options);
    this.update_count();
  }

  , init_view : function() {
    var that = this;
    return can.view(this.options.list_view, this.context, function(frag) {
      that.element.find('.spinner, .tree-structure').hide();
      that.element
        .append(frag)
        .trigger("loaded");
      that.options.state.attr('loading', false);
    });
  }

  , update_count: function() {
      if (this.element) {
        if (this.options.pager)
          this.element.trigger("updateCount", this.options.pager.total);
        else
          this.element.trigger("updateCount", this.options.list.length);
        this.element.trigger("widget_updated");
      }
    }
  , reset_search: function(el, ev){
      this.options.search_params = {};
      this.options.search_query = '';
      this.element.find('.search-filters').find('input[name=search], select[name=user_role]').val('');
      this.fetch_list().then(this.proxy("draw_list"));
  }
  , insert_items : function(items){
    this.options.list.push.apply(this.options.list, items);
  }
  , "{list} change": "update_count"
  , ".view-more-paging click" : function(el, ev) {
      var that = this
        , collection_name = that.options.model.root_collection+"_collection"
        , is_next = el.data('next')
        , can_load = is_next ? that.options.pager.has_next() : that.options.pager.has_prev()
        , load = is_next ? that.options.pager.next : that.options.pager.prev;
      that.options.list.replace([]);
      that.element.find('.spinner').show();
      if (can_load) {
        load().done(function(data) {
          that.element.find('.spinner').hide();
          if(typeof data === 'undefined') return;
          if (data[collection_name] && data[collection_name].length > 0) {
            that.enqueue_items(data[collection_name]);
          }
          that.options.pager = data.paging;
          that.context.attr("pager", data.paging);
        });
      }
    }
  , reset_sticky_clone : function(){
      this.element.find('.sticky-clone').remove();
      this.element.find('.advanced-filters').removeClass('sticky sticky-header').removeAttr('style');
      this.element.find('.tree-footer').removeClass('sticky sticky-footer').removeAttr('style').hide();
      this.element.find('.tree-footer').show();
    }

  , ".search-filters input[name=search] change" : function(el, ev) {
      var that = this;
      delete this.options.search_params.search_ids;
      this.options.search_query = el.val();
      GGRC.Models.Search.search_for_types(this.options.search_query, [this.options.model.model_singular], {}).then(function(results) {
        var ids = $.map(results.entries, function(person) { return person.id; });
        that.options.search_params.search_ids = ids;
        that.fetch_list();
      });
    }

  , ".search-filters select[name=user_role] change" : function(el, ev) {
      var that = this;
      delete this.options.search_params.user_role_ids;
      if (el.val()) {
        CMS.Models.UserRole.findAll({ role_id: el.val() }).then(function(user_roles) {
          var ids = $.map(user_roles, function(user_role) { return user_role.person.id; });
          that.options.search_params.user_role_ids = ids;
          that.fetch_list();
        });
      }
      else {
        this.fetch_list();
      }
    }

  , ".search-filters button[type=reset] click" : "reset_search"
  , ".btn-add modal:success" : "reset_search"
  }
);

})(this.can, this.can.$);
