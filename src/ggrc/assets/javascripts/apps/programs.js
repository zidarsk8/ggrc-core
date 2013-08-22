/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require controllers/tree_view_controller
//= require controls/control
//= require controls/category

/*  RefreshQueue
 *
 *  enqueue(obj, force=false) -> queue or null
 *  trigger() -> Deferred
 */

can.Construct("ModelRefreshQueue", {
}, {
    init: function(model) {
      this.model = model;
      this.ids = [];
      this.deferred = new $.Deferred();
      this.triggered = false;
      this.completed = false;
      this.updated_at = Date.now();
    }

  , enqueue: function(id) {
      if (this.triggered)
        return null;
      else {
        if (this.ids.indexOf(id) === -1) {
          this.ids.push(id);
          this.updated_at = Date.now();
        }
        return this;
      }
    }

  , trigger: function() {
      var self = this;
      if (!this.triggered) {
        this.triggered = true;
        if (this.ids.length > 0)
          this.model.findAll({ id__in: this.ids.join(",") }).then(function() {
            self.completed = true;
            self.deferred.resolve();
          });
        else {
          this.completed = true;
          this.deferred.resolve();
        }
      }
      return this.deferred;
    }

  , trigger_with_debounce: function(delay) {
      var ms_to_wait = (delay || 0) + this.updated_at - Date.now();

      if (!this.triggered) {
        if (ms_to_wait < 0)
          this.trigger();
        else
          setTimeout(this.proxy("trigger_with_debounce", delay), ms_to_wait);
      }

      return this.deferred;
    }
});

can.Construct("RefreshQueueManager", {
}, {
    init: function() {
      this.null_queue = new ModelRefreshQueue(null);
      this.queues = [];
    }

  , enqueue: function(obj, force) {
      var self = this
        , model = obj.constructor
        , model_name = model.shortName
        , found_queue = null
        , id = obj.id
        ;

      if (!force)
        // Check if the ID is already contained in another queue
        can.each(this.queues, function(queue) {
          if (!found_queue
              && queue.model === model && queue.ids.indexOf(id) > -1)
            found_queue = queue;
        });

      if (!found_queue) {
        can.each(this.queues, function(queue) {
          if (!found_queue
              && queue.model === model && !queue.triggered)
            found_queue = queue.enqueue(id);
        });
        if (!found_queue) {
          found_queue = new ModelRefreshQueue(model);
          this.queues.push(found_queue)
          found_queue.enqueue(id);
          found_queue.deferred.done(function() {
            var index = self.queues.indexOf(found_queue);
            if (index > -1)
              self.queues.splice(index, 1);
          });
        }
      }

      return found_queue;
    }
});

can.Construct("RefreshQueue", {
    refresh_queue_manager: new RefreshQueueManager()
}, {
    init: function() {
      this.objects = [];
      this.queues = [];
      this.deferred = new $.Deferred();
      this.triggered = false;
      this.completed = false;
    }

  , enqueue: function(obj, force) {
      if (!obj)
        return;
      if (this.triggered)
        return null;

      var model = obj.constructor
        , model_name = model.shortName
        ;

      this.objects.push(obj);
      if (force || !obj.selfLink) {
        queue = this.constructor.refresh_queue_manager.enqueue(obj, force);
        if (this.queues.indexOf(queue) === -1)
          this.queues.push(queue);
      }
      return this;
    }

  , trigger: function(delay) {
      var self = this
        , deferreds = []
        ;

      if (!delay)
        delay = 50;

      this.triggered = true;
      can.each(this.queues, function(queue) {
        deferreds.push(queue.trigger_with_debounce(50));
      });

      if (deferreds.length > 0)
        $.when.apply($, deferreds).then(function() {
          self.deferred.resolve(self.objects);
        });
      else
        return this.deferred.resolve(this.objects);

      return this.deferred;
    }
});


