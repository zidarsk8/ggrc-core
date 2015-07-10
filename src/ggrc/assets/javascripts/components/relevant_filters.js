/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function(can, $) {
  can.Component.extend({
    tag: "relevant-filter",
    template: can.view(GGRC.mustache_path + "/mapper/relevant_filter.mustache"),
    scope: {
      menu: can.compute(function () {
        var type = this.attr("type") === "AllObject" ? GGRC.page_model.type : this.attr("type"),
            mappings = GGRC.Mappings.get_canonical_mappings_for(type);
        return _.map(_.keys(mappings), function (mapping) {
          return CMS.Models[mapping];
        });
      })
    },
    events: {
      ".add-filter-rule click": function (el, ev) {
        ev.preventDefault();
        this.scope.attr("relevant").push({
          value: "",
          filter: new can.Map(),
          model_name: this.scope.attr("menu")[0].model_singular
        });
      },
      ".ui-autocomplete-input autocomplete:select": function (el, ev, data) {
        var index = el.data("index"),
            panel = this.scope.attr("relevant")[index];

        panel.attr("filter", data.item);
      },
      ".remove_filter click": function (el) {
        this.scope.attr("relevant").splice(el.data("index"), 1);
      }
    }
  });
})(window.can, window.can.$);
