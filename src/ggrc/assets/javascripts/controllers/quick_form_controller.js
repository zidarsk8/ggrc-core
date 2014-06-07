/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/

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


can.Component.extend({
  tag: "ggrc-quick-add",
  template: "<content/>",
  scope: {
    parent_instance: null,
    source_mapping: null,
    model: null,
  },
  events: {
    init: function() {
      this.scope.attr("controller", this);
    },
    "a[data-toggle=submit]:not(.disabled) click": function(el){
      var that = this,
        far_model = this.scope.model || this.scope.instance.constructor;
      GGRC.Mappings.make_join_object(
        this.scope.parent_instance,
        this.scope.instance,
        { context : this.scope.parent_instance.context }
      ).save().done(function() {
        el.trigger("modal:success");
      });
    },
    autocomplete_select : function(el, event, ui) {
      var that = this;
      setTimeout(function() {
        that.scope.attr(el.attr("name"), ui.item);
      });
    },
    "input[data-mapping] change" : function(el) {
      if (!el.val()) {
        this.scope.attr(el.attr("name"), null);
      }
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
