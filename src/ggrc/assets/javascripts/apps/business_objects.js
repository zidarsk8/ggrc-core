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

  var object_class = GGRC.infer_object_type(GGRC.page_object);
  var object = GGRC.make_model_instance(GGRC.page_object);

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
