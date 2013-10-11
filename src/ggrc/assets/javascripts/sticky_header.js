/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: andy@reciprocitylabs.com
    Maintained By: andy@reciprocitylabs.com
*/


(function(can, $) {

can.Control("StickyHeader", {
    defaults: {
        scroll_area: ".object-area"
      , header_selector: "header, .tree-open > .item-open > .item-main"
      , depth_selector: ".tree-open > .item-open"
      , root_header_selector: "header"
      // , margin: 50
    }
}, {
    init : function() {
      this.options = new can.Observe(can.extend(this.options, {
          header: this.element.find(this.options.root_header_selector)
        , scroll_area: typeof this.options.scroll_area === 'string' ? this.element.closest(this.options.scroll_area) : this.options.scroll_area
      }));
      this.on();
    }

  , "{scroll_area} scroll" : function(el, ev) {
    if (!this.options.header.is(":visible"))
      return;

    // Update the header positions
    var headers = this.find_headers();
    for (var i = headers.length - 1; i >= 0; i--) {
      var el = headers.eq(i)
        , clone = el.data('sticky').clone
        ;

      if (this.in_viewport(el)) {
        !clone[0].parentNode && el.parent().append(clone);
      }
      else {
        clone[0].parentNode && clone.remove();
        $.removeData(el, 'sticky');
      }
    }
  }

  , find_headers : function() {
    var headers = this.element.find(this.options.header_selector).filter(':not(.sticky):visible')
      , self = this
      ;
    headers.each(function(i) {
      var $this = $(this);
      if (!$this.data('sticky')) {
        var data = {
          level: $this.parents(self.options.depth_selector).length
        };
        $this.data('sticky', data);
        data.clone = self.clone($this, headers.slice(0, i));
      }
    });

    return headers;
  }

  , position_header : function(el) {
    var level = el.data('sticky').level
      , pos = el.position()
      ;
  }

  , in_viewport : function(el) {
    var parent = el.parent()
      , pos = parent.position()
      , top = this.options.scroll_area[0].scrollTop
      , bottom = top + this.options.scroll_area.outerHeight() 
      , offset = el.data('sticky').offset
      ;

    return pos.top < offset && (pos.top + parent.outerHeight() - el.outerHeight()) > offset;
  }

    // Clones and prepares a header
  , clone : function(el, headers) {
    // Compute heights of above headers
    var offset = 0
      , level = el.data('sticky').level
      ;
    headers.each(function() {
      var $this = $(this);
      if ($this.data('sticky').level < level)
        offset += $this.outerHeight();
    })

    el.data('sticky').offset = offset;
    return el
      .clone(true, true)
      .addClass("sticky")
      .css({
          position: 'fixed'
        , top: (offset + parseFloat(this.options.scroll_area.css("top"))) + 'px'
        , left: el.offset().left + 'px'
        , width: (el[0].getBoundingClientRect().width
            - parseFloat(el.css('paddingLeft')) 
            - parseFloat(el.css('paddingRight'))) 
            + 'px'
      });
  }
});

})(this.can, this.can.$);
