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

var RefreshQueue = function() {
  var refresh_types_ids = {}
    , refresh_types_models = {}
    ;

  return {
    enqueue: function(obj, force) {
      var model = obj.constructor
        , model_name = model.shortName
        ;

      if (force || !obj.selfLink) {
        refresh_types_models[model_name] = model;
        refresh_types_ids[model_name] = refresh_types_ids[model_name] || [];
        if (refresh_types_ids[model_name].indexOf(obj.id) == -1)
          refresh_types_ids[model_name].push(obj.id);
      }
    },

    trigger: function() {
      var dfds = []
        , this_refresh_types_ids = refresh_types_ids
        , this_refresh_types_models = refresh_types_models
        ;

      refresh_types_ids = {};
      refresh_types_models = {};

      can.each(this_refresh_types_ids, function(ids, model_name) {
        var model = this_refresh_types_models[model_name];
        dfds.push(model.findAll({ id__in: ids.join(",") }));
      });

      if (dfds.length > 0)
        return $.when.apply($, dfds);
      else
        return (new $.Deferred()).resolve()
    }
  }
};

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

  is_allowed = function(permission) {
    return _is_allowed(GGRC.permissions, permission);
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
  //var context_id = GGRC.page_object.context && GGRC.page_object.context.id;
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
};

$(function() {

  if (/programs\/\d+/.test(window.location)) {
    var c = $('.cms_controllers_page_object').control(CMS.Controllers.PageObject);
    c.add_dashboard_widget_from_descriptor(
      program_widget_descriptors.authorizations);
  }

  var $controls_tree = $("#controls .tree-structure").append(
    $(new Spinner().spin().el).css(spin_opts));

  $.when(
    CMS.Models.Category.findTree()
    , CMS.Models.Control.findAll({ "directive.program_directives.program_id" : program_id })
    , CMS.Models.Control.findAll({ "program_controls.program_id" : program_id })
  ).done(function(cats, ctls) {
    var uncategorized = cats[cats.length - 1]
    , ctl_cache = {}
    , uncat_cache = {};
    // can.each(ctls, function(c) {
    //   uncat_cache[c.id] = ctl_cache[c.id] = c;
    // });
    // function link_controls(c) {
    //   //empty out the category controls that aren't part of the program
    //   c.controls.replace(can.map(c.controls, function(ctl) {
    //     delete uncat_cache[c.id];
    //     return ctl_cache[c.id];
    //   }));
    //   can.each(c.children, link_controls);
    // }
    // can.each(cats, link_controls);
    // can.each(Object.keys(uncat_cache), function(cid) {
    //     uncategorized.controls.push(uncat_cache[cid]);
    // });

    // $controls_tree.cms_controllers_tree_view({
    //   model : CMS.Models.Category
    //   , list : cats
    // });

    var page_model = GGRC.make_model_instance(GGRC.page_object)
    , combined_ctls = new CMS.Models.Control.List(can.unique(can.map(ctls, function(c) { return c; }).concat(can.map(page_model.controls, function(c) { return c; }))));

    $controls_tree.parent().ggrc_controllers_list_view({
      model : CMS.Models.Control
      , list : combined_ctls
      , list_loader : function() {
        return $.when(combined_ctls);
      }
    });

    page_model.controls.bind("change", function() {
      combined_ctls.replace(
        can.unique(
          can.map(ctls, function(c) { return c; })
          .concat(can.map(page_model.controls, function(c) { return c; }))
      ));
    });
  });
  /*
  CMS.Models.Control
    .findAll({ "directive.program_directives.program_id" : program_id })
    .done(function(s) {
      $controls_tree.cms_controllers_tree_view({
          model : CMS.Models.Control
        //, edit_sections : true
        , list : s
        , list_view : "/static/mustache/controls/tree.mustache"
        , parent_instance : GGRC.make_model_instance(GGRC.page_object)
      });
    });
  */

  var $objectives_tree = $("#objectives .tree-structure").append(
    $(new Spinner().spin().el).css(spin_opts));

  CMS.Models.Objective
    .findAll({ "section_objectives.section.directive.program_directives.program_id" : program_id })
    .done(function(s) {
      $objectives_tree.cms_controllers_tree_view({
          model : CMS.Models.Objective
        //, edit_sections : true
        , list : s
        , list_view : "/static/mustache/objectives/tree.mustache"
        , parent_instance : GGRC.make_model_instance(GGRC.page_object)
      });
    });

  var directives_by_type = {
    regulation : []
    , contract : []
    , policy : []
  };

  var models_by_kind = {
    regulation : CMS.Models.Regulation
    , contract : CMS.Models.Contract
    , policy : CMS.Models.Policy
  };

  var directive_dfds = [];

  can.each(directives_by_type, function(v, k) {
    var query_params = { "program_directives.program_id" : program_id };
    directive_dfds.push(models_by_kind[k].findAll(query_params)
    .done(function(directives) {
      directives_by_type[k] = directives;
    }));
  });

  var $sections_tree = $("#directives .tree-structure").append($(new Spinner().spin().el).css(spin_opts));
  $.when.apply(
    $
    , directive_dfds
  ).done(function(r, p, c) {
    var d = new can.Observe.List(r.concat(p).concat(c));

    CMS.Models.ProgramDirective.bind("created", function(ev, instance) {
      if (instance instanceof CMS.Models.ProgramDirective
          && instance.program.id == program_id)
        d.push(instance.directive);
    });

    CMS.Models.ProgramDirective.bind("destroyed", function(ev, instance) {
      var index;
      if (instance instanceof CMS.Models.ProgramDirective
          && instance.program.id == program_id) {
        index = d.indexOf(instance.directive);
        if (index > -1)
          d.splice(index, 1);
      }
    });

    $sections_tree.cms_controllers_tree_view({
      model : CMS.Models.Directive
      , parent_instance : GGRC.make_model_instance(GGRC.page_object)
      , list : d
      , list_view : "/static/mustache/directives/tree.mustache"
      , child_options : [{
        model : CMS.Models.Section
        , parent_find_param : "directive.id"
        //, find_params : { "parent_id__null" : true }
      }]
    });
  });

  $(document.body).on("modal:success", "a[href^='/controls/new']", function(ev, data) {
    var c = new CMS.Models.Control(data);
    $("a[href='#controls']").click();
      can.each(c.category_ids.length ? c.category_ids : [-1], function(catid) {
        $controls_tree.find("[data-object-id=" + catid + "] > .item-content > ul[data-object-type=control]").trigger("newChild", c);
      });
  });

  $(document.body).on("modal:relationshipcreated modal:relationshipdestroyed", ".add-new-item a", function(ev, data) {
    $sections_tree
    .trigger(ev.type === "modal:relationshipcreated" ? "newChild" : "removeChild", data.directive || CMS.Models.Directive.findInCacheById(data.directive_id));
  });

});

})(window.can, window.can.$);
