
/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: sasmita
    Maintained By: sasmita
*/
//----------------------------------------------------------------------------------------------
//Advanced search controller  extended from MultitypeObjectModalSelector
//
//----------------------------------------------------------------------------------------------



(function(can, $) {
  GGRC.Controllers.MultitypeObjectModalSelector("GGRC.Controllers.AdvancedSearchSelector", {
    defaults: {
          option_type_menu: null
        , option_descriptors: null
        , base_modal_view: "/static/mustache/search/advanced_search_base_modal.mustache"
        , option_items_view: "/static/mustache/search/advanced_search_option_items.mustache"
        , option_column_view: "/static/mustache/search/advanced_search_option_column.mustache"
        , option_type: null
        , option_model: null
        , object_model: null
        , join_model: null
    }
  }, {

  init_menu: function() {
      var menu
        , lookup = {
            governance: 0
          , business: 1
          , entities: 2
          };

      if (!this.options.option_type_menu) {
        menu = [
            { category: "Governance"
            , items: []
            }
          , { category: "Assets/Business"
            , items: []
            }
          , { category: "People/Groups"
            , items: []
            }
          ];
        can.each(this.options.option_descriptors, function(descriptor) {
          if ( descriptor.model.category === undefined ) {
            ;//do nothing
          }
          else {
            menu[lookup[descriptor.model.category] || 0].items.push({
                model_name: descriptor.model.shortName
              , model_display: descriptor.model.title_plural
            })
          }
        })

        this.options.option_type_menu = menu;
      }
      //hard code some of the submenu
      this.options.option_type_menu_2 = can.map([
            "Program","Regulation", "Policy", "Standard", "Contract", "Clause", "Section", "Objective", "Control",
            "Person", "System", "Process", "DataAsset", "Product", "Project", "Facility" , "Market"
            ],
            function(key) {
              return CMS.Models[key];
            }
      );
  }

  , set_option_descriptor: function(option_type) {
      var self = this
        , descriptor = this.options.option_descriptors[option_type]
        ;

      if (option_type == null || option_type == "undefined")
        return;

      this.constructor.last_selected_options_type = option_type;

      can.Model.startBatch();

      this.context.attr('selected_option_type', option_type);
      this.context.attr('option_column_view', descriptor.column_view);
      this.context.attr('option_detail_view', descriptor.detail_view);
      this.context.attr('option_descriptor', descriptor);
      this.context.selected_options = [];
      this.context.attr('selected_result', can.compute(function() {
        return self.get_result_for_option(self.context.attr('selected_options'));
      }));
      this.context.attr('related_table_plural', descriptor.related_table_plural);
      this.context.attr('related_table_singular', descriptor.related_table_singular);
      this.context.attr('related_model_singular', descriptor.related_model_singular);
      this.context.attr('new_object_title', descriptor.new_object_title);
      this.options.option_items_view = descriptor.items_view;
      this.options.option_model = descriptor.model;
      if (!this.options.option_search_term)
        this.options.option_search_term = '';

      can.Model.stopBatch();
      //Refresh_option_list is done from the search button
      //this.refresh_option_list();
  }


  , refresh_option_list: function() {
        var self = this
          , current_option_model = this.options.option_model
          , current_option_model_name = current_option_model.shortName
          , current_search_term = this.options.option_search_term
          , active_fn
          , draw_fn
          ;

        active_fn = function() {
          return self.element &&
                 self.options.option_model === current_option_model &&
                 self.options.option_search_term === current_search_term;
        };

        draw_fn = function(options) {
          self.insert_options(options);
        };

        self.option_list.replace([]);
        self.element.find('.option_column ul.new-tree').empty();

        var join_model = GGRC.Mappings.join_model_name_for(
              this.options.object_model, current_option_model_name);
        var permission_parms = { __permission_type: 'read' };
        if (current_option_model_name == 'Program') {
          permission_parms = {
            __permission_type: 'create'
            , __permission_model: join_model
          };
        }
        return GGRC.Models.Search
          .search_for_types(
              current_search_term || '',
              [current_option_model_name],
              permission_parms)
          .then(function(search_result) {
            var options = [],
              base_options ;

            if (active_fn()) {

              function match_object(result){
                var owner_val = $('input.search-by-owner').val(),
                    contact_val = $('input.search-by-contact').val();

                if(result.type == "Person") { return true; }

                if (self.context.owner && self.context.contact && owner_val !== "" && contact_val !== "") {
                  if (result.type == "Program") //FIXME after backend is done
                    return true;

                  return (result.owners[0] && (result.owners[0].id === self.context.owner.id) &&
                    result.contact && (result.contact.id === self.context.contact.id));
                }
                else if (self.context.owner && owner_val !== "") {
                  if (result.type == "Program") //FIXME after backend is done
                    return true;

                  return (result.owners[0] && owner_val !== "" && result.owners[0].id === self.context.owner.id);
                }
                else if (self.context.contact && contact_val !== "") {
                  return (result.contact && result.contact.id === self.context.contact.id);
                }
                else
                  return true;
              }

              base_options = search_result.getResultsForType(current_option_model_name);

              for (var i = 0 ; i < base_options.length; i++){
                if(match_object(base_options[i]))
                  options.push(base_options[i]);
              }

              self.option_list.push.apply(self.option_list, options);
              self._start_pager(options, 20, active_fn, draw_fn);
            }
          });
    }

    //Search button click
    , ".objectReview click": "triggerSearch"

    , "#search keyup": function(el, ev) {
        if (ev.which == 13) {
          this.triggerSearch();
        }
      }

    , triggerSearch: function(){

      // Remove Search Criteria text
      $('.results-wrap span.info').hide();
      var con = this.context;

      //Get the selected object value

      var selected = $("select.option-type-selector").val(),
        self = this,
        loader, custom_filter,
        term = $("#search").val() || "",
        re = new RegExp("^.*" + term + ".*","gi"),
        filters = [],
        cancel_filter;


      this.set_option_descriptor(selected);

      this.context.filter_list.each(function(filter_obj) {
        if(cancel_filter || !filter_obj.search_filter) {
          cancel_filter = true;
          return;
        }

        filters.push(
          // Must type filter here because the canonical mapping
          //  may be polymorphic.
          new GGRC.ListLoaders.TypeFilteredListLoader(
            GGRC.Mappings.get_canonical_mapping_name(filter_obj.search_filter.constructor.shortName, selected),
            [selected]
          ).attach(filter_obj.search_filter)
        );
      });
      if(cancel_filter) {
        //missing search term.
        return;
      }

      if (filters.length > 0) {
        //Object selected count and Add selected button should reset.
        //User need to make their selection again
        this.reset_selection_count();

        //if(filters.length === 1 && !term) {
        //  //don't bother making an intersecting filter when there's only one source
        //  loader = filters[0];
        //} else {
        //  // make an intersecting loader, that only shows the results that
        //  //  show up in all sources.
        //  if(term) {
        //    filters.push(new GGRC.ListLoaders.SearchListLoader(term, [selected]).attach(GGRC.current_user));
        //  }
        //  loader = new GGRC.ListLoaders.IntersectingListLoader(filters).attach();
        //}

        if (filters.length === 1) {
          loader = filters[0];
        }
        else {
          loader = new GGRC.ListLoaders.IntersectingListLoader(filters).attach();
        }

        custom_filter = new GGRC.ListLoaders.CustomFilteredListLoader(loader, function(result) {
          var model_type = result.instance.type,
            owner_val = $('input.search-by-owner').val(),
            contact_val = $('input.search-by-contact').val();

          switch(model_type){

            case "Person": //check for only search text, not owner or contact
              if (term) { return (result.instance.name.match(re)); }
              else { return true; }

            case "Program": //Fixme, Currently Program is not filtered by owner
              if ( term && self.context.contact && contact_val !== "" ) {
                return (result.instance.title.match(re) &&
                  result.instance.contact && result.instance.contact.id === self.context.contact.id);
              }
              else if (self.context.contact && contact_val !== "" ) {
                return ( result.instance.contact && result.instance.contact.id === self.context.contact.id);
              }
              else if(term) { return (result.instance.title.match(re)); }
              else { return true; }

            default:
              if (term && self.context.owner && self.context.contact && owner_val !== "" && contact_val !== "") {
                return (result.instance.title.match(re) &&
                  result.instance.owners[0] && (result.instance.owners[0].id === self.context.owner.id) &&
                  result.instance.contact && (result.instance.contact.id === self.context.contact.id));
              }
              else if( self.context.owner && self.context.contact && owner_val !== "" && contact_val !== ""){
                return ( result.instance.owners[0] && (result.instance.owners[0].id === self.context.owner.id) &&
                  result.instance.contact && (result.instance.contact.id === self.context.contact.id));
              }
              else if (term && self.context.owner && owner_val !== "") {
                return (result.instance.title.match(re) &&
                  result.instance.owners[0] && (result.instance.owners[0].id === self.context.owner.id));
              }
              else if (self.context.owner && owner_val !== "") {
                return (result.instance.owners[0] && (result.instance.owners[0].id === self.context.owner.id));
              }
              else if (term && self.context.contact && contact_val !== "") {
                return (result.instance.title.match(re) &&
                  result.instance.contact && (result.instance.contact.id === self.context.contact.id));
              }
              else if (self.context.contact && contact_val !== "") {
                return ( result.instance.contact && (result.instance.contact.id === self.context.contact.id));
              }
              else {
                return true;
              }
          }; //end switch
        }).attach(CMS.Models.get_instance(GGRC.current_user));

        this.last_loader = loader;
        this.last_custom_filter = custom_filter;
        self.option_list.replace([]);
        self.element.find('.option_column ul.new-tree').empty();
        custom_filter.refresh_instances().then(function(options) {
          var active_fn = function() {
            return self.element &&
                   self.last_custom_filter === custom_filter;
          };

          var draw_fn = function(options) {
            self.insert_options(options);
          };
          self.option_list.push.apply(self.option_list, options);
          self._start_pager(can.map(options, function(op) {
              return op.instance;
            }), 20, active_fn, draw_fn);
        });
      } else {
        //Object selected count and Add selected button should reset.
        //User need to make their selection again
        this.reset_selection_count();

        // With no mappings specified, just do a general search
        //  on the type selected.
        this.last_loader = null;
        this.options.option_search_term = term;
        this.refresh_option_list();
        this.constructor.last_option_search_term = term;
      }
    }

    , autocomplete_select : function(el, ev, ui) {
      setTimeout(function(){
        el.val(ui.item.name || ui.item.email || ui.item.title, ui.item);
        el.trigger('change');
      }, 0);
      this.context.attr(el.attr("name"), ui.item);
    }

  });

  search_descriptor_view_option = {
    "Person": {
        column_view : GGRC.mustache_path + "/search/advanced_search_option_column.mustache",
        items_view  : GGRC.mustache_path + "/search/advanced_search_people_items.mustache"
    }
  }

  function get_search_multitype_option_set(object_model_name, option_model_name, data, column_view, item_view) {

    var join_descriptors = null
      , option_descriptors = {}
      , option_set = {
            object_model: object_model_name
        }
      , exclude_option_types = data.exclude_option_types ? data.exclude_option_types.split(",") : []
      ;

    if (!option_model_name) {
      join_descriptors =
        GGRC.Mappings.get_canonical_mappings_for(object_model_name);
    } else {
      join_descriptors = {};
      join_descriptors[option_model_name] = GGRC.Mappings.get_canonical_mapping(object_model_name, option_model_name);
    }

    can.each(join_descriptors, function(descriptor, far_model_name) {
      var option_model_name = descriptor.option_model_name || far_model_name;
      var extra_options = search_descriptor_view_option[option_model_name];


      //  If we have duplicate options, we want to use the first, so return
      //    early.
      //  Also return now if the descriptor is explicitly excluded from the
      //    set of descriptors for this modal.
      if (option_descriptors[option_model_name]
          || ~can.inArray(option_model_name, exclude_option_types)
          //  For some recently-added join settings, there is no join model, so
          //  short-circuit
          || !descriptor.model_name
          || !(descriptor instanceof GGRC.ListLoaders.ProxyListLoader))
        return;


      if (!option_set.default_option_descriptor)
        option_set.default_option_descriptor = "Program";

      if (!extra_options){
        extra_options = {
            column_view : column_view
          , items_view  : item_view
        }
      }

      option_descriptors[option_model_name] =
        ModalOptionDescriptor.from_join_model(
            descriptor.model_name
          , descriptor.option_attr
          , option_model_name
          , extra_options);

    });

    //Fixme later , temporary fix for missing objects
    var extra_options = {
            column_view : column_view
          , items_view  : item_view
    };
    option_descriptors["Clause"] = ModalOptionDescriptor.from_join_model("TaskGroupObject", "object", "Clause", extra_options );
    option_descriptors["Section"] = ModalOptionDescriptor.from_join_model("TaskGroupObject", "object", "Section", extra_options );

    option_set.option_descriptors = option_descriptors;
    return option_set;
  }


  $(function() {
    $('body').on('click', '[data-toggle="multitype-search-modal-selector"]', function(e) {
      var $this = $(this)
        , options
        , data_set = can.extend({}, $this.data())
        ;

      can.each($this.data(), function(v, k) {
        data_set[k.replace(/[A-Z]/g, function(s) { return "_" + s.toLowerCase(); })] = v; //this is just a mapping of keys to underscored keys
        if(!/[A-Z]/.test(k)) //if we haven't changed the key at all, don't delete the original
          delete data_set[k];
      });


      //set up the options for new multitype Object  modal
      var column_view = GGRC.mustache_path + "/search/advanced_search_option_column.mustache",
      item_view =  GGRC.mustache_path + "/search/advanced_search_option_items.mustache" ;

      data_set.join_object_type = "Program";
      options = get_search_multitype_option_set(
        data_set.join_object_type, data_set.join_option_type, data_set, column_view, item_view);


      //options.selected_object = CMS.Models.get_instance(
      //    data_set.join_object_type, data_set.join_object_id);

      //No need for the binding -------
      //options.binding = options.selected_object.get_binding(
      //    data_set.join_mapping)

      //The below line is not needed, verify and clean up
      //options.object_params = $this.data("object-params");

      e.preventDefault();

      // Trigger the controller
      //GGRC.Controllers.MultitypeObjectModalSelector.launch($this, options)
      //.on("opened closed", function(ev, data) {
      //  $this.trigger("modal:" + ev.type, data);
      //});
      GGRC.Controllers.AdvancedSearchSelector.launch($this, options);
      //.on("opened closed", function(ev, data) {
      //  $this.trigger("modal:" + ev.type, data);
      //});
    });
  });

})(window.can, window.can.$);
