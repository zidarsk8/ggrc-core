/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/

//= require can.jquery-all

(function(can, $) {

$(function() {
  if (!GGRC.page_object)
    return;

  var object_class = GGRC.infer_object_type(GGRC.page_object)
    , object_table = object_class.table_plural
    , object = GGRC.page_instance();

  if (!GGRC.widget_descriptors)
    GGRC.widget_descriptors = {};
  if (!GGRC.default_widgets)
    GGRC.default_widgets = [];


  //A widget descriptor has the minimum five properties:
  // widget_id:  the unique ID string for the widget
  // widget_name: the display title for the widget in the UI
  // widget_icon: the CSS class for the widget in the UI
  // content_controller: The controller class for the widget's content section
  // content_controller_options: options passed directly to the content controller; the
  //   precise options depend on the controller itself.  They usually require instance
  //   and/or model and some view.
  can.Construct("GGRC.WidgetDescriptor", {
    make_info_widget : function(instance, widget_view) {
      var default_info_widget_view = GGRC.mustache_path + "/base_objects/info.mustache";
      return new this({
        widget_id: "info",
        widget_name: function() {
          if (instance.constructor.title_singular === 'Person')
            return 'Info';
          else
            return instance.constructor.title_singular + " Info";
        },
        widget_icon: "grcicon-info",
        content_controller : GGRC.Controllers.InfoWidget,
        content_controller_options : {
          instance: instance,
          model: instance.constructor,
          widget_view: widget_view || default_info_widget_view
        }
      });
    },
    make_tree_view : function(instance, far_model, mapping, extenders) {
      var descriptor = {
        content_controller: CMS.Controllers.TreeView,
        content_controller_selector: "ul",
        widget_initial_content: '<ul class="tree-structure new-tree"></ul>',
        widget_id: far_model.table_singular,
        widget_guard: function(){
          if (far_model.title_plural === "Audits"
              && instance instanceof CMS.Models.Program){
            return "context" in instance && !!(instance.context.id);
          }
          return true;
        },
        widget_name: function() {
            var $objectArea = $(".object-area");
            if ( $objectArea.hasClass("dashboard-area") || instance.constructor.title_singular === "Person" ) {
              if (/dashboard/.test(window.location)) {
                return "My " + far_model.title_plural;
              } else {
                return far_model.title_plural;
              }
            } else if (far_model.title_plural === "Audits") {
              return "Mapped Audits";
            } else {
              return (far_model.title_plural === "References" ? "Linked " : "Mapped ") + far_model.title_plural;
            }
          }
        , widget_icon: far_model.table_singular
        , object_category: far_model.category || 'default'
        , model: far_model
        , content_controller_options: {
              child_options: []
            , draw_children: false
            , parent_instance: instance
            , model: far_model
            , list_loader: $.proxy(mapping, "refresh_list")
          }
      };

      $.extend.apply($, [true, descriptor].concat(extenders || []));

      return new this(descriptor);
    },
    newInstance : function(opts) {
      var ret;
      if(GGRC.widget_descriptors[opts.widget_id]) {
        if(GGRC.widget_descriptors[opts.widget_id] instanceof this) {
          $.extend(GGRC.widget_descriptors[opts.widget_id], opts);
        } else {
          ret = this._super.apply(this);
          $.extend(ret, GGRC.widget_descriptors[opts.widget_id], opts);
          GGRC.widget_descriptors[opts.widget_id] = ret;
        }
        return GGRC.widget_descriptors[opts.widget_id];
      } else {
        ret = this._super.apply(this, arguments);
        $.extend(ret, opts);
        GGRC.widget_descriptors[ret.widget_id] = ret;
        return ret;
      }
    }
  }, {
    register_as_default : function() {
      if(!~can.inArray(this.widget_id, GGRC.default_widgets)) {
        GGRC.default_widgets.push(this.widget_id);
      }
      return this;
    }
  });


  // Info widgets display the object information instead of listing connected 
  //  objects.
  var info_widget_views = {
      'programs': GGRC.mustache_path + "/programs/info.mustache"
    , 'people': GGRC.mustache_path + "/people/info.mustache"
    , 'policies': GGRC.mustache_path + "/policies/info.mustache"
    , 'sections': GGRC.mustache_path + "/sections/info.mustache"
    , 'objectives': GGRC.mustache_path + "/objectives/info.mustache"
    , 'controls': GGRC.mustache_path + "/controls/info.mustache"
    , 'systems': GGRC.mustache_path + "/systems/info.mustache"
    , 'processes': GGRC.mustache_path + "/processes/info.mustache"
    , 'products': GGRC.mustache_path + "/products/info.mustache"
  };
  GGRC.WidgetDescriptor.make_info_widget(object, info_widget_views[object_table]).register_as_default();

  function sort_sections(sections) {
    return can.makeArray(sections).sort(window.natural_comparator);
  }

  function apply_mixins(definitions) {
    var mappings = {};

    // Recursively handle mixins
    function reify_mixins(definition) {
      var final_definition = {};
      if (definition._mixins) {
        can.each(definition._mixins, function(mixin) {
          if (typeof(mixin) === "string") {
            // If string, recursive lookup
            if (!definitions[mixin])
              console.debug("Undefined mixin: " + mixin, definitions);
            else
              can.extend(final_definition, reify_mixins(definitions[mixin]));
          } else if (can.isFunction(mixin)) {
            // If function, call with current definition state
            mixin(final_definition);
          } else {
            // Otherwise, assume object and extend
            can.extend(final_definition, mixin);
          }
        });
      }
      can.extend(final_definition, definition);
      delete final_definition._mixins;
      return final_definition;
    }

    can.each(definitions, function(definition, name) {
      // Only output the mappings if it's a model, e.g., uppercase first letter
      if (name[0] === name[0].toUpperCase())
        mappings[name] = reify_mixins(definition);
    });

    return mappings;
  }

  var far_models = GGRC.JoinDescriptor
        .by_object_option_models[object.constructor.shortName]
    , model_widget_descriptors = {}
    , model_default_widgets = []

    // here we are going to define extra descriptor options, meaning that
    //  these will be used as extra options to create widgets on top of 

    , extra_descriptor_options = {
          all: {
              Person: {
                  widget_icon: 'grcicon-user-black'
              }
            , Document: {
                  widget_icon: 'grcicon-link'
              }
          }
        , Contract : {
            Clause: {
              widget_name : function() {
                var $objectArea = $(".object-area");
                if ( $objectArea.hasClass("dashboard-area") ) {
                  return "Clauses";
                } else {
                  return "Mapped Clauses";
                }
              }
            }
          }
      }
    // Prevent widget creation with <model_name>: false
    // e.g. to prevent ever creating People widget:
    //     { all : { Person: false }}
    // or to prevent creating People widget on Objective page:
    //     { Objective: { Person: false } }
    , overridden_models = {
          Program: {
            //  Objective: false
            //, Control: false
            //, Regulation: false
            //, Policy: false
            //, Standard: false
            //, Contract: false
          }
          , all : {
              Document : false
            , DocumentationResponse : false
            , InterviewResponse : false
            , PopulationSampleResponse : false
          }
      }

    , section_child_options = {
          model : CMS.Models.Section
        , mapping : "sections"
        , show_view : GGRC.mustache_path + "/sections/tree.mustache"
        , footer_view : GGRC.mustache_path + "/sections/tree_footer.mustache"
        , draw_children : true
      }

    , clause_child_options = {
          model: CMS.Models.Clause
        , mapping: "clauses"
        , show_view: GGRC.mustache_path + "/sections/tree.mustache"
        , footer_view: GGRC.mustache_path + "/sections/tree_footer.mustache"
        , draw_children: true
        }

    , extra_content_controller_options = apply_mixins({
          objectives: {
              Objective: {
                  mapping: "objectives"
                , draw_children: true
                , show_view: GGRC.mustache_path + "/objectives/tree.mustache"
                , footer_view: GGRC.mustache_path + "/objectives/tree_footer.mustache"
                }
            }
        , controls: {
              Control: {
                  mapping: "controls"
                , draw_children: true
                , show_view: GGRC.mustache_path + "/controls/tree.mustache"
                , footer_view: GGRC.mustache_path + "/controls/tree_footer.mustache"
                }
            }
        , business_objects: {
              DataAsset: {
                  mapping: "related_data_assets"
                }
            , Facility: {
                  mapping: "related_facilities"
                }
            , Market: {
                  mapping: "related_markets"
                }
            , OrgGroup: {
                  mapping: "related_org_groups"
                }
            , Process: {
                  mapping: "related_processes"
                }
            , Product: {
                  mapping: "related_products"
                }
            , Project: {
                  mapping: "related_projects"
                }
            , System: {
                  mapping: "related_systems"
                }
            , Document: {
                  mapping: "documents"
                }
            , Person: {
                  mapping: "people"
                }
            , Program: {
                  mapping: "programs"
                }
            }

        , governance_objects: {
              Regulation: {
                  mapping: "regulations"
                , draw_children: true
                , child_options: [section_child_options]
                , fetch_post_process: sort_sections
                , show_view: GGRC.mustache_path + "/directives/tree.mustache"
                , footer_view: GGRC.mustache_path + "/directives/tree_footer.mustache"
                }
            , Contract: {
                  mapping: "contracts"
                , draw_children: true
                , child_options: [clause_child_options]
                , fetch_post_process: sort_sections
                , show_view: GGRC.mustache_path + "/directives/tree.mustache"
                , footer_view: GGRC.mustache_path + "/directives/tree_footer.mustache"
                }
            , Policy: {
                  mapping: "policies"
                , draw_children: true
                , child_options: [section_child_options]
                , fetch_post_process: sort_sections
                , show_view: GGRC.mustache_path + "/directives/tree.mustache"
                , footer_view: GGRC.mustache_path + "/directives/tree_footer.mustache"
                }
            , Standard: {
                  mapping: "standards"
                , draw_children: true
                , child_options: [section_child_options]
                , fetch_post_process: sort_sections
                , show_view: GGRC.mustache_path + "/directives/tree.mustache"
                , footer_view: GGRC.mustache_path + "/directives/tree_footer.mustache"
                }
            , Control: {
                  mapping: "controls"
                }
            , Objective: {
                  mapping: "objectives"
                }
            }

        , Program: {
              _mixins: [
                  "governance_objects"
                , "objectives"
                , "controls"
                , "business_objects"
                ]

            , Audit: {
              mapping: "audits"
              , allow_mapping : true
              , draw_children : true
              , show_view : GGRC.mustache_path + "/audits/tree.mustache"
              , footer_view : GGRC.mustache_path + "/audits/tree_footer.mustache"
            }
          }

        , directive: {
              _mixins: [
                  "objectives"
                , "controls"
                , "business_objects"
                ]
            }

        , Regulation: {
              _mixins: ["directive"]
            , Section: section_child_options
            }
        , Standard: {
              _mixins: ["directive"]
            , Section: section_child_options
            }
        , Policy: {
              _mixins: ["directive"]
            , Section: section_child_options
            }
        , Contract: {
              _mixins: ["directive"]
            , Clause: clause_child_options
            }

        , extended_audits: {
            Audit: {
              mapping: "related_audits_via_related_responses"
              , allow_mapping : false
              , allow_creating : false
              , draw_children : true
              , show_view : GGRC.mustache_path + "/audits/tree.mustache"
              , footer_view : null
            }
          }

        , Clause: {
            _mixins: ["governance_objects", "business_objects", "extended_audits"]
          }
        , Objective: {
            _mixins: ["governance_objects", "business_objects", "extended_audits"]
          }
        , Control: {
            _mixins: ["governance_objects", "business_objects", "extended_audits"]
          }
        , DataAsset: {
            _mixins: ["governance_objects", "business_objects", "extended_audits"]
          }
        , Facility: {
            _mixins: ["governance_objects", "business_objects", "extended_audits"]
          }
        , Market: {
            _mixins: ["governance_objects", "business_objects", "extended_audits"]
          }
        , OrgGroup: {
            _mixins: ["governance_objects", "business_objects", "extended_audits"]
          }
        , Process: {
            _mixins: ["governance_objects", "business_objects", "extended_audits"]
          }
        , Product: {
            _mixins: ["governance_objects", "business_objects", "extended_audits"]
          }
        , Project: {
            _mixins: ["governance_objects", "business_objects", "extended_audits"]
          }
        , System: {
            _mixins: ["governance_objects", "business_objects", "extended_audits"]
          }
        , Document: {
            _mixins: ["governance_objects", "business_objects", "extended_audits"]
          }

        , Person : {
            // _mixins: ["extended_audits"]
             Program : {
                mapping: "extended_related_programs_via_search"
              , fetch_post_process: sort_sections
              }
            , Regulation: {
                mapping: "extended_related_regulations_via_search"
              , draw_children: true
              , child_options: [section_child_options]
              , fetch_post_process: sort_sections
              , show_view: GGRC.mustache_path + "/directives/tree.mustache"
              }
            , Contract: {
                mapping: "extended_related_contracts_via_search"
              , draw_children: true
              , child_options: [clause_child_options]
              , fetch_post_process: sort_sections
              , show_view: GGRC.mustache_path + "/directives/tree.mustache"
              }
            , Standard: {
                mapping: "extended_related_standards_via_search"
              , draw_children: true
              , child_options: [section_child_options]
              , fetch_post_process: sort_sections
              , show_view: GGRC.mustache_path + "/directives/tree.mustache"
              }
            , Policy: {
                mapping: "extended_related_policies_via_search"
              , draw_children: true
              , child_options: [section_child_options]
              , fetch_post_process: sort_sections
              , show_view: GGRC.mustache_path + "/directives/tree.mustache"
              }
            , Audit: {
                mapping: "extended_related_audits_via_search"
              , draw_children : true
              , show_view : GGRC.mustache_path + "/audits/tree.mustache"
              }
            , Section : {
                model : CMS.Models.Section
              , mapping : "extended_related_sections_via_search"
              , show_view : GGRC.mustache_path + "/sections/tree.mustache"
              , footer_view: GGRC.mustache_path + "/base_objects/tree_footer.mustache"
              , draw_children : true
              }
            , Clause : {
                model : CMS.Models.Clause
              , mapping : "extended_related_clauses_via_search"
              , show_view : GGRC.mustache_path + "/sections/tree.mustache"
              , footer_view: GGRC.mustache_path + "/base_objects/tree_footer.mustache"
              , draw_children : true
              }
            , Objective: {
                mapping: "extended_related_objectives_via_search"
              , draw_children: true
              , show_view: GGRC.mustache_path + "/objectives/tree.mustache"
              , footer_view: GGRC.mustache_path + "/base_objects/tree_footer.mustache"
              }
            , Control: {
                mapping: "extended_related_controls_via_search"
              , draw_children: true
              , show_view: GGRC.mustache_path + "/controls/tree.mustache"
              , footer_view: GGRC.mustache_path + "/base_objects/tree_footer.mustache"
              }
            , DataAsset: {
                mapping: "extended_related_data_assets_via_search"
              }
            , Facility: {
                mapping: "extended_related_facilities_via_search"
              }
            , Market: {
                mapping: "extended_related_markets_via_search"
              }
            , OrgGroup: {
                mapping: "extended_related_org_groups_via_search"
              }
            , Process: {
                mapping: "extended_related_processes_via_search"
              }
            , Product: {
                mapping: "extended_related_products_via_search"
              }
            , Project: {
                mapping: "extended_related_projects_via_search"
              }
            , System: {
                mapping: "extended_related_systems_via_search"
              }
            , Document: {
                mapping: "extended_related_documents_via_search"
              }
        }
      })
    ;

  // Disable editing on profile pages, as long as it isn't audits on the dashboard
  if (GGRC.page_instance() instanceof CMS.Models.Person) {
    var person_options = extra_content_controller_options.Person;
    can.each(person_options, function(options, model_name) {
      if (model_name !== 'Audit' || !/dashboard/.test(window.location)) {
        can.extend(options, {
            allow_creating: false
          , allow_mapping: false
        });
      }
    });
  }

  can.each(far_models, function(join_descriptors, model_name) {
    if ((overridden_models.all
          && overridden_models.all.hasOwnProperty(model_name)
          && !overridden_models[model_name])
        || (overridden_models[object.constructor.shortName]
            && overridden_models[object.constructor.shortName].hasOwnProperty(model_name)
            && !overridden_models[object.constructor.shortName][model_name]))
      return;

    var sources = []
      , list_loader
      , join_descriptor = join_descriptors[0]
      ;

    can.each(join_descriptors, function(join_descriptor) {
      sources.push(join_descriptor.get_loader());
    });
    list_loader = new GGRC.ListLoaders.TypeFilteredListLoader(
      new GGRC.ListLoaders.MultiListLoader(sources), [model_name]);
    list_loader = list_loader.attach(object);

    var far_model = join_descriptor.get_model(model_name);
    var extenders = [];

    // Custom overrides
    if (extra_descriptor_options.all
        && extra_descriptor_options.all[model_name]
    ) {
      extenders.push(extra_descriptor_options.all[model_name]);
    }

    if (extra_descriptor_options[object.constructor.shortName]
        && extra_descriptor_options[object.constructor.shortName][model_name]) {
      extenders.push(extra_descriptor_options[object.constructor.shortName][model_name]);
    }

    if (extra_content_controller_options.all
        && extra_content_controller_options.all[model_name]) {
      extenders.push({ content_controller_options : extra_content_controller_options.all[model_name] });
    }

    if (extra_content_controller_options[object.constructor.shortName]
        && extra_content_controller_options[object.constructor.shortName][model_name]) {
      extenders.push({ content_controller_options : extra_content_controller_options[object.constructor.shortName][model_name] });
    }

    if (!list_loader)
      return;

    if (GGRC.page_instance() instanceof CMS.Models.Program && model_name === 'Person') {
      extenders.push(GGRC.widget_descriptors[far_model.table_singular]);
    }
    
    var wd= GGRC.WidgetDescriptor.make_tree_view(GGRC.page_instance(), far_model, list_loader, extenders);
    wd.register_as_default();

  });

});

})(window.can, window.can.$);
