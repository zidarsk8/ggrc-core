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
      , header_selector: ".header, .tree-open > .item-open > .item-main, .advanced-filters"
        // A selector for all sticky-able footers
      , footer_selector: ".tree-footer"
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

    // Update the header/footer positions
    this.update_items('header');
    this.update_items('footer');
  }

    // Resize clones on window resize
  , "{window} resize" : function(el, ev) {
    this.position_items('header');
    this.position_items('footer');
  }

    // Updates the given set of sticky items
  , update_items : function(type) {
    var items = this['_'+type] = this.find_items(type);
    for (var i = items.length - 1; i >= 0; i--) {
      var el = items.eq(i)
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
        clone.css('margin' + (type === 'footer' ? 'Bottom' : 'Top'), margin + 'px');
      }
    }
  }
    // Repositions all sticky items
  , position_items : function(type) {
    var self = this;
    this['_'+type] && this['_'+type].each(function() {
      var $this = $(this);
      self.position_clone($this, $this.data('sticky').clone);
    });
  }

    // Find all sticky-able headers in the document
  , find_items : function(type) {
    var items = this.element.find(this.options[type + '_selector']).filter(':not(.sticky):visible')
      , self = this
      , increment = type === 'footer' ? -1 : 1
      , i = type === 'footer' ? items.length - 1 : 0
      ;

    // Generate the depth and clone for each header
    for (var $this; $this = items[i]; i += increment) {
      $this = $($this);
      if (!$this.data('sticky')) {
        var data = {
            type: type
          , depth: $this.parents(self.options.depth_selector).length
        };
        $this.data('sticky', data);
        data.clone = self.clone($this, type === 'footer' ? items.slice(i) : items.slice(0, i));
      }
    }

    return items;
  }

    // Determine whether a header's content section is within the scrolling viewport
  , in_viewport : function(el) {
    var data = el.data('sticky')
      , type = data.type
      , parent = el.parent()
      , offset = data.offset
      , pos = parent.position().top
      , margin
      ;

    if (type === 'footer') {
      offset = data.offset + this.options.scroll_area.outerHeight() + this.options.scroll_area[0].scrollTop;
      pos = el.position().top + this.options.scroll_area[0].scrollTop + el.outerHeight();
    }
    margin = pos + parent.outerHeight() - el.outerHeight();

    // If the content is in the viewport...
    if ((type === 'footer' ? offset < pos : pos < offset) && margin > offset) {
      // Return zero or the amount that the header should start scrolling away if applicable
      margin -= offset;
      return margin <= this.options.margin ? -Math.max(0, this.options.margin - margin) : 0;
    }
    else
      return false;
  }

    // Clones and prepares a header
  , clone : function(el, items) {
    // Compute heights of above items
    var offset = 0
      , data = el.data('sticky')
      , depths = []
      , selector
      , increment = data.type === 'footer' ? -1 : 1
      , i = data.type === 'footer' ? items.length - 1 : 0
      ;

    // Determine which selector part grabbed this element
    can.each(this.options[data.type + '_selector'].split(','), function(part) {
      if (el.is(part))
        selector = part;
    });

    // Determine the offset based on nested parents
    for (var $this; $this = items[i]; i += increment) {
      if (el[0] === $this) {
        break;
      }
      else {
        $this = $($this);
        var depth = $this.data('sticky').depth;

        // Only add offsets for the closest nested parent of the given depth
        // as well as offsets for siblings with different selectors
        if ((!depths[depth] && depth < data.depth) || (depth <= data.depth && !$this.is(selector))) {
          offset += $this.outerHeight();
          depths[depth] = true;
        }
      }
    }
    data.offset = offset;

    return this.position_clone(el, el.clone(true, true).addClass("sticky sticky-" + data.type));
  }

    // Reposition a clone
  , position_clone : function(el, clone) {
    var data = el.data('sticky');
    return clone.css({
          position: 'fixed'
        , left: el.offset().left + 'px'
        , width: (el[0].getBoundingClientRect().width
            - parseFloat(el.css('paddingLeft')) 
            - parseFloat(el.css('paddingRight'))) 
            + 'px'
      }).css(
          data.type === 'footer' ? 'bottom' : 'top'
          , (
              data.type === 'footer'
              ? data.offset + $(window).height() - this.options.scroll_area.outerHeight() - parseFloat(this.options.scroll_area.position().top)
              : data.offset + parseFloat(this.options.scroll_area.position().top)
            ) + 'px'
      );
  }

    // Clean up when destroyed
  , destroy : function() {
    var items = $().add(this._header || $()).add(this._footer || $());
    items.each(function() {
      var $this = $(this);
      $this.data('sticky').clone.remove();
      $.removeData($this, 'sticky');
    });
    delete this._header;
    delete this._footer;
  }
});

})(this.can, this.can.$);
