/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: anze@reciprocitylabs.com
    Maintained By: anze@reciprocitylabs.com
*/

;(function(CMS, GGRC, can, $) {
  can.Control("GGRC.Controllers.MappingCount", {
    defaults: {
      view: GGRC.mustache_path + "/dashboard/mapping_count.mustache",
      person: null,
      mapping: null,
    },
    init: function() {
      if (this._super) {
        this._super.apply(this, arguments);
      }
    }
  }, {
    init: function() {
      this._super.apply(this, arguments);
      var that = this;
      can.view(this.options.view, this.options, function(frag) {
        that.element.append(frag);
      });
      this.on();
    },
  });

})(this.CMS, this.GGRC, this.can, this.can.$);
