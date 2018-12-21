/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Role from '../models/service-models/role';
import Person from '../models/business-models/person';
import UserRole from '../models/service-models/user-role';

/* Role Assignment Modal Selector
  *
  * parameters:
  *   Templates:
  *     base_modal_view:
  *     option_column_view:
  *     option_detail_view:
  *
  *   Models and Queries:
  *     option_model: The model being "selected" (the "many")
  *     join_model: The model representing the join table
  *
  *   Customizable text components:
  *     modal_title:
  */
const userRolesModalSelector = can.Control.extend({
  defaults: {
    base_modal_view:
      GGRC.mustache_path + '/people_roles/base_modal.mustache',
    option_column_view:
      GGRC.mustache_path + '/people_roles/option_column.mustache',
    object_detail_view:
      GGRC.mustache_path + '/people_roles/object_detail.mustache',

    option_model: Role,
    object_model: Person,
    join_model: UserRole,
    join_id_field: 'person_id',
    option_attr: 'role',
    join_attr: 'person',
    selected_id: null,
    modal_title: 'User Role Assignments',
  },

  launch: function ($trigger, options) {
    // Extract parameters from data attributes
    let href = $trigger.attr('data-href') || $trigger.attr('href');
    let modalId =
      'ajax-modal-' + href.replace(/[/?=&#%]/g, '-').replace(/^-/, '');
    let $target = $(
      '<div id="' + modalId + '" class="modal modal-selector hide"></div>'
    );

    $target.modal_form({}, $trigger);
    this.newInstance($target[0], $.extend({$trigger: $trigger}, options));
    return $target;
  },
}, {
  init: function () {
    this.object_list = new can.List();
    this.option_list = new can.List();
    this.join_list = new can.List();
    this.active_list = new can.List();

    this.init_context();
    this.init_bindings();
    this.init_view();
    this.init_data();
  },

  '.option_column li click': 'select_option',
  '.confirm-buttons a.btn:not(.disabled) click': 'change_option',

  init_bindings: function () {
    this.join_list.bind('change', this.proxy('update_active_list'));
    this.context.bind('selected_object', this.proxy('refresh_join_list'));
    this.option_list.bind('change', this.proxy('update_option_radios'));
  },

  init_view: function () {
    let self = this;
    let deferred = $.Deferred();

    can.view(
      this.options.base_modal_view,
      this.context,
      function (frag) {
        $(self.element).html(frag);
        deferred.resolve();
        self.element.trigger('loaded');
      });

    this.on(); // Start listening for events

    return deferred;
  },

  init_data: function () {
    return $.when(
      this.refresh_object_list(),
      this.refresh_option_list(),
      this.refresh_join_list()
    );
  },

  init_context: function () {
    if (!this.context) {
      this.context = new can.Map($.extend({
        objects: this.object_list,
        options: this.option_list,
        joins: this.join_list,
        actives: this.active_list,
        selected_object: null,
        selected_option: null,
      }, this.options));
    }
    return this.context;
  },

  update_active_list: function () {
    let self = this;

    self.active_list.replace(
      can.map(self.join_list, function (join) {
        return new can.Map({
          join: join,
        });
      }));
  },

  refresh_object_list: function () {
    let self = this;

    return this.options.object_model.findAll(
      $.extend({}, this.options.object_query),
      function (objects) {
        self.object_list.replace(objects);
        if (self.object_list.length === 1) {
          self.context.attr('selected_object', self.object_list[0]);
        }
      });
  },

  refresh_option_list: function () {
    let params = {
      scope__in: 'System,Admin',
    };

    return this.options.option_model.findAll(
      params,
      (options) => {
        options = can.makeArray(_.sortBy(options, 'role_order'));
        let description =
          'This role allows a user access to the MyWork dashboard and ' +
          'applications Help files.';

        options.unshift({
          name: 'No role',
          id: 0,
          description: description,
          scope: params.scope || 'System',
        });
        this.option_list.replace(options);
      });
  },

  refresh_join_list: function () {
    let self = this;
    let joinObject = this.get_join_object();
    let joinQuery = {};

    if (joinObject) {
      joinQuery[this.options.join_id_field] = this.get_join_object_id();

      return this.options.join_model.findAll(
        $.extend({}, joinQuery),
        function (joins) {
          self.join_list.replace(joins);
          self.update_option_radios();
        });
    }

    return $.Deferred().resolve();
  },

  update_option_radios: function () {
    let allowedIds = can.map(this.context.options, function (join) {
      return join.id;
    });
    if (!allowedIds.length) {
      return;
    }
    if (!this.join_list.length) {
      this.context.attr('selected_id', 0);
    }
    this.join_list.forEach(function (join) {
      let id = join[this.options.option_attr].id;
      if (allowedIds.indexOf(id) >= 0) {
        this.context.attr('selected_id', id);
      }
    }.bind(this));
  },

  select_option: function (el) {
    el.closest('.option_column').find('li').removeClass('selected');
    el.addClass('selected');
    this.context.attr('selected_option', el.data('option'));
  },

  change_option: function (el_, ev) {
    let self = this;
    let el = $('.people-selector').find('input[type=radio]:checked');
    let li = el.closest('li');
    let clickedOption = li.data('option') || {};
    let join;
    let deleteDfds;
    let alreadyExists = false;

    // Look for and remove the existing join.
    deleteDfds = $.map(li.parent().children(), function (el) {
      let $el = $(el);
      let option = $el.closest('li').data('option');
      let join = self.find_join(option.id);

      if (join && join.role.id === clickedOption.id) {
        // Don't delete the role we marked to add.
        alreadyExists = true;
        return;
      }
      if (join) {
        return join.refresh().then(function () {
          return join.destroy();
        }).then(function () {
          self.refresh_object_list();
        });
      }
    });

    // Create the new join (skipping "No Role" role, with id == 0)
    if (clickedOption.id > 0 && !alreadyExists) {
      $.when(...deleteDfds).then(function () {
        join = self.get_new_join(
          clickedOption.id,
          clickedOption.scope,
          clickedOption.constructor.shortName
        );
        join.save().then(function () {
          self.join_list.push(join);
          self.refresh_option_list();
          self.refresh_object_list();
        });
      });
    }
  },

  // HELPERS

  find_join: function (optionId) {
    return _.find(this.join_list, (join) => this.match_join(optionId, join));
  },

  match_join: function (optionId, join) {
    return (
      join[this.options.option_attr] &&
      join[this.options.option_attr].id === optionId
    );
  },

  get_new_join: function (optionId, optionScope, optionType) {
    let joinParams = {};
    joinParams[this.options.option_attr] = {};
    joinParams[this.options.option_attr].id = optionId;
    joinParams[this.options.option_attr].type = optionType;
    joinParams[this.options.join_attr] = {};
    joinParams[this.options.join_attr].id = this.get_join_object_id();
    joinParams[this.options.join_attr].type = this.get_join_object_type();

    $.extend(joinParams, this.options.extra_join_fields);
    if (optionScope === 'Admin') {
      joinParams.context = {id: 0, type: 'Context'};
    }
    return new (this.options.join_model)(joinParams);
  },

  get_join_object: function () {
    return this.context.attr('selected_object');
  },

  get_join_object_id: function () {
    return this.get_join_object().id;
  },

  get_join_object_type: function () {
    let joinObject = this.get_join_object();
    return (joinObject ? joinObject.constructor.shortName : null);
  },
});

function getOptionSet(name, data) {
  // Construct options for Authorizations selector
  let objectQuery = {};
  if (data.person_id) {
    objectQuery = {id: data.person_id};
  }

  return {
    object_query: objectQuery,
    extra_join_fields: {
      context: {id: null},
    },
  };
}

export {
  getOptionSet,
};

export default userRolesModalSelector;
