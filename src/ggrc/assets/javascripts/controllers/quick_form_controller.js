/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/
;(function(cam, $, GGRC) {

GGRC.Controllers.Modals("GGRC.Controllers.QuickForm", {
  defaults : {
    model: null,
    instance: null
  }
}, {
  init: function () {
    if(this.options.instance && !this.options.model) {
      this.options.model = this.options.instance.constructor;
    }
    this.options.$content = this.element;
    if (this.element.data("force-refresh")) {
      this.options.instance.refresh();
    }
  },
  "input, textarea, select change": function (el, ev) {
    if (el.data("toggle") === "datepicker") {
      var val = el.datepicker("getDate"),
          prop = el.attr("name"),
          old_value = this.options.instance.attr(prop);

          if (moment(val).isSame(old_value)) {
            return;
          }
          $.when(this.options.instance.refresh()).then(function () {
            this.options.instance.attr(prop, val);
            this.options.instance.save();
          }.bind(this));
      return;
    }
    if (!el.is("[data-lookup]")) {
      this.set_value_from_element(el);
      setTimeout(function () {
        this.options.instance.save();
      }.bind(this), 100);
    }
  },
  autocomplete_select: function (el, event, ui) {
    var prop = el.attr("name").split(".").slice(0, -1).join(".");
    if (this._super.apply(this, arguments) !== false) {
      setTimeout(function () {
        this.options.instance.save().then(function () {
          var obj = this.options.instance.attr(prop);
          if (obj && obj.attr) {
            obj.attr("saved", true);
          }
        }.bind(this));
      }.bind(this), 100);
    } else {
      return false;
    }
  },
  "input, select, textarea click": function (el, ev) {
    if (el.data("toggle") === "datepicker") {
      return;
    }
    this._super && this._super.apply(this, arguments);
    ev.stopPropagation();
  },
  ".dropdown-menu > li click": function (el, ev) {
    ev.stopPropagation();
    var that = this;
    this.set_value({ name: el.data('name'), value: el.data('value') });
    setTimeout(function() {
      that.options.instance.save();
      $(el).closest(".open").removeClass("open");
    }, 100);
  }

  , "button[data-name][data-value]:not(.disabled), a.undoable[data-toggle*=modal] click": function(el, ev) {

    var that = this
      , name = el.data('name')
      , old_value = {};


    if(el.data('openclose')){
      var action = el.data('openclose'),
          main = el.closest('.item-main'),
          openclose = main.find('.openclose'),
          isOpened = openclose.hasClass('active');

      // We can't use main.openclose(action) here because content may not be loaded yet
      if(action === 'trigger'){
        openclose.trigger('click');
      }
      else if(action === 'close' && isOpened){
        openclose.trigger('click');
      }
      else if(action === 'open' && !isOpened){
        openclose.trigger('click');
      }
    }

    old_value[el.data("name")] = this.options.instance.attr(el.data("name"));
    if(el.data("also-undo")) {
      can.each(el.data("also-undo").split(","), function(attrname) {
        attrname = attrname.trim();
        old_value[attrname] = that.options.instance.attr(attrname);
      });
    }

    // Check if the undo button was clicked:
    this.options.instance.attr('_undo') || that.options.instance.attr('_undo', []);

    if(el.is("[data-toggle*=modal")) {
      setTimeout(function() {
        $(".modal:visible").one("modal:success", function() {
          that.options.instance.attr('_undo').unshift(old_value);
        });
      }, 100);
    } else {
      ev.stopPropagation();
      that.options.instance.attr('_undo').unshift(old_value);

    that.options.instance.attr('_disabled', 'disabled');
    that.options.instance.refresh().then(function(instance){
      that.set_value({ name: el.data('name'), value: el.data('value') });
      return instance.save();
    }).then(function(){
      that.options.instance.attr('_disabled', '');
    });
  }
  }


  , "a.undo click" : function(el, ev){
    ev.stopPropagation();
    var that = this
      , name = el.data('name')
      , old_value = this.options.instance.attr(name) || "";

    new_value = that.options.instance.attr('_undo').shift();
    that.options.instance.attr('_disabled', 'disabled');
    that.options.instance.refresh().then(function(instance){
      can.each(new_value, function(value, name) {
        that.set_value({ name: name, value: value });
      });
      return instance.save();
    }).then(function(){
      that.options.instance.attr('_disabled', '');
    });
  }
});
})(this.can, this.can.$, this.GGRC);
