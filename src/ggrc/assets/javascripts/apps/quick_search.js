/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function($) {
  $(document.body).on("click", ".lhn-no-init", function() {
    $(this).removeClass('lhn-no-init');
    import(/* webpackChunkName: "lhn" */'../controllers/lhn_controllers')
      .then(function () {
        $("#lhn").cms_controllers_lhn();
        $(document.body).ggrc_controllers_recently_viewed();
      });
  });

  $(document.body).on("click", "a[data-toggle=unmap]", function(ev) {
    var $el = $(this)
      ;
    //  Prevent toggling `openclose` state in trees
    ev.stopPropagation();
    $el.fadeTo('fast', 0.25);
    $el.children(".result").each(function(i, result_el) {
      var $result_el = $(result_el)
        , result = $result_el.data('result')
        , mappings = result && result.get_mappings()
        , i
        ;

      function notify(instance){
        $(document.body).trigger(
            "ajax:flash"
            , {"success" : "Unmap successful."}
          );
      }

      can.each(mappings, function(mapping) {
        mapping.refresh().done(function() {
          if (mapping instanceof CMS.Models.Control) {
            mapping.removeAttr('directive');
            mapping.save().then(notify);
          }
          else {
            mapping.destroy().then(notify);
          }
        });
      });
    });
  });
})(jQuery);
