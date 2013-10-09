/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: andy@reciprocitylabs.com
    Maintained By: andy@reciprocitylabs.com
*/


(function(can, $) {

can.Control("StickyHeader", {
    defaults: {
        header: "header"
      , scroll_area: ".object-area"
    }
}, {
    init : function() {
      this.options = new can.Observe(can.extend(this.options, {
          header: typeof this.options.header === 'string' ? this.element.find(this.options.header) : this.options.header
        , scroll_area: typeof this.options.scroll_area === 'string' ? this.element.closest(this.options.scroll_area) : this.options.scroll_area
      }));
      this.options.header.css('transform-origin', '0 0');
      this.on();
    }

  , "{scroll_area} scroll" : function(el, ev) {
    if (!this.options.header.is(":visible"))
      return;

    if (!this._origin && !this._margin) {
      this._origin = this.options.scroll_area[0].scrollTop;
      this._margin = this.options.header.position().top;
    }
    
    this.position(Math.max(0, el[0].scrollTop - this._origin - this._margin));
  }

  , position : function(y_position) {
    this.options.header.transition({ 'translate': [0, y_position] }, 0, 'cubic-bezier(0.33, 0.66, 0.66, 1)');
  }
});

})(this.can, this.can.$);
