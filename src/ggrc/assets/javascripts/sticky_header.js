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
      , header_selector: ".header"
                      +", .tree-open > .item-open > .item-main"
                      +", .tree-open > .item-open > .item-content > .inner-tree > h6"
                      +", .advanced-filters"
        // A selector for all sticky-able footers
      , footer_selector: ".tree-footer"
        // A selector for counting the depth
        // Generally this should be header_selector with the final element in each selector removed
      , depth_selector: ".tree-open > .item-open"
                      +", .tree-open > .item-open > .item-content > .inner-tree"
        // Identify "extra" headers that should be fixed alongside their previous header siblings.
      , extra_selector: ".extra-header"
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
    // Update the header/footer positions
    this.update_items('header');
    this.update_items('footer');
  }

    // Updates the given set of sticky items
  , update_items : function(type) {
    var items = this.find_items(type);

    for (var i = items.length - 1; i >= 0; i--) {
      var el = items.eq(i)
        , clone = el.data('sticky').clone
        , margin
        ;

      el.data('sticky').offset = this.calculate_offset(el, items);
      margin = this.in_viewport(el);
      // Remove the clone if its content no longer inside the viewport
      if (margin === false) {
        this.remove(el);
      }
      // Otherwise inject the clone
      else {
        if(!clone) {
          clone = this.clone($(items[i]), type === 'footer' ? items.slice(i) : items.slice(0, i));
        }

        !clone[0].parentNode && el.parent().append(clone);

        // When the content is close to scrolling away, also scroll the header away
        clone.css('margin' + (type === 'footer' ? 'Bottom' : 'Top'), margin + 'px');
      }
    }
  }

    // Find all sticky-able headers in the document
  , find_items : function(type) {
    var old_items = this['_'+type] || $()
      , items = this['_'+type] = this.element.find(this.options[type + '_selector']).filter(':not(.sticky):visible')
      , self = this
      , increment = type === 'footer' ? -1 : 1
      , i = type === 'footer' ? items.length - 1 : 0
      ;

    // Remove all items that no longer are active
    old_items.not(items).each(function() {
      self.remove($(this));
    });

    // Generate the depth for each header
    for (var $this; $this = items[i]; i += increment) {
      $this = $($this);

      if (!$this.data('sticky')) {
        var data = {
            type: type
          , depth: $this.parents(self.options.depth_selector).length
        };
        $this.data('sticky', data);
      }

      //don't clone yet -- only clone when we need to show the clone
    }

    return items;
  }

    // Determine whether a header's content section is within the scrolling viewport
  , in_viewport : function(el) {
    var data = el.data('sticky')
      , type = data.type
      , parent = el.parent()
      , offset = data.offset || 0
      , pos = parent.position().top
      , margin = pos + parent.outerHeight() - el.outerHeight()
      , scroll_height = this.options.scroll_area.outerHeight()
      ;

    if (type === 'footer') {
      offset = scroll_height - offset;
      margin = offset - pos - el.outerHeight();
    }

    // If the content is in the viewport...
    if (type === 'header' && pos < offset && margin > offset) {
      // Return zero or the amount that the header should start scrolling away if applicable
      margin -= offset;
      return margin <= this.options.margin ? -Math.max(0, this.options.margin - margin) : 0;
    }
    else if (type === 'footer' && pos < scroll_height && (el.position().top + el.outerHeight()) > offset && margin > 0) {
      return margin <= this.options.margin ? -Math.max(0, this.options.margin - margin) : 0;
    }
    else
      return false;
  }

    // Clones (if one doesn't exist) and prepares an item
  , clone : function(el, items) {
    // Compute heights of above items
    var offset = this.calculate_offset(el, items)
      , data = el.data('sticky')
      ;

    data.offset = offset;
    data.clone = data.clone || el.clone(true, true).addClass("sticky sticky-" + data.type);
    return this.position_clone(el);
  }

  , calculate_offset : function(el, items) {
    var data = el.data('sticky')
    , offset = new Array(data.depth + 1)
    , increment = data.type === 'footer' ? -1 : 1
    , depths = {}
    , i = data.type === 'footer' ? items.length - 1 : 0
    , selector = this.selector_of(el, data.type)
    ;

    // Find the number of ancestors that two elements share
    //  (a measure of how close together they are compared to others)
    function common_parents(a, b) {
      return a.first().parents().filter(b.first().parents());
    }

    // Determine the offset based on nested parents
    for (var $this; $this = items[i]; i += increment) {
      if (el[0] === $this) {
        break;
      }
      else {
        $this = $($this);
        var depth = $this.data('sticky').depth
          , depth_selector = this.selector_of($this, data.type) + depth
          , cp = common_parents(el, $this).length
          ;

        // Only add offsets for the closest nested parent of the given depth
        // as well as offsets for the first adjacent sibling of different selectors
        if ((!depths[depth] && depth < data.depth) // if we haven't set up any header for this parent depth yet.
          || (depth <= data.depth   // or if we have (OR we are at the current level)...
              && cp >= (depths[depth] || 0) //...AND the current item is a closer fit for the level (more common ancestors)
              && (el.is(this.options.extra_selector) 
                  && $this.nextAll().is(el) //    ...AND this is an extra header sibling
                  || !$this.is(selector))  //     ...OR a different type of header/footer than the point element
              && !depths[depth_selector])  // ....AND there wasn't a match for this selector at this level yet.
          ) {
            offset[depth] = $this.is(this.options.extra_selector) ? ((offset[depth] || 0) + $this.outerHeight()) : $this.outerHeight();
            depths[depth] = cp
            depths[depth_selector] = true;
        }
      }
    }
    //Add together all the offsets for all the depths.
    return can.reduce(offset, function(a, b) { return a + (b || 0); }, 0);
  }

    // Determine the selector that "selected" a given element
  , selector_of : function(el, type) {
    var selector = '';
    can.each(this.options[type + '_selector'].split(','), function(part) {
      if (el.is(part))
        selector = part;
    });
    return selector;
  }

    // Reposition a clone
  , position_clone : function(el) {
    var data = el.data('sticky');
    return data.clone.css({
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

    // Detach an element's sticky data
  , remove : function(el) {
    var $clone = el.data('sticky').clone;
    $clone && $clone[0].parentNode && $clone.remove();
    $.removeData(el, 'sticky');
  }

    // Clean up when destroyed
  , destroy : function() {
    var items = $().add(this._header || $()).add(this._footer || $())
      , self = this
      ;
    items.each(function() {
      self.destroy($(this));
    });
    delete this._header;
    delete this._footer;
  }
});

})(this.can, this.can.$);
