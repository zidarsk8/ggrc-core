(function(can, $) {

can.Control("GGRC.Controllers.InfoWidget", {
  defaults : {
    model : null
    , instance : null
    , widget_view : GGRC.mustache_path + "/base_objects/info.mustache"
  }
  , init : function() {
    var that = this;
    $(function() {
      if (GGRC.page_object) {
        $.extend(that.defaults, {
          model : GGRC.infer_object_type(GGRC.page_object)
          , instance : GGRC.make_model_instance(GGRC.page_object)
        });
      }
    });
  }
}, {
  init : function() {
    var $content = this.options.$content = this.element.find("section.content");
    can.view(this.options.widget_view, this.options.instance, function(frag) {
      $content.html(frag);
    });
  }

});

})(this.can, this.can.$);