(function(can, $) {

if(!/^\/programs\/\d+/.test(window.location.pathname))
 return;

var program_id = /^\/programs\/(\d+)/.exec(window.location.pathname)[1];
var spin_opts = { position : "absolute", top : 100, left : 100, height : 50, width : 50 };

Permission = function(action, resource_type, context_id) {
  return {
    action: action,
    resource_type: resource_type,
    context_id: context_id
  };
};

$.extend(Permission, (function() {
  var _permission_match, _is_allowed, _admin_permission_for_context
    , ADMIN_PERMISSION = new Permission('__GGRC_ADMIN__', '__GGRC_ALL__', 0)
    ;

  _admin_permission_for_context = function(context_id) {
    return new Permission(
      ADMIN_PERMISSION.action, ADMIN_PERMISSION.resource_type, context_id);
  };

  _permission_match = function(permissions, permission) {
    var resource_types = permissions[permission.action] || {}
      , contexts = resource_types[permission.resource_type] || []
      ;

    return (contexts.indexOf(permission.context_id) > -1);
  };

  _is_allowed = function(permissions, permission) {
    if (!permissions)
      return false; //?
    if (permission.context_id == null)
      return true;
    if (_permission_match(permissions, permission))
      return true;
    if (_permission_match(permissions, ADMIN_PERMISSION))
      return true;
    if (_permission_match(permissions,
          _admin_permission_for_context(permission.context_id)))
      return true;
    return false;
  };

  is_allowed = function(action, resource_type, context_id) {
    return _is_allowed(
        GGRC.permissions, new Permission(action, resource_type, context_id));
  };

  return {
    _is_allowed: _is_allowed,
    is_allowed: is_allowed,
  };
})());

function collated_user_roles_by_person(user_roles) {
  var person_roles = new can.Observe.List([])
    , refresh_queue = new RefreshQueue()
    ;

  function insert_user_role(user_role) {
    var found = false;
    can.each(person_roles, function(data, index) {
      if (user_role.person.id == data.person.id) {
        person_roles.attr(index).attr('roles').push(user_role.role);
        refresh_queue.enqueue(user_role.role);
        found = true;
      }
    });
    if (!found) {
      person_roles.push({
        person: user_role.person,
        roles: [user_role.role]
      });
      refresh_queue.enqueue(user_role.person);
      refresh_queue.enqueue(user_role.role);
    }
  }

  function remove_user_role(user_role) {
    var roles, role_index
      , person_index_to_remove = null
      ;

    can.each(person_roles, function(data, index) {
      if (user_role.person.id == data.person.id) {
        roles = person_roles.attr(index).attr('roles');
        role_index = roles.indexOf(user_role.role);
        if (role_index > -1) {
          roles.splice(role_index, 1);
          if (roles.length == 0)
            person_index_to_remove = index;
        }
      }
    });
    if (person_index_to_remove)
      person_roles.splice(person_index_to_remove, 1);
  }

  CMS.Models.UserRole.bind("created", function(ev, user_role) {
    if (user_role.constructor == CMS.Models.UserRole)
      insert_user_role(user_role);
  });
  CMS.Models.UserRole.bind("destroyed", function(ev, user_role) {
    if (user_role.constructor == CMS.Models.UserRole)
      remove_user_role(user_role);
  });

  can.each(user_roles.reverse(), function(user_role) {
    insert_user_role(user_role);
  });

  return refresh_queue.trigger().then(function() { return person_roles });
}

function authorizations_list_loader() {
  var instance = GGRC.make_model_instance(GGRC.page_object)
    , context_id = instance.context && instance.context.id
    ;

  return CMS.Models.UserRole
    .findAll({ context_id: context_id })
    .then(collated_user_roles_by_person);
}

function should_show_authorizations() {
  var instance = GGRC.make_model_instance(GGRC.page_object)
    , context_id = instance.context && instance.context.id
    ;

  return (context_id
      && Permission.is_allowed('read', 'Role', 1)
      && Permission.is_allowed('read', 'UserRole', context_id)
      && Permission.is_allowed('create', 'UserRole', context_id)
      && Permission.is_allowed('update', 'UserRole', context_id)
      && Permission.is_allowed('delete', 'UserRole', context_id));
}

$(function() {

  can.Construct("GGRC.ListLoaders.MultiList", {
  }, {
      init: function(loaders) {
        this.list = new can.Observe.List;
        this.loaders = loads;
      }

    , refresh_list: function() {
      }
  });

  can.Construct("GGRC.ListLoaders.List", {
      insert_object: function(list, instance_mappings) {
        var i
          , entry
          , found = false
          ;

        for (i=0; i<list.length; i++) {
          entry = list[i];
          if (entry.instance === instance_mappings.instance) {
            // Cannot use 'concat', since can.Observe.List.concat will serialize()
            // list entries, which breaks 'instanceof'.
            entry.mappings.push.apply(entry.mappings, instance_mappings.mappings);
            //entry.mappings = entry.mappings.concat(instance_mappings.mappings);
            found = true;
            break;
          }
        }
        if (!found)
          list.push(instance_mappings);
      }

    , remove_object_via_mapping: function(list, mapping) {
        var i
          , j
          , entry
          , mappings
          , found = false
          ;

        for (i=0; i<list.length; i++) {
          mappings = list[i].mappings;
          for (j=0; j<mappings.length; j++) {
            if (mappings[j] === mapping) {
              mappings.splice(j, 1);
              j--;
            }
          }
          if (mappings.length == 0) {
            list.splice(i, 1);
            i--;
          }
        }
      }
  }, {
      init: function(options) {
        $.extend(this, options);
        if (!this.list)
          this.list = new can.Observe.List();
        this.refresh_queue = new RefreshQueue();
        this.init_bindings();
      }

    , init_bindings: function() {
        var self = this;

        this.mapping_model.bind("created", function(ev, mapping) {
          if (mapping instanceof self.mapping_model
              && (!self.source_value
                  || mapping[self.mapping_source_attr] == self.source_value)
              && mapping[self.mapping_target_attr] instanceof self.model)
            self.insert_object({
                instance: mapping[self.mapping_target_attr]
              , mappings: [mapping]
            });
        });

       this. mapping_model.bind("destroyed", function(ev, mapping) {
          if (mapping instanceof self.mapping_model
              && (!self.source_value
                  || mapping[self.mapping_source_attr] == self.source_value)
              && mapping[self.mapping_target_attr] instanceof self.model)
            self.remove_object_via_mapping(mapping);
        });
      }

    , init_list: function(mappings) {
        var self = this;

        can.each(mappings, function(mapping) {
          var instance = mapping[self.mapping_target_attr];
          if (instance) {
            self.refresh_queue.enqueue(instance);
            self.insert_object({
                instance: instance
              , mappings: [mapping]
            });
          }
        });

        return this.refresh_queue.trigger().then(function() {
          return self.list;
        });
      }

    , insert_object: function(result) {
        this.constructor.insert_object(this.list, result);
      }

    , remove_object_via_mapping: function(mapping) {
        this.constructor.remove_object_via_mapping(this.list, mapping);
      }
  });


  function init_directives_from_program(model, program) {
    var refresh_queue = new RefreshQueue();
    var loader = new GGRC.ListLoaders.List({
        model: model
      , mapping_model: CMS.Models.ProgramDirective
      , mapping_target_attr: 'directive'
      , mapping_source_attr: 'program'
      , source_value: program
    });

    can.each(program.program_directives, function(mapping) {
      refresh_queue.enqueue(mapping);
    });

    return function() {
      return refresh_queue.trigger()
        .then(function(mappings) {
          var program_directives = can.map(mappings, function(mapping) {
            if (mapping.directive instanceof model)
              return mapping;
          });
          return loader.init_list(program_directives);
        });
    }
  }

  function init_objectives_from_object(object) {
    var $objectives_tree = $("#objectives .tree-structure").append(
      $(new Spinner().spin().el).css(spin_opts));

    var refresh_queue = new RefreshQueue()
      , results_list = new can.Observe.List();

    var loader1 = new GGRC.ListLoaders.List({
        list: results_list
      , model: CMS.Models.Objective
      , mapping_model: CMS.Models.ObjectObjective
      , mapping_target_attr: 'objective'
      , mapping_source_attr: 'objectiveable'
      , source_value: object
    });

    var loader2 = new GGRC.ListLoaders.List({
        list: results_list
      , model: CMS.Models.Objective
      , mapping_model: CMS.Models.SectionObjective
      , mapping_target_attr: 'objective'
      , mapping_source_attr: 'section'
      , source_value: null
    });

    can.each(object.object_objectives, function(object_objective) {
      refresh_queue.enqueue(object_objective);
    });

    var params = {
      "section.directive.program_directives.program_id":
          program_id
    };

    return $.when(
        refresh_queue.trigger().then(can.proxy(loader1, "init_list"))
      , CMS.Models.SectionObjective.findAll(params).then(can.proxy(loader2, "init_list"))
    ).then(function() {
      return results_list;
    });
  }

  function init_controls_from_object(object) {
    var $controls_tree = $("#controls .tree-structure").append(
      $(new Spinner().spin().el).css(spin_opts));

    var refresh_queue = new RefreshQueue()
      , results_list = new can.Observe.List();

    var loader = new GGRC.ListLoaders.List({
        list: results_list
      , model: CMS.Models.Control
      , mapping_model: CMS.Models.ProgramControl
      , mapping_target_attr: 'control'
      , mapping_source_attr: 'program'
      , source_value: object
    });

    can.each(object.program_controls, function(mapping) {
      refresh_queue.enqueue(mapping);
    });

    return refresh_queue.trigger().then(can.proxy(loader, "init_list"));
  }


  var page_model = GGRC.make_model_instance(GGRC.page_object)

  program_widget_descriptors = {
      authorizations: {
          widget_id: "authorizations"
        , widget_name: "Authorizations"
        , widget_icon: "authorization"
        , widget_guard: should_show_authorizations
        , extra_widget_actions_view: '/static/ggrc_basic_permissions/mustache/people_roles/authorizations_modal_actions.mustache'
        , content_controller: GGRC.Controllers.ListView
        , content_controller_options: {
              list_view: "/static/ggrc_basic_permissions/mustache/people_roles/authorizations_by_person_list.mustache"
            , list_loader: authorizations_list_loader
            }
        }

    , objectives: {
          widget_id: "objectives"
        , widget_name: "Mapped Objectives"
        , widget_icon: "objective"
        , widget_info : function() {
            var $objectArea = $(".object-area");
            if ( $objectArea.hasClass("dashboard-area") ) {
              return ""
            } else {
              return "Does not include mappings to Directives, Objectives and Controls"
            }
          }
        , widget_initial_content: '<ul class="tree-structure new-tree"></ul>'
        , content_controller: CMS.Controllers.TreeView
        , content_controller_selector: "ul"
        , content_controller_options: {
              model : CMS.Models.Objective
            , list_loader : init_objectives_from_object
            , list_view : GGRC.mustache_path + "/objectives/tree.mustache"
            , parent_instance : page_model
            }
        }

    , controls: {
          widget_id: "controls"
        , widget_name: "Mapped Controls"
        , widget_icon: "control"
        , widget_info : function() {
            var $objectArea = $(".object-area");
            if ( $objectArea.hasClass("dashboard-area") ) {
              return ""
            } else {
              return "Does not include mappings to Directives, Objectives and Controls"
            }
          }
        , widget_initial_content: '<ul class="tree-structure new-tree"></ul>'
        , content_controller: CMS.Controllers.TreeView
        , content_controller_selector: "ul"
        , content_controller_options: {
              model : CMS.Models.Control
            , list_loader : init_controls_from_object
            , list_view : GGRC.mustache_path + "/controls/tree.mustache"
            , parent_instance : page_model
            }
        }
  };

  var models_by_kind = {
      contracts : CMS.Models.Contract
    , policies : CMS.Models.Policy
    , regulations : CMS.Models.Regulation
  };

  function sort_sections(sections) {
    return can.makeArray(sections).sort(window.natural_comparator);
  }

  can.each(models_by_kind, function(model, table_plural) {
    program_widget_descriptors[table_plural] = {
        widget_id: table_plural
      , widget_name: "Mapped " + model.title_plural
      , widget_icon: model.table_singular
      , widget_initial_content: '<ul class="tree-structure new-tree"></ul>'
      , content_controller: CMS.Controllers.TreeView
      , content_controller_selector: "ul"
      , content_controller_options: {
            model : model
          , list_loader : init_directives_from_program(model, page_model)
          , list_view : GGRC.mustache_path + "/directives/tree.mustache"
          , parent_instance : page_model
          , child_options : [{
              model : CMS.Models.Section
            , parent_find_param : "directive.id"
            , fetch_post_process : sort_sections
          }]
        }
    }
  });


  if (/programs\/\d+/.test(window.location)) {
    var widget_ids = [
            'regulations', 'policies', 'contracts'
          , 'controls', 'objectives', 'authorizations'
        ]

    if (!GGRC.extra_widget_descriptors)
      GGRC.extra_widget_descriptors = {};
    $.extend(GGRC.extra_widget_descriptors, program_widget_descriptors);

    if (!GGRC.extra_default_widgets)
      GGRC.extra_default_widgets = [];
    GGRC.extra_default_widgets.push.apply(
        GGRC.extra_default_widgets, widget_ids);
  }

});

})(window.can, window.can.$);
