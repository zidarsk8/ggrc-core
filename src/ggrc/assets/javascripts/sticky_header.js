/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: andy@reciprocitylabs.com
    Maintained By: andy@reciprocitylabs.com
*/


(function(can, $) {

can.Control("StickyHeader", {
    defaults: {
        // A selector for the scrollable area ancestor
        scroll_area_selector: ".object-area"
        // A selector for all sticky-able headers
      , header_selector: ".header, .tree-open > .item-open > .item-main"
        // A selector for counting the depth
        // Generally this should be header_selector with the final element in each selector removed
      , depth_selector: ".tree-open > .item-open"
        // The amount of space at the bottom of the content when the header should start scrolling away
      , margin: 30
    }
}, {
    init : function() {
      this.options = can.extend(this.options, {
        scroll_area: this.element.closest(this.options.scroll_area_selector)
      });
      this.on();
    }

    // Handle window scrolling
  , "{scroll_area} scroll" : function(el, ev) {
    // Only process if this section is visible
    if (!this.element.is(":visible"))
      return;

    // Update the header positions
    this._headers = this.find_headers();
    for (var i = this._headers.length - 1; i >= 0; i--) {
      var el = this._headers.eq(i)
        , clone = el.data('sticky').clone
        , margin = this.in_viewport(el)
        ;

      // Remove the clone if its content no longer inside the viewport
      if (margin === false) {
        clone[0].parentNode && clone.remove();
        $.removeData(el, 'sticky');
      }
      // Otherwise inject the clone
      else {
        !clone[0].parentNode && el.parent().append(clone);

        // When the content is close to scrolling away, also scroll the header away
        clone.css('marginTop', margin + 'px');
      }
    }
  }

    // Resize clones on window resize
  , "{window} resize" : function(el, ev) {
    var self = this;
    this._headers && this._headers.each(function() {
      var $this = $(this);
      self.position_clone($this, $this.data('sticky').clone);
    });
  }

    // Find all sticky-able headers in the document
  , find_headers : function() {
    var headers = this.element.find(this.options.header_selector).filter(':not(.sticky):visible')
      , self = this
      ;

    // Generate the depth and clone for each header
    headers.each(function(i) {
      var $this = $(this);
      if (!$this.data('sticky')) {
        var data = {
          depth: $this.parents(self.options.depth_selector).length
        };
        $this.data('sticky', data);
        data.clone = self.clone($this, headers.slice(0, i));
      }
    });

    return headers;
  }

    // Determine whether a header's content section is within the scrolling viewport
  , in_viewport : function(el) {
    var parent = el.parent()
      , pos = parent.position()
      , top = this.options.scroll_area[0].scrollTop
      , bottom = top + this.options.scroll_area.outerHeight() 
      , offset = el.data('sticky').offset
      , margin = pos.top + parent.outerHeight() - el.outerHeight() - offset
      ;

    // If the content is in the viewport...
    if (pos.top < offset && (pos.top + parent.outerHeight() - el.outerHeight()) > offset) {
      // Return zero or the amount that the header should start scrolling away if applicable
      return margin <= this.options.margin ? -Math.max(0, this.options.margin - margin) : 0;
    }
    else
      return false;
  }

    // Clones and prepares a header
  , clone : function(el, headers) {
    // Compute heights of above headers
    var offset = 0
      , data = el.data('sticky')
      , depths = []
      ;

    // Determine the offset based on nested parents
    for (var i = headers.length - 1; i >= 0; i--) {
      var $this = $(headers[i])
        , depth = $this.data('sticky').depth
        ;

      // Only add offsets for the closest nested parent of the given depth
      if (!depths[depth] && depth < data.depth) {
        offset += $this.outerHeight();
        depths[depth] = true;
      }
    }
    data.offset = offset;

    return this.position_clone(el, el.clone(true, true).addClass("sticky"));
  }

    // Reposition a clone
  , position_clone : function(el, clone) {
    return clone.css({
          position: 'fixed'
        , top: (el.data('sticky').offset + parseFloat(this.options.scroll_area.css("top"))) + 'px'
        , left: el.offset().left + 'px'
        , width: (el[0].getBoundingClientRect().width
            - parseFloat(el.css('paddingLeft')) 
            - parseFloat(el.css('paddingRight'))) 
            + 'px'
      });
  }

    // Clean up when destroyed
  , destroy : function() {
    this._headers.each(function() {
      var $this = $(this);
      $this.data('sticky').clone.remove();
      $.removeData($this, 'sticky');
    });
    delete this._headers;
  }
});

})(this.can, this.can.$);
