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

can.Component.extend({
  tag: "ggrc-quick-add",
  template: "<content/>",
  scope: {
    parent_instance: null,
    source_mapping: null,
    model: null,
    attributes: {}
  },
  events: {
    init: function() {
      var that = this;
      this.scope.attr("controller", this);
      this.element.bind("inserted", function() {
        $(this).find("input:not([data-mapping])").each(function(i, el) {
          that.scope.attributes.attr($(el).attr("name"), $(el).val());
        });
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
    mapping_autocomplete : function(options) {
      return function(el) {
        $(el).ggrc_mapping_autocomplete({ controller : options.contexts.attr("controller") });
      };
    }
  },
});


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
    "input[null-if-empty] change" : function(el) {
      if (!el.val()) {
        this.scope.instance.attr(el.attr("name"), null);
      }
    },
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
