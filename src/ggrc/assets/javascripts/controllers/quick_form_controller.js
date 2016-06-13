/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
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
          if (obj.attr) {
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

/*
  This component is for quickly updating the properties of an object through form fields.
  It works similar to GGRC.Controllers.QuickForm but has an extra feature: if the instance
  we're working with is a join object, and the option type is changed, it will work around
  the lack of support in proxy mappers for join objects being changed like that, and
  destroy the join object while creating a new one.

  Field updates trigger updates to the model automatically, even on the server.  This differs
  from the quick-add component above, in that it is not waiting for a submit trigger.
*/
can.Component.extend({
  tag: "ggrc-quick-update",
  template: "<content/>",
  scope: {
    instance: null,
    source_mapping: null,
    model: null,
    attributes: {}
  },
  events: {
    init: function() {
      this.scope.attr("controller", this);
      this.scope.attr("model", this.scope.model || this.scope.instance.constructor);
      if(!this.scope.instance._transient) {
        //only refresh if there's not currently an edit modal spawned.
        this.scope.instance.refresh();
      }
    },
    //currently we don't support proxy object updates in mappings, so for now a change
    //  to a connected object (assuming we are operating on a proxy object) will trigger
    //  a deletion of the proxy object and creation of a new one.
    autocomplete_select : function(el, event, ui) {
      var that = this;
      setTimeout(function() {
        var serial = that.scope.instance.serialize();
        delete serial[el.attr("name")];
        delete serial[el.attr("name") + "_id"];
        delete serial[el.attr("name") + "_type"];
        delete serial.id;
        delete serial.href;
        delete serial.selfLink;
        delete serial.created_at;
        delete serial.updated_at;
        delete serial.provisional_id;
        serial[el.attr("name")] = ui.item.stub();
        that.scope.instance.destroy().then(function() {
          new that.scope.model(serial).save();
        });
      });
    },
    // null-if-empty attributes are a pattern carried over from GGRC.Controllers.Modals
    //  Useful for connected objects.
    "input[null-if-empty] change" : function(el) {
      if (!el.val()) {
        this.scope.instance.attr(el.attr("name"), null);
      }
    },
    // data-mapping is the element decoration that triggers an autocomplete based on a
    //  mapping to a parent instance.  The mapping_autocomplete helper defined below is
    //  generally for these.
    "input:not([data-mapping]), select change" : function(el) {
      var isCheckbox = el.is("[type=checkbox][multiple]");
      if (isCheckbox) {
        if(!this.scope.instance[el.attr("name")]) {
          this.scope.instance.attr(el.attr("name"), new can.List());
        }
        this.scope.instance
        .attr(el.attr("name"))
        .replace(
          can.map(
            this.element.find("input[name='" + el.attr("name") + "']:checked"),
            function(el) {
              return $(el).val();
            }
          )
        );
        this.element.find("input:checkbox").prop("disabled", true);
      } else {
        this.scope.instance.attr(el.attr("name"), el.val());
      }
      this.scope.instance.save().then(function () {
        if (isCheckbox) {
          this.element.find("input:checkbox").prop("disabled", false);
        }
      }.bind(this));
    },
  },
  helpers: {
    mapping_autocomplete : function(options) {
      return function(el) {
        $(el).ggrc_mapping_autocomplete({ controller : options.contexts.attr("controller") });
      };
    }
  },
});

})(this.can, this.can.$, this.GGRC);
