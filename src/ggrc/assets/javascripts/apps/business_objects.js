/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all

(function(can, $) {

$(function() {
  var object_class = GGRC.infer_object_type(GGRC.page_object);
  var object = GGRC.make_model_instance(GGRC.page_object);

  if(!~can.inArray(
    object_class
    , [CMS.Models.OrgGroup
    , CMS.Models.Project
    , CMS.Models.Product
    , CMS.Models.DataAsset
    , CMS.Models.Facility
    , CMS.Models.Market]))
    return;

  var $top_tree = $("#" + object_class.root_object + "_widget .tree-structure").cms_controllers_tree_view({
    model : object_class
    // , list_view : GGRC.mustache_path + "/" + object_class.root_collection + "/tree.mustache"
    , single_object : true
    , list : [object]
  });

  $(document.body).on("modal:success", ".link-objects", function(ev, data) {
    $top_tree.trigger("linkObject", $.extend($(this).data(), {
      parentId : object.id
      , data : data
    }));

  });


});

})(window.can, window.can.$);