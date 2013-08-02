/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require controls/control
//= require models/cacheable

can.Model.Cacheable("CMS.Models.Section", {
  root_object : "section"
  , root_collection : "sections"
  , category : "governance"
  , root_model : "Section"
  , findAll : "GET /api/sections"
  , create : "POST /api/sections"
  , update : "PUT /api/sections/{id}"
  , attributes : {
    parent : "CMS.Models.Section.model"
    , children : "CMS.Models.Section.models"
    , controls : "CMS.Models.Control.models"
    , objectives : "CMS.Models.Objective.models"
    , control_sections : "CMS.Models.ControlSection.models"
    , section_objectives : "CMS.Models.SectionObjective.models"
    , object_sections : "CMS.Models.ObjectSection.models"
  }
  , tree_view_options : {
    list_view : "/static/mustache/sections/tree.mustache"
    , child_options : [{
      model : can.Model.Cacheable
      , property : "business_objects"
      , list_view : GGRC.mustache_path + "/base_objects/tree.mustache"
      , title_plural : "Business Objects"
    }, {
      model : CMS.Models.Objective
      , property : "objectives"
      , list_view : "/static/mustache/objectives/tree.mustache"
    }, {
      model : CMS.Models.Control
      , property : "controls"
      , list_view : "/static/mustache/controls/tree.mustache"
    }, {
      model : CMS.Models.Section
      , property : "children"
    }]
  }
  , defaults : {
    children : []
    , controls : []
    , objectives : []
    , object_sections : []
    , title : ""
    , slug : ""
    , description : ""
  }
  , findTree : function(params) {
    function filter_out(original, predicate) {
      var target = [];
      for(var i = original.length - 1; i >= 0; i--) {
        if(predicate(original[i])) {
          target.unshift(original.splice(i, 1)[0]);
        }
      }
      return target;
    }

    function treeify(list, directive_id, pid) {
      var ret = filter_out(list, function(s) { 
        return (!s.parent && !pid) || (s.parent.id == pid && (!directive_id || (s.directive && s.directive.id === directive_id)));
      });
      can.$(ret).each(function() {
        this.children = treeify(list, this.directive ? this.directive.id : null, this.id);
      });
      return ret;
    }

    return this.findAll(params).then(
        function(list, xhr) {
          var current;
          can.$(list).each(function(i, s) {
            can.extend(s, s.section);
            delete s.section;
          });
          var roots = treeify(list); //empties the list if all roots (no parent in list) are actually roots (null parent id)
          // for(var i = 0; i < roots.length; i++)
          //   list.push(roots[i]);
          function findRoot(i, v) {
            // find a pseudo-root whose parent wasn't in the returned sections
            if(can.$(list).filter(function(j, c) { return c !== v && v.parent && c.id === v.parent.id && ((!c.directive && !v.directive) || (c.directive && v.directive && c.directive.id === v.directive.id)) }).length < 1) {
              current = v;
              list.splice(i, 1); //remove current from list
              return false;
            }
          }
          while(list.length > 0) {
            can.$(list).each(findRoot);
            current.attr ? current.attr("children", treeify(list, current.id)) : (children = treeify(list, current.id));
            roots.push(current);
          }
          return roots;
        });
  }
  , init : function() {
    this._super.apply(this, arguments);
    this.tree_view_options.child_options[3].model = this;
    this.validatePresenceOf("title");
    this.bind("created updated", function(ev, inst) {
      can.each(this.attributes, function(v, key) {
        (inst.key instanceof can.Observe.List) && inst.key.replace(inst.key); //force redraw in places
      });
    });
  }
  , map_object : function(params, section) {
    var join_ids, joins;

    if(params.u) {
      join_ids = can.map(params.object[params.join_model.root_collection], function(v) {
        return v.id;
      });

      joins = can.map(section[params.join_model.root_collection], function(sc) {
        return ~can.inArray(sc.id, join_ids) ? sc : undefined;
      });

      return $.when.apply($, can.map(joins, function(join) {
        return join.refresh().then(function(j) {
          return j.destroy();
        });
      }));
    } else {
      var j = new params.join_model({
        section : section.stub()
        , context : { id : params.context_id }
      });
      j.attr(params.object.constructor.root_object, params.object.stub());
      return j.save();
    }

  }
  , map_control : function(params, section) {
    var p = $.extend({}, params);
    p.object = p.control;
    p.join_model = CMS.Models.ControlSection;
    delete p.control;
    return this.map_object(p, section);
  }
  , map_objective : function(params, section) {
    var p = $.extend({}, params);
    p.object = p.objective;
    p.join_model = CMS.Models.SectionObjective;
    delete p.objective;
    return this.map_object(p, section);
  }
}, {

  init : function() {

    this._super();

    var that = this;
    this.each(function(value, name) {
      if (value === null)
        that.removeAttr(name);
    });

    this.attr("descendant_sections", can.compute(function() {
      return that.attr("children").concat(can.reduce(that.children, function(a, b) {
        return a.concat(can.makeArray(b.descendant_sections()));
      }, []));
    }));
    this.attr("descendant_sections_count", can.compute(function() {
      return that.attr("descendant_sections")().length;
    }));
    this.attr("business_objects", new can.Model.List(
      can.map(
        this.object_sections,
        function(os) {return os.sectionable || new can.Model({ selfLink : "/" }); }
      )
    ));
    this.object_sections.bind("change", function(ev, attr, how) {
      if(/^(?:\d+)?(?:\.updated)?$/.test(attr)) {
        that.business_objects.replace(
          can.map(
            that.object_sections,
            function(os, i) {
              if(os.sectionable) {
                return os.sectionable;
              } else {
                os.refresh({ "__include" : "sectionable" }).done(function(d) {
                  that.business_objects.attr(i, d.sectionable);
                  //can.Observe.stopBatch();
                }).fail(function() {
                  //can.Observe.stopBatch();
                });
                return new can.Model({ selfLink : "/"});
              }
          })
        );
      }
    });
  }

  , map_control : function(params) {
    return this.constructor.map_control(
      can.extend({}, params, { section : this })
      , this);
  }
  , map_objective : function(params) {
    return this.constructor.map_objective(
      can.extend({}, params, { section : this })
      , this);
  }

});

