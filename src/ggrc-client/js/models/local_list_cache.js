/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/
;(function(can) {

can.Model.LocalStorage("CMS.Models.LocalListCache", {
  attributes : {
    objects : "modelize",
  }
  , convert : {
    modelize : function(serial) {
      let ml = this.type ? this.type.List : can.List;
      let insts;
      can.batch.start();
      insts = new ml(can.map(serial, function(s) {
        let inst = CMS.Models.get_instance(s);
        if(!inst.selfLink) {
          inst.attr(s); // Add any other attributes in the serial form, like title
        }
        return inst;
      }));
      can.batch.stop();
      return insts;
    },
  }
  , init : function() {
    let that = this
    , _update = this.update;

    this.update = function(id, params) {
      return that.destroy({ id : id }).then(function() {
        return that.create(params);
      });
    };
  },
}, {
  save : function() {
    let that = this
    , ct = this.constructor;

    return ct.findAll({ name : this.name }).then(function(to_del) {
      return $.when.apply($, can.map(to_del, function(d) {
        return d.destroy();
      }));
    }).then(function() {
      return ct.create(that.serialize());
    });
  }
  , serialize : function() {
    let that = this;
    return {
      id : this.id
      , name : this.name
      , type : this.type
      , search_text : this.search_text
      , my_work : this.my_work
      , extra_params: this.extra_params
      , objects : can.map(this.objects || [], function(d) {
        if(that.type && d.constructor.shortName !== that.type)
          return;

        let obj = {
          id : d.id
          , type : that.type
          , href : d.href || d.selfLink || ("/api/" + that.type + "/" + d.id),
        };
        can.each(that.keys, function(key) {
          obj[key] = (d[key] && d[key].serialize) ? d[key].serialize() : d[key];
        });
        return obj;
      })
      , keys : this.keys.serialize ? this.keys.serialize() : this.keys,
    };
  },
});
})(window.can);
