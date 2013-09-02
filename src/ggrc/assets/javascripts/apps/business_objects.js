/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all

(function(can, $) {

$(function() {
  if (!GGRC.page_object)
    return;

  var object_class = GGRC.infer_object_type(GGRC.page_object)
    , object_table = object_class.table_plural
    , object = GGRC.page_instance();

  var info_widget_views = {
    'programs': GGRC.mustache_path + "/programs/info.mustache"
  }
  default_info_widget_view = GGRC.mustache_path + "/base_objects/info.mustache";

  var info_widget_descriptors = {
      info: {
          widget_id: "info"
        , widget_name: object_class.title_singular + " Info"
        , widget_icon: "grcicon-info"
        , content_controller: GGRC.Controllers.InfoWidget
        , content_controller_options: {
              instance: object
            , model: object_class
            , widget_view: info_widget_views[object_table] || default_info_widget_view
          }
      }
  }

  if (!GGRC.extra_widget_descriptors)
    GGRC.extra_widget_descriptors = {};
  if (!GGRC.extra_default_widgets)
    GGRC.extra_default_widgets = [];

  GGRC.extra_widget_descriptors.info = info_widget_descriptors.info;
  GGRC.extra_default_widgets.splice(0, 0, 'info');

  function sort_sections(sections) {
    return can.makeArray(sections).sort(window.natural_comparator);
  }

  var far_models = GGRC.JoinDescriptor
        .by_object_option_models[object.constructor.shortName]
    , model_widget_descriptors = {}
    , model_default_widgets = []
    , extra_descriptor_options = {
          all: {
              Person: {
                  widget_icon: 'grcicon-user-black'
              }
            , Document: {
                  widget_icon: 'grcicon-link'
              }
          }
      }
    // Prevent widget creation with <model_name>: false
    // e.g. to prevent ever creating People widget:
    //     { Person: false }
    // or to prevent creating People widget on Objective page:
    //     { Objective: { Person: false } }
    , overridden_models = {
          Program: {
            //  Objective: false
            //, Control: false
            //, Regulation: false
            //, Policy: false
            //, Contract: false
          }
      }

    , directive_section_descriptor =
        GGRC.JoinDescriptor.by_object_option_models.Regulation.Section[0]
    , program_directive_options = {
          list_view : GGRC.mustache_path + "/directives/tree.mustache"
        , draw_children : true
        , child_options : [{
              model : CMS.Models.Section
            , list_loader : function(directive) {
                return directive_section_descriptor
                  .get_loader()
                  .attach(directive)
                  .refresh_list();
              }
            , fetch_post_process : sort_sections
            , draw_children : true
            }]
      }
    , extra_content_controller_options = {
          Program: {
              Regulation: program_directive_options
            , Policy: program_directive_options
            , Contract: program_directive_options
            , Control: { draw_children : true }
            , Objective: { draw_children : true }
          }
        , Regulation: {
          Section : program_directive_options.child_options[0]
          , Control : { draw_children : true }
        }
        , Policy: {
          Section : program_directive_options.child_options[0]
          , Control : { draw_children : true }
        }
        , Contract : {
          Section : program_directive_options.child_options[0]
          , Control : { draw_children : true }
        }
      }
    ;

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
    list_loader = new GGRC.ListLoaders.MultiListLoader(sources);
    list_loader = list_loader.attach(object);

    var far_model = join_descriptor.get_model(model_name)
      , descriptor = {
            content_controller: CMS.Controllers.TreeView
          , content_controller_selector: "ul"
          , widget_initial_content: '<ul class="tree-structure new-tree"></ul>'
          , widget_id: far_model.table_singular
          , widget_name: function() {
              var $objectArea = $(".object-area");
              if ( $objectArea.hasClass("dashboard-area") ) {
                return far_model.title_plural;
              } else {
                return "Mapped " + far_model.title_plural;
              }
            }

          , widget_info : function() {
              var $objectArea = $(".object-area");
              if ( $objectArea.hasClass("dashboard-area") ) {
                return ""
              } else {
                return "Does not include mappings to Directives, Objectives and Controls"
              }
            }
          , widget_icon: far_model.table_singular
          , object_category: far_model.category || 'default'
          , content_controller_options: {
                child_options: []
              , draw_children: false
              , parent_instance: object
              , model: model_name
              , list_loader: can.proxy(list_loader, "refresh_list")
            }
        }
      ;

    // Custom overrides
    if (extra_descriptor_options.all
        && extra_descriptor_options.all[model_name]) {
      can.extend(
          descriptor,
          extra_descriptor_options.all[model_name]);
    }

    if (extra_descriptor_options[object.constructor.shortName]
        && extra_descriptor_options[object.constructor.shortName][model_name]) {
      can.extend(
          descriptor,
          extra_descriptor_options[object.constructor.shortName][model_name]);
    }

    if (extra_content_controller_options.all
        && extra_content_controller_options.all[model_name]) {
      can.extend(
          descriptor.content_controller_options,
          extra_content_controller_options.all[model_name]);
    }

    if (extra_content_controller_options[object.constructor.shortName]
        && extra_content_controller_options[object.constructor.shortName][model_name]) {
      can.extend(
          descriptor.content_controller_options,
          extra_content_controller_options[object.constructor.shortName][model_name]);
    }

    if (!list_loader)
      return;
    model_widget_descriptors[far_model.table_singular] = descriptor;
    model_default_widgets.push(far_model.table_singular);
  });

  can.extend(GGRC.extra_widget_descriptors, model_widget_descriptors);
  GGRC.extra_default_widgets.push.apply(
      GGRC.extra_default_widgets, model_default_widgets);
});

})(window.can, window.can.$);
