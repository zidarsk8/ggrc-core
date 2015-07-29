/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/
(function($, GGRC) {
  GGRC.Utils = {
    getPickerElement: function (picker) {
      return _.find(_.values(picker), function (val) {
        if (val instanceof Node) {
          return /picker\-dialog/.test(val.className);
        }
        return false;
      });
    },
    download: function (filename, text) {
      var element = document.createElement('a');
      element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
      element.setAttribute('download', filename);
      element.style.display = 'none';
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    export_request: function (request) {
      return $.ajax({
        type: "POST",
        dataType: "text",
        headers: $.extend({
          "Content-Type": "application/json",
          "X-export-view": "blocks",
          "X-requested-by": "gGRC"
        }, request.headers || {}),
        url: "/_service/export_csv",
        data: JSON.stringify(request.data || {})
      });
    },
    is_mapped: function (target, destination) {
      var bindings = target.get_binding(CMS.Models[destination.type].table_plural);
      if (bindings && bindings.list && bindings.list.length) {
        return _.find(bindings.list, function (item) {
          return item.instance.id === destination.id;
        });
      }
      if (target.objects && target.objects.length) {
        return _.find(target.objects, function (item) {
          return item.id === destination.id && item.type === destination.type;
        });
      }
    }
  };
})(jQuery, window.GGRC = window.GGRC || {});
