/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require directives/routes_controller
//= require mapping/mapping_controller
//= require models/simple_models
(function(namespace, $) {

var directive_id = namespace.location.pathname.substr(window.location.pathname.lastIndexOf("/") + 1);

function getPageModel() {
  if($(document.body).attr("data-page-type") === "directives") { 
    switch($(document.body).attr("data-page-subtype")) {
      case "regulations" :
        return CMS.Models.Regulation;
      case "policies" :
        return CMS.Models.Policy;
      case "contracts" :
        return CMS.Models.Contract;
      default :
        return CMS.Models.Directive;
    }
  } else { 
    return CMS.Models.Program;
  }
}

//Note that this also applies to programs
jQuery(function($) {
  $("body").on("click", "a.controllist, a.objectivelist", function(ev) {
    var $trigger = $(ev.currentTarget)
    , model = $trigger.is(".objectivelist") ? CMS.Models.Objective : CMS.Models.Control
    , $section = $trigger.closest("[data-id]")
    , $dialog = $("#mapping_dialog")
    , id = $section.data("id");

    if(!$dialog.length) {
      $dialog = $('<div id="mapping_dialog" class="modal modal-selector hide"></div>')
        .appendTo(document.body)
        .draggable({ handle: '.modal-header' });
    }
    $dialog.html($(new Spinner().spin().el).css({"position" : "relative", "left" : 50, "top" : 50, "height": 150, "width": 150}));
    $dialog.modal("show");

    (CMS.Models.SectionSlug.findInCacheById(id)
      ? $.when(CMS.Models.SectionSlug.findInCacheById(id))
      : CMS.Models.SectionSlug.findAll({ id : id }))
    .done(function(section) {
      $dialog.cms_controllers_control_mapping_popup({
        section : $(section).filter(function(i, d) { return d.id == id; })[0]
        , parent_model : getPageModel()
        , parent_id : directive_id
        , model : model
        , subheader_view : GGRC.mustache_path + "/" + model.table_plural + "/selector_subheader.mustache"
      });
      $(document.body).trigger('kill-all-popovers');

      var timeout, oldvals;
      can.each({
        controls: "control"
        , objectives: "objective"
      }, function(type, collection) {

        section[collection].bind("change.mapper", function(ev, attr, how, newVal, oldVal) {
          if(!~attr.indexOf(".") && how === "add") { // when newval and oldval are correct
            if(timeout) {
              can.each(oldvals, function(v) {
                if(!~can.inArray(v, newVal)) {
                  $section.find(".cms_controllers_tree_view[data-object-type=" + type + "]:first").trigger("removeChild", v);
                }
              });
              clearTimeout(timeout);
            }
            can.each(newVal, function(v) {
              if(!~can.inArray(v, oldVal)) {
                $section.find(".cms_controllers_tree_view[data-object-type=" + type + "]:first").trigger("newChild", v);
              }
            });
          } else if(!~attr.indexOf(".") && how === "remove") {
            oldvals = oldVal;
            timeout = setTimeout(function() {
              can.each(oldVal, function(v) {
                $section.find(".cms_controllers_tree_view[data-object-type=" + type + "]:first").trigger("removeChild", v);
              });
              timeout = null;
            }, 100);
          }
        });
        $dialog.one("hide", function() {
          section[collection].unbind("change.mapper");
        });
      });
    });
  });
});


if (!/\/directives\b/.test(window.location.pathname))
  return;

$(function() {
  var spin_opts = { position : "absolute", top : 100, left : 100, height : 50, width : 50};
  var $controls_tree, uncategorized;

  CMS.Controllers.DirectiveRoutes.Instances = {
    Control : $(document.body).cms_controllers_directive_routes({}).control(CMS.Controllers.DirectiveRoutes)};

  $controls_tree = $("#controls .tree-structure").append($(new Spinner().spin().el).css(spin_opts));
  $.when(
    CMS.Models.Category.findTree()
    , CMS.Models.Control.findAll({ directive_id : directive_id })
  ).done(function(cats, ctls) {
    uncategorized = cats[cats.length - 1]
    , ctl_cache = {}
    , uncat_cache = {};
    can.each(ctls, function(c) {
      uncat_cache[c.id] = ctl_cache[c.id] = c;
    });
    function link_controls(c) {
      //empty out the category controls that aren't part of the program
      c.controls.replace(can.map(c.controls, function(ctl) {
        delete uncat_cache[c.id];
        return ctl_cache[c.id];
      }));
      can.each(c.children, link_controls);
    }
    can.each(cats, link_controls);
    can.each(Object.keys(uncat_cache), function(cid) {
        uncategorized.controls.push(uncat_cache[cid]);
    });

    $controls_tree.cms_controllers_tree_view({
      model : CMS.Models.Category
      , list : cats
    });
  });

  var $sections_tree = $("#sections .tree-structure").append($(new Spinner().spin().el).css(spin_opts));

  CMS.Models.SectionSlug.findAll({ directive_id : directive_id, "parent_id__null" : true })
  .done(function(s) {

    $sections_tree.cms_controllers_tree_view({
      model : CMS.Models.SectionSlug
      , edit_sections : true
      , list : s
      , list_view : "/static/mustache/sections/tree.mustache"
    });
  });

  $("#sections").on("modal:success", "a[data-toggle=modal-ajax-form][data-object-singular=Control], a[data-toggle=modal-ajax-form][data-object-singular=Objective]", function(ev, data) {
    //var c = new CMS.Models.Control(data);
    var $object = $(this)
    , section = $object
      .closest('[data-object-meta-type=section]').find('[data-model]').first()
      .data("model")
    , params = { context : GGRC.make_model_instance(GGRC.page_object).context };
    params[data.constructor.table_singular] = data;

    if(data instanceof CMS.Models.Control) {
      //TODO uncomment when categorizations are restored to controls
      // can.each(data.categorizations.length ? data.categorizations : [uncategorized], function(catid) {
      //   $controls_tree.find("[data-object-id=" + catid + "] > .item-content > ul[data-object-type=control]").trigger("newChild", data);
      // });
    }

    section["map_" + data.constructor.table_singular](params).done(function(){
      $object.trigger("newChild", data);
    });
  });

  $(document.body).on("modal:success", "a[href^='/sections'][href$='/edit']", function(ev, data) {
    CMS.Models.SectionSlug.model(data);
  });

  $(document.body).on("modal:success", "a[href^='/sections/new']", function(ev, data) {
    var c = new CMS.Models.SectionSlug(data)
    , p;
    $("a[href='#sections']").click();

    if(c.parent_id && (p = CMS.Models.SectionSlug.findInCacheById(c.parent_id))) {
      $sections_tree.control().add_child_lists([c]);
      p.children.push(c);
    } else {
      $sections_tree.trigger("newChild", c);
    }

  });

});

})(this, jQuery);
