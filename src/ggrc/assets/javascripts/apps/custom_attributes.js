/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: anze@reciprocitylabs.com
    Maintained By: anze@reciprocitylabs.com
*/

(function(can, $) {

  can.Component.extend({
    tag: "custom-attributes",
    scope: {
      instance: null
    },
    content: "<content/>",
    events: {
    },
    helpers: {
      with_custom_attribute_definitions: function(options) {
        var instance = this.instance || GGRC.page_instance(),
            self = this,
            dfd;

        if (!(instance && instance.custom_attribute_definitions)) {
          return;
        }

        dfd = $.when(
          instance.custom_attribute_definitions(),
          // Making sure custom_attribute_values are loaded
          instance.custom_attribute_values ? instance.refresh_all('custom_attribute_values') : []
        );

        function finish(custom_attributes, values) {
          setTimeout(function() {
            // TODO: Find a better way of enabling rich text fields
            $($.find('custom-attributes .wysihtml5')).each(function() {
              $(this).cms_wysihtml5();
            });

            // TODO: Find a better way for inserting attribute values into DOM
            $($.find("custom-attributes :input:not(isolate-form *)")).each(function(_, el) {
              var $el = $(el), name, val = "", id, i;
              if (!$el.attr('name')) {
                return;
              }
              name = $el.attr('name').split('.');
              if (name[0] != 'custom_attributes') {
                return;
              }
              id = name[1];

              for (i = 0; i < values.length; i++) {
                if (values[i].custom_attribute_id == id) {
                  val = values[i].attribute_value;
                }
              }
              $el.val(val);
              // TODO: This bit triggers a validate form on load, causing the title
              //       cannot be blank error to show up on form load.
              $el.trigger('change');
            });
            $($.find("custom-attributes [data-custom-attribute]")).each(function(_, el) {
              var $el = $(el),
                  id = $el.data('custom-attribute'),
                  val = "";

              for (i = 0; i < values.length; i++) {
                if (values[i].custom_attribute_id == id) {
                  val = values[i].attribute_value;
                }
              }
              $el.html(val);
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
