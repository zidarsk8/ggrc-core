(function(can, $) {

  /* Role Assignment Modal Selector
   *
   * parameters:
   *   Templates:
   *     base_modal_view:
   *     option_column_view:
   *     active_column_view:
   *     option_object_view:
   *     active_object_view:
   *     option_detail_view:
   *
   *   Models and Queries:
   *     option_model: The model being "selected" (the "many")
   *     option_query:
   *       Any additional parameters needed to restrict valid options
   *     active_query:
   *       Any additional parameters needed to restrict active options
   *     join_model: The model representing the join table
   *     join_query:
   *       Any additional parameters needed to restrict the join results
   *
   *   Customizable text components:
   *     modal_title:
   *     option_list_title:
   *     active_list_title:
   *     new_object_title:
   */

  can.Control("GGRC.Controllers.UserRolesModalSelector", {
    _templates: [
      "base_modal_view",
      "option_column_view",
      "active_column_view",
      "option_object_view",
      "active_object_view",
      "option_detail_view"
    ],

    defaults: {
      base_modal_view: GGRC.mustache_path + "/selectors/base_modal.mustache"
      , option_column_view: "/static/ggrc_basic_permissions/mustache/people_roles/option_column.mustache"
      , active_column_view: "/static/ggrc_basic_permissions/mustache/people_roles/active_column.mustache"
      , option_object_view: null
      , active_object_view: null
      , option_detail_view: "/static/ggrc_basic_permissions/mustache/people_roles/option_detail.mustache"

      , option_model: CMS.Models.Person
      , option_query: {}
      , active_query: {}
      , join_model: CMS.Models.UserRole
      , join_query: {}
      , join_object: null

      , modal_title: "User Role Assignments"
      , option_list_title: null
      , active_list_title: null
      , new_object_title: "Person"
    },

    launch: function($trigger, options) {
      // Extract parameters from data attributes

      var href = $trigger.attr('data-href') || $trigger.attr('href')
        , modal_id = 'ajax-modal-' + href.replace(/[\/\?=\&#%]/g, '-').replace(/^-/, '')
        , $target = $('<div id="' + modal_id + '" class="modal modal-selector fade hide"></div>')
        ;

      $target
        .modal_form({}, $trigger)
        .ggrc_controllers_user_roles_modal_selector($.extend(
          { $trigger: $trigger },
          options
        ));
    }
  }, {
    init: function() {
      debugger;

      var self = this
        , _data_changed = false
        ;

      this.option_list = new can.Observe.List();
      this.join_list = new can.Observe.List();
      this.active_list = new can.Observe.List();

      //this.join_list.bind("change", function() {
        //self.active_list.replace(
          //can.map(self.join_list, function(join) {
            //return new can.Observe({
              //option: CMS.Models.get_instance(
                //CMS.Models.get_link_type(join, self.options.option_attr),
                //join[self.options.option_id_field] || join[self.options.option_attr].id)
            //, join: join
            //});
          //}))
      //});

      //this.join_list.bind("change", function() {
        //// FIXME: This is to update the Document and Person lists when the
        ////   selected items change -- that list should be Can-ified.
        //var list_target = self.options.$trigger.data('list-target');
        //if (list_target)
          //$(list_target)
          //.tmpl_setitems(self.join_list)
          //.closest(":has(.grc-badge)")
          //.find(".grc-badge")
          //.text("(" + self.join_list.length + ")");
      //});

      $.when(
        this.post_init(),
        this.fetch_data()
      ).then(
        this.proxy('post_draw')
      );
    },

    fetch_data: function() {
      var self = this
        , join_query = can.extend({}, this.options.join_query)
        ;

      join_query[this.options.join_id_field] = this.get_join_object_id();
      if (this.options.join_type_field) {
        join_query[this.options.join_type_field] = this.get_join_object_type();
      }
      $.extend(join_query, this.options.extra_join_fields);

      // FIXME: Do this better
      cache_buster = { _: Date.now() }
      debugger;
      return $.when(
        this.options.option_model.findAll(
          $.extend({}, this.option_query, cache_buster),
          function(options) {
            self.option_list.replace(options)
          }),
        this.options.join_model.findAll(
          $.extend({}, join_query, cache_buster),
          function(joins) {
            debugger;
            can.each(joins, function(join) {
              join.attr('_removed', false);
            });
            self.join_list.replace(joins);
          })
        );
    },

    post_init: function() {
      var self = this
        , deferred = $.Deferred()
        ;

      this.context = new can.Observe($.extend({
        options: this.option_list,
        joins: this.join_list,
        actives: this.active_list,
        selected: null,
      }, this.options));

      can.view(
        this.options.base_modal_view,
        this.context,
        function(frag) {
          $(self.element).html(frag);
          deferred.resolve();
          //self.post_draw();
        });

      // Start listening for events
      this.on();

      return deferred;
    },

    post_draw: function() {
      var self = this
        , $option_list = $(this.element).find('.selector-list ul')
        ;

      this.join_list.forEach(function(join, index, list) {
        $option_list
          .find('li[data-id=' + join[self.options.option_attr].id + '] input[type=checkbox]')
          .prop('checked', true);
      });
    },

    // EVENTS

    " hide": function(el, ev) {
      // FIXME: This should only happen if there has been a change.
      //   - (actually, the "Related Widget" should just be Can-ified instead)
      var list_target = this.options.$trigger.data('list-target');
      if (list_target === "refresh" && this._data_changed)
        setTimeout(can.proxy(window.location.reload, window.location), 10);
    },

    ".option_column li click": function(el, ev) {
      var option = el.data('option')
        ;

      el.closest('.modal-content').find('li').each(function() {
        $(this).removeClass('selected');
      });
      el.addClass('selected');
      this.context.attr('selected', option);
    },

    ".option_column li input[type='checkbox'] change": function(el, ev) {
      var self = this
        , option = el.closest('li').data('option')
        , join = this.find_join(option.id)
        ;

      // FIXME: This is to trigger a page refresh only when data has changed
      //   - currently only used for the Related widget (see the " hide" event)
      this._data_changed = true;

      if (el.is(':checked')) {
        // First, check if join instance already exists
        if (join) {
          // Ensure '_removed' attribute is false
          join.attr('_removed', false);
        } else {
          // Otherwise, create it
          join = this.get_new_join(option.id, option.constructor.getRootModelName());
          join.save().then(function() {
            //join.refresh().then(function() {
              self.join_list.push(join);
            //});
          });
        }
      } else {
        // Check if instance is still selected
        if (join) {
          // Ensure '_removed' attribute is false
          if (join.isNew()) {
            // It was created, then removed, so remove from list
            join_index = this.join_list.indexOf(join);
            if (join_index >= 0) {
              this.join_list.splice(join_index, 1);
            }
          } else {
            // FIXME: The data should be updated in bulk, and only when "Save"
            //   is clicked.  Right now, it updates continuously.
            //join.attr('_removed', true);
            join.refresh().done(function() {
              join.destroy().then(function() {
                join_index = self.join_list.indexOf(join);
                if (join_index >= 0) {
                  self.join_list.splice(join_index, 1);
                }
              });
            });
          }
        }
      }
    },

    // HELPERS

    find_join: function(option_id) {
      var self = this
        ;

      return can.reduce(
        this.join_list,
        function(result, join) {
          if (result)
            return result;
          if (self.match_join(option_id, join))
            return join;
        },
        null);
    },

    match_join: function(option_id, join) {
      return join[this.options.option_id_field] == option_id ||
        (join[this.options.option_attr] 
         && join[this.options.option_attr].id == option_id)
    },

    get_new_join: function(option_id, option_type) {
      var join_params = {};
      join_params[this.options.option_id_field] = option_id;
      if (this.options.option_type_field) {
        join_params[this.options.option_type_field] = option_type;
      }
      join_params[this.options.join_id_field] = this.get_join_object_id();
      if (this.options.join_type_field) {
        join_params[this.options.join_type_field] = this.get_join_object_type();
      }
      // FIXME: context_id must get a real value
      $.extend(join_params, this.options.extra_join_fields, { context: { id: 0 } });
      return new (this.options.join_model)(join_params);
    },

    get_join_object_id: function() {
      return this.options.join_object.id;
    },

    get_join_object_type: function() {
      return this.options.join_object.constructor.getRootModelName();
    }
  });

  $(function() {
    $('body').on('click', '[data-toggle="user-roles-modal-selector"]', function(e) {
      debugger;
      var $this = $(this)
        , options = $this.data('modal-selector-options')
        , data_set = can.extend({}, $this.data())
        ;

      can.each($this.data(), function(v, k) {
        data_set[k.replace(/[A-Z]/g, function(s) { return "_" + s.toLowerCase(); })] = v; //this is just a mapping of keys to underscored keys
        if(!/[A-Z]/.test(k)) //if we haven't changed the key at all, don't delete the original
          delete data_set[k];
      });

      if (typeof(options) === "string")
        options = get_option_set(
          options
          , data_set
        );

      e.preventDefault();

      // Trigger the controller
      GGRC.Controllers.UserRolesModalSelector.launch($this, options);
    });
  });

  function get_option_set(name, data) {
    // Construct options for Person and Reference selectors
    return can.extend({
      option_column_view: "/static/ggrc_basic_permissions/mustache/people_roles/option_column.mustache"
      , active_column_view: "/static/ggrc_basic_permissions/mustache/people_roles/active_column.mustache"
      , option_detail_view: "/static/ggrc_basic_permissions/mustache/people_roles/option_detail.mustache"

      , new_object_title: "Person"
      , modal_title: "User Role Assignments"

      , related_model_singular: "Person"
      , related_table_plural: "people"
      , related_title_singular: "Person"
      , related_title_plural: "People"

      , option_model: CMS.Models.Person

      , join_model: CMS.Models.UserRole
      , option_attr: 'user'
      , join_attr: 'role'
      , option_id_field: 'email'
      , option_type_field: null
      , join_id_field: 'context_id'
      , join_type_field: null

      //, join_model: CMS.Models.ObjectPerson
      //, option_attr: 'person'
      //, join_attr: 'personable'
      //, option_id_field: 'person_id'
      //, option_type_field: null
      //, join_id_field: 'personable_id'
      //, join_type_field: 'personable_type'

      , join_object: GGRC.make_model_instance(GGRC.page_object).context
    }
    , {
      join_query : can.deparam(data.join_query)
    });
  }

  function get_page_object() {
    debugger;
    return GGRC.make_model_instance(GGRC.page_object);
  }

})(window.can, window.can.$);
debugger
