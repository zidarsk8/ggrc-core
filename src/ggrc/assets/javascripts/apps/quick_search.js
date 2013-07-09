/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require controllers/quick_search_controller
(function(namespace, $) {

$(function() {

  $(".recent").ggrc_controllers_recently_viewed();

  function bindQuickSearch(ev, opts) {

    var $qs = $(this).uniqueId();
    var obs = new can.Observe();
    $qs.bind("keypress", "input.widgetsearch", function(ev) {
      if(ev.which === 13)
        obs.attr("value", $(ev.target).val());
    });
    can.getObject("Instances", CMS.Controllers.QuickSearch, true)[$qs.attr("id")] = 
     $qs.find(".lhs-nav:not(.recent), section.content")
      .cms_controllers_quick_search(can.extend({
        observer : obs
        , spin : $qs.is(":not(section)")
      }, opts)).control(CMS.Controllers.QuickSearch);

  }
  $("section.widget-tabs").each(function() {
    bindQuickSearch.call(this, {}, {});
  });//get anything that exists on the page already.

  $(".lhs").each(function() {
    bindQuickSearch.call(this, {}, {
      list_view : GGRC.mustache_path + "/base_objects/search_result.mustache"
      , tooltip_view : GGRC.mustache_path + "/base_objects/extended_info.mustache"
      , spin : false
      , tab_selector : 'ul.top-level > li > a'
      // , tab_href_attr : [ "href", "data-tab-href" ]
      , tab_target_attr : "href"
      // , tab_model_attr : [ "data-model", "data-object-singular" ]
      , limit : 6
    });
  });
  //Then listen for new ones
  $(document.body).on("click", ".quick-search:not(:has(.cms_controllers_quick_search)), section.widget-tabs:not(:has(.cms_controllers_quick_search))", bindQuickSearch);

  
  $(document.body).on("click", ".bar-v", function(ev) {
    $("#lhs").toggleClass("lhs-closed");
    var newAreaWidth = $(".area").width();
    if ($("#lhs").hasClass("lhs-closed")) {
      newAreaWidth = newAreaWidth + 200;
    } else {
      newAreaWidth = newAreaWidth - 200;
    };
    var newObjectAreaWidth = newAreaWidth - 200;
    $(".area").css("width", newAreaWidth);
    $(".object-area").css("width", newObjectAreaWidth);
  });

});

})(this, jQuery);