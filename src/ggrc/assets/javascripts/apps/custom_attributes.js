/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: anze@reciprocitylabs.com
    Maintained By: anze@reciprocitylabs.com
*/

(function(can, $) {

  can.Component.extend({
    tag: "custom-attributes",
    content: "<content/>",
    events: {
    },
    helpers: {
      with_custom_attribute_definitions: function(options) {
        var instance = this.instance,
            self = this,
            dfd = $.when(
              instance.custom_attribute_definitions(),
              // Making sure custom_attribute_values are loaded
              instance.custom_attribute_values ? instance.refresh_all('custom_attribute_values') : []
            );

        function finish(custom_attributes, values) {
          // TODO: Find a better way of enabling rich text fields
          setTimeout(function() {
            $($.find('custom-attributes .wysihtml5')).each(function() {
              $(this).cms_wysihtml5();
            });
          });

          return options.fn(options.contexts.add({
            loaded_definitions: custom_attributes.reverse()
          }));
        }

        function progress() {
          return options.inverse(options.contexts);
        }

        return Mustache.defer_render('div', {
          done: finish,
          progress: progress,
        }, dfd);
      }
    }
  });

})(window.can, window.can.$);
