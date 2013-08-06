/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

can.Model("GGRC.Models.Search", {

  findOne : "GET /search"
  , search : function(str, params) {
    return this.findOne($.extend({q : str}, params));
  }
  , search_for_types : function(str, types, params) {
    return this.findOne($.extend({q : str, types : types.join(",") }, params));
  }
  , counts : function(str, params) {
    return this.findOne($.extend({q : str, counts_only : true}, params));
  }
  , counts_for_types : function(str, types, params) {
    return this.findOne(
      $.extend({q: str, types: types.join(","), counts_only: true }, params));
  }
  , init : function() {
    this._super && this._super.apply(this, arguments);
    var _findOne = this.findOne;
    this.findOne = function() {
      return _findOne.apply(this, arguments).then(function(data) {
        if (data.results.entries)
          data.attr("entries", data.results.entries);
        if (data.results.counts)
          data.attr("counts", data.results.counts);
        data.removeAttr("results");
        return data;
      });
    };
  }
}, {

  getResultsFor : function(type) {
    var _class = type.shortName
      ? type
      : (can.getObject("CMS.Models." + type) || can.getObject("GGRC.Models." + type));

    type = _class.shortName;
    return can.map(
      this.entries
      , function(v) {
        var inst;
        if(v.type === type) {
          inst = new _class({id : v.id});
          // if(!inst.selfLink) {
          //   inst.attr("selfLink", v.href);
          //   inst.refresh();
          // }
          return inst;
        }
    });
  }

  , getResultsForType : function(model_name) {
      var model = CMS.Models[model_name]
        , entries;

      if (this.entries instanceof Array)
        entries = this.entries[model_name] || [];
      else
        entries = can.map(this.entries, function(v) {
          if (v.type == model_name)
            return v;
        });

      return can.map(entries, function(stub) {
        return new model({ id: stub.id });
      });
  }

  , getCountFor : function(type) {
      if (type && type.shortName)
        type = type.shortName;

      if (!this.counts[type])
        return 0;
      else
        return this.counts[type];
  }
});
