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
    , object = GGRC.make_model_instance(GGRC.page_object);

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

  var queue = new RefreshQueue()
  , queue_dfd;

  can.each(object.object_people, can.proxy(queue, "enqueue"));
  can.each(object.object_documents, can.proxy(queue, "enqueue"));
  queue_dfd = queue.trigger();

  var business_object_widget_descriptors = {
      people: {
          widget_id: "people"
        , widget_name: "Mapped People"
        , widget_icon: "grcicon-user-black"
        , content_controller: GGRC.Controllers.ListView
        , content_controller_options: {
              model : CMS.Models.ObjectPerson
            , list_loader: function() {
                return queue_dfd.then(function() { return object.object_people; });
              }
            , list_view : GGRC.mustache_path + "/people/list.mustache"
            , parent_instance : object
          }
      }
    , documents: {
          widget_id: "documents"
        , widget_name: "Reference Links"
        , widget_icon: "grcicon-link"
        , content_controller: GGRC.Controllers.ListView
        , content_controller_options: {
              model : CMS.Models.ObjectDocument
            , list_loader: function(){
                return queue_dfd.then(function() { return object.object_documents; });
              }
            , list_view : GGRC.mustache_path + "/documents/list.mustache"
            , parent_instance : object
          }
      }

  }

  var widget_ids = ['people', 'documents']

  $.extend(GGRC.extra_widget_descriptors, business_object_widget_descriptors);
  GGRC.extra_default_widgets.push.apply(GGRC.extra_default_widgets, widget_ids);


  if(!~can.inArray(
    object_class
    , [CMS.Models.OrgGroup
      , CMS.Models.Project
      , CMS.Models.Product
      , CMS.Models.DataAsset
      , CMS.Models.Facility
      , CMS.Models.Market
      , CMS.Models.Risk]))
    return;

  var $top_tree = $("#" + object_class.root_object + "_widget .tree-structure").cms_controllers_tree_view({
    model : object_class
    , single_object : true
    , list : [object]
  }).on("modal:relationshipcreated modal:relationshipdestroyed", "li", function(ev, data) {
    var tree_obj = $(this).find(".item-main:first").data("model")
    , other_obj;

    if((other_obj = data.getOtherSide(tree_obj)) != null) {
      $(this)
      .find([".tree-structure[data-object-sub-type="
        , other_obj.constructor.table_singular
        , "], .tree-structure[data-object-type="
        , other_obj.constructor.shortName + "], .tree-structure[data-object-meta-type="
        , other_obj.constructor.root_object
        , "]"].join(""))
      .first()
      .trigger(ev.type === "modal:relationshipcreated" ? "newChild" : "removeChild", other_obj);
    }
  });

  var $risk_tree = $("#" + object_class.root_object + "_risk_widget .tree-structure").cms_controllers_tree_view({
    model : object_class
    , single_object : true
    , list : [object]
    , options_property : "risk_tree_options"
  });


  $(document.body).on("modal:success", ".link-objects", function(ev, data) {
    $top_tree.trigger("linkObject", $.extend($(this).data(), {
      parentId : object.id
      , data : data
    }));

  });


});

})(window.can, window.can.$);
