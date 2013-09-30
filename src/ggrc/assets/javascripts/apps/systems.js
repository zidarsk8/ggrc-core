/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: brad@reciprocitylabs.com
 * Maintained By: brad@reciprocitylabs.com
 */

//= require can.jquery-all

(function(can, $) {

if(!/^\/systems\/\d+/.test(window.location.pathname))
 return;


$(function() {
  var system = GGRC.page_instance();

  var $top_tree = $("#system_widget .tree-structure").cms_controllers_tree_view({
    model : CMS.Models.System
    , single_object : true
    , list : [system]
  });

  var $top_risk_tree = $("#system_risk_widget .tree-structure").cms_controllers_tree_view({
    model : CMS.Models.System
    , single_object : true
    , list : [system]
    , options_property : "risk_tree_options"
  });


  $(document.body).on("modal:success", ".link-objects", function(ev, data) {
    $top_tree.trigger("linkObject", $.extend($(this).data(), {
      parentId : system_id
      , data : data
    }));

  });


});

})(window.can, window.can.$);
