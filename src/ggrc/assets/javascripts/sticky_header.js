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
      , mode: "fixed" // transform | fixed
    }
}, {
    init : function() {
      this.options = new can.Observe(can.extend(this.options, {
          header: typeof this.options.header === 'string' ? this.element.find(this.options.header) : this.options.header
        , scroll_area: typeof this.options.scroll_area === 'string' ? this.element.closest(this.options.scroll_area) : this.options.scroll_area
      }));
      this.on();
    }

  , "{scroll_area} scroll" : function(el, ev) {
    if (!this.options.header.is(":visible"))
      return;

    // Initialize on first visibility
    if (!this._origin && !this._margin) {
      this._origin = this.options.scroll_area[0].scrollTop;
      this._margin = this.options.header.position().top;
      if (this.options.mode === "fixed") {
        this._clone_min = this.options.header.position().top;
        this._clone = this.options.header.clone(true, true).css({
            position: 'fixed'
          , top: this.options.scroll_area.css("top")
          , left: this.options.header.offset().left + 'px'
          , width: (this.options.header[0].getBoundingClientRect().width
              - parseFloat(this.options.header.css('paddingLeft')) 
              - parseFloat(this.options.header.css('paddingRight'))) + 'px'
        });
      }
      else if (this.options.mode === "transform")
        this.options.header.css('transform-origin', '0 0');
    }

    // Update the position
    if (this.options.mode === "fixed") {
      if (el[0].scrollTop < this._margin && this._clone[0].parentNode) {
        this._clone.remove();
    }
    else if (this.options.mode === "transform") {
      var y_position = Math.max(0, el[0].scrollTop - this._origin - this._margin);
      this.options.header.transition({ 'translate': [0, y_position] }, 0, 'cubic-bezier(0.33, 0.66, 0.66, 1)');
    }
  }
});

})(this.can, this.can.$);
