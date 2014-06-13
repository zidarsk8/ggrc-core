/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/
;(function(cam, $, GGRC) {

GGRC.Controllers.Modals("GGRC.Controllers.QuickForm", {
  defaults : {
    model : null
    , instance : null
  }
}, {

  init : function() {
    if(this.options.instance && !this.options.model) {
      this.options.model = this.options.instance.constructor;
    }
    this.options.$content = this.element;
    this.options.instance.refresh();
  }

  , "input, textarea, select change" : function(el, ev) {
    var that = this;
    if(!el.is("[data-lookup]")) {
      this.set_value_from_element(el);
      setTimeout(function() {
        that.options.instance.save();
      }, 100);
    }
  }

  , autocomplete_select : function(el, event, ui) {
    var that = this;
    var prop = el.attr("name").split(".").slice(0, -1).join(".");
    if(this._super.apply(this, arguments) !== false) {
      setTimeout(function() {
        that.options.instance.save().then(function() {
          var obj = that.options.instance.attr(prop);
          if(obj.attr) {
            obj.attr("saved", true);
          }
        });
      }, 100);
    } else {
      return false;
    }
  }

  , "input, select, textarea click" : function(el, ev) {
    this._super && this._super.apply(this, arguments);
    ev.stopPropagation();
  }
  
  , ".dropdown-menu > li click" : function(el, ev){
    ev.stopPropagation();
    var that = this;
    this.set_value({ name: el.data('name'), value: el.data('value') });
    setTimeout(function() {
      that.options.instance.save();
      $(el).closest('.open').removeClass('open');
    }, 100);
  }
  , "button,a.undo click" : function(el, ev){
    ev.stopPropagation();
    if(!el.data('name') || !el.data('value') || $(el).hasClass('disabled')){
      return;
    }
    var that = this
      , name = el.data('name')
      , old_value = this.options.instance.attr(name);

    // Check if the undo button was clicked:
    this.options.instance.attr('_undo') || that.options.instance.attr('_undo', []);
    if(!el.data('undo')){
      that.options.instance.attr('_undo').unshift(old_value);
    }
    else{
      that.options.instance.attr('_undo').shift();
    }
    that.options.instance.attr('_disabled', 'disabled');
    that.options.instance.refresh().then(function(instance){ 
      that.set_value({ name: el.data('name'), value: el.data('value') });
      return instance.save();
    }).then(function(){
      that.options.instance.attr('_disabled', '');
    });
  }

});

/*
  Below this line we're defining a few can.Components, which are in this file
  because they work similarly to the quick form controller (in fact, you should
  expect the quick form controller to be refactored into a component in the 
  future) but they share no code with the quick form controller.

  the first component is quick add.  It is meant to have one or more form elements
  and a data-toggle="submit" link which will create a new join object between
  the parent instance and some selected option instance (likely picked through an 
  autocomplete dropdown).

  Technically you can choose your instance however you want, as long as you find
  some way of getting its value into the component scope.  Extending this component
  with other methods to do that is fine.  You can also just pass it in when 
  instantiating the component.
*/
can.Component.extend({
  tag: "ggrc-quick-add",
  // <content> in a component template will be replaced with whatever is contained
  //  within the component tag.  Since the views for the original uses of these components
  //  were already created with content, we just used <content> instead of making
  //  new view template files.
  template: "<content/>",
  scope: {
    parent_instance: null,
    source_mapping: null,
    model: null,
    attributes: {}
  },
  events: {
    init: function() {
      this.scope.attr("controller", this);
    },
    // The inserted event fires when the component content is added to the DOM.
    //  At this time, live bound rendering should be resolved, which is not the
    //  case during init.
    inserted: function(el) {
      var that = this;
      this.element.find("input:not([data-mapping])").each(function(i, el) {
        that.scope.attributes.attr($(el).attr("name"), $(el).val());
      });
    },
    "a[data-toggle=submit]:not(.disabled) click": function(el){
      var that = this,
        far_model = this.scope.model || this.scope.instance.constructor;
      GGRC.Mappings.make_join_object(
        this.scope.parent_instance,
        this.scope.instance || this.scope.attributes.instance,
        $.extend({
          context : this.scope.parent_instance.context
                    || new CMS.Models.Context({id : null})
                  },
                  this.scope.attributes.serialize())
      ).save().done(function() {
        el.trigger("modal:success");
      });
    },
    // this works like autocomplete_select on all modal forms and 
    //  descendant class objects.
    autocomplete_select : function(el, event, ui) {
      var that = this;
      setTimeout(function() {
        that.scope.attr(el.attr("name"), ui.item);
      });
    },
    "input[null-if-empty] change" : function(el) {
      if (!el.val()) {
        this.scope.attributes.attr(el.attr("name"), null);
      }
    },
    "input:not([data-mapping]) change" : function(el) {
      this.scope.attributes.attr(el.attr("name"), el.val());
    }
  },
  helpers: {
    // Mapping-based autocomplete selectors use this helper to 
    //  attach the mapping autocomplete ui widget.  These elements should
    //  be decorated with data-mapping attributes.
    mapping_autocomplete : function(options) {
      return function(el) {
        $(el).ggrc_mapping_autocomplete({ controller : options.contexts.attr("controller") });
      };
    }
  },
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
      this.scope.instance.refresh();
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
          new that.scope.instance.constructor(serial).save();
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
    "input:not([data-mapping]) change" : function(el) {
      this.scope.instance.attr(el.attr("name"), el.val());
      this.scope.instance.save();
    }
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
