/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//require can.jquery-all

(function(can) {

can.Model.Cacheable("CMS.Models.Program", {
  root_object : "program"
  , root_collection : "programs"
  , category : "programs"
  , findAll : "/api/programs?kind=Directive"
  , create : "POST /api/programs"
  , update : "PUT /api/programs/{id}"
  , destroy : "DELETE /api/programs/{id}"
  , links_to : {
    "Regulation" : "ProgramDirective"
    , "Policy" : "ProgramDirective"
    , "Contract" : "ProgramDirective"
    , "System" : {}
    , "Process" : {}
    //, "Control" 
    , "Product" : {}
    , "Facility" : {}
    , "OrgGroup" : {}
    , "Project" : {}
    , "DataAsset" : {}
    , "Product" : {}
    , "Market" : {}
  }
  , init : function() {
    this.validatePresenceOf("title");
    this._super.apply(this, arguments);
  }
}, {});

can.Model.Cacheable("CMS.Models.Directive", {
  root_object : "directive"
  , root_collection : "directives"
  , category : "governance"
  // `rootModel` overrides `model.shortName` when determining polymorphic types
  , root_model : "Directive"
  , findAll : "/api/directives"
  , create : "POST /api/directives"
  , update : "PUT /api/directives/{id}"
  , destroy : "DELETE /api/directives/{id}"
  , attributes : {
    sections : "CMS.Models.Section.models"
    , program : "CMS.Models.Program.model"
  }
  , serialize : {
    "CMS.Models.Program.model" : function(val, type) {
      return {id : val.id, href : val.selfLink || val.href};
    }
  }
  , defaults : {
    sections : []
  }
  , model : function(attrs) {
    if(!attrs[this.root_object]) {
      attrs = { directive : attrs };
    }
    var kind;
    try {
      kind = GGRC.infer_object_type(attrs);
    } catch(e) {
      console.warn("infer_object_type threw an error on Directive stub (likely no 'kind')");
      kind = CMS.Models.Directive;
    }
    var m = this.findInCacheById(attrs.directive.id);
    if(!m || m.constructor === CMS.Models.Directive) {
      //We accidentally created a Directive or haven't created a subtype yet.
      if(m) {
        delete CMS.Models.Directive.cache[m.id];
        m = this._super.call(kind, $.extend(m.serialize(), attrs));
      } else {
        m = this._super.call(kind, attrs);
      }
      this.cache[m.id] = m;
    } else {
      m = this._super.apply(this, arguments);
    }
    return m;
  }
  , init : function() {
    this.validatePresenceOf("title");
    this.validateInclusionOf("kind", this.meta_kinds);
    this._super.apply(this, arguments);
  }
  , meta_kinds : []
  , links_to : { "Control" : "DirectiveControl", "Program" : "ProgramDirective" }
}, {
  init : function() {
    this._super && this._super.apply(this, arguments);
    var that = this;
    this.attr("descendant_sections", can.compute(function() {
      var sections = [].slice.call(that.attr("sections"), 0);
      return can.reduce(that.sections, function(a, b) {
        return a.concat(can.makeArray(b.descendant_sections()));
      }, sections);
    }));
    this.attr("descendant_sections_count", can.compute(function() {
      return that.attr("descendant_sections")(true).length; //giving it a value to force revalidation
    }));
  }
  , lowercase_kind : function() { return this.kind ? this.kind.toLowerCase() : undefined; }
  , stub : function() {
    return $.extend(this._super(), {kind : this.kind });
  }
});

CMS.Models.Directive("CMS.Models.Regulation", {
  model_plural : "Regulations"
  , table_plural : "regulations"
  , title_plural : "Regulations"
  , model_singular : "Regulation"
  , title_singular : "Regulation"
  , table_singular : "regulation"
  , findAll : "/api/directives?kind=Regulation"
  , defaults : {
    kind : "Regulation"
  }
  , attributes : {
    sections : "CMS.Models.Section.models"
    , program : "CMS.Models.Program.model"
  }
  , serialize : {
    "CMS.Models.Program.model" : function(val, type) {
      return {id : val.id, href : val.selfLink || val.href};
    }
  }
  , meta_kinds : [ "Regulation" ]
  , cache : can.getObject("cache", CMS.Models.Directive, true)
}, {});

CMS.Models.Directive("CMS.Models.Policy", {
  model_plural : "Policies"
  , table_plural : "policies"
  , title_plural : "Policies"
  , model_singular : "Policy"
  , title_singular : "Policy"
  , table_singular : "policy"
  , findAll : "/api/directives?kind__in=Company+Policy,Org+Group+Policy,Data+Asset+Policy,Product+Policy,Contract-Related+Policy,Company+Controls+Policy"
  , defaults : {
    kind : "Company Policy"
  }
  , attributes : {
    sections : "CMS.Models.Section.models"
    , program : "CMS.Models.Program.model"
  }
  , serialize : {
    "CMS.Models.Program.model" : function(val, type) {
      return {id : val.id, href : val.selfLink || val.href};
    }
  }
  , meta_kinds : [  "Company Policy", "Org Group Policy", "Data Asset Policy", "Product Policy", "Contract-Related Policy", "Company Controls Policy" ]
  , cache : can.getObject("cache", CMS.Models.Directive, true)
}, {});

CMS.Models.Directive("CMS.Models.Contract", {
  model_plural : "Contracts"
  , table_plural : "contracts"
  , title_plural : "Contracts"
  , model_singular : "Contract"
  , title_singular : "Contract"
  , table_singular : "contract"
  , findAll : "/api/directives?kind=Contract"
  , defaults : {
    kind : "Contract"
  }
  , attributes : {
    sections : "CMS.Models.Section.models"
    , program : "CMS.Models.Program.model"
  }
  , serialize : {
    "CMS.Models.Program.model" : function(val, type) {
      return {id : val.id, href : val.selfLink || val.href};
    }
  }
  , meta_kinds : [ "Contract" ]
  , cache : can.getObject("cache", CMS.Models.Directive, true)
}, {});

can.Model.Cacheable("CMS.Models.OrgGroup", {
  root_object : "org_group"
  , root_collection : "org_groups"
  , category : "business"
  , findAll : "/api/org_groups"
  , create : "POST /api/org_groups"
  , update : "PUT /api/org_groups/{id}"
  , destroy : "DELETE /api/org_groups/{id}"
  , tree_view_options : {
    list_view : GGRC.mustache_path + "/base_objects/tree.mustache"
    , child_options : [{
      model : null
      , find_params : {
        "destination_type" : "System"
        , "source_type" : "OrgGroup"
        , relationship_type_id : "org_group_has_process"
      }
      , parent_find_param : "source_id"
      , draw_children : true
      , find_function : "findRelated"
      , related_side : "source"
      , create_link : true
    }, {
      model : null
      , find_params : {
        "destination_type" : "OrgGroup"
        , "source_type" : "OrgGroup"
        , relationship_type_id: "org_group_relies_upon_org_group"
      }
      , parent_find_param : "destination_id"
      , draw_children : true
      , start_expanded : false
      , find_function : "findRelatedSource"
      , related_side : "destination"
      , single_object : false
      , create_link : true
    }]}
  , links_to : {
    "System" : {}
    , "Process" : {}
    , "Program" : {}
    , "Product" : {}
    , "Facility" : {}
    , "OrgGroup" : {}
    , "Project" : {}
    , "DataAsset" : {}
    , "Market" : {}
    }
  , init : function() {
    var that = this;
    this._super && this._super.apply(this, arguments);
    $(function(){
      that.tree_view_options.child_options[0].model = CMS.Models.Process;
    });
    this.tree_view_options.child_options[1].model = this;
    this.risk_tree_options.child_options[1] = can.extend(true, {}, this.tree_view_options.child_options[1]);
    this.risk_tree_options.child_options[1].create_link = false;

    this.validatePresenceOf("title");
  }
}, {});

can.Model.Cacheable("CMS.Models.Project", {
  root_object : "project"
  , root_collection : "projects"
  , category : "business"
  , findAll : "/api/projects"
  , create : "POST /api/projects"
  , update : "PUT /api/projects/{id}"
  , destroy : "DELETE /api/projects/{id}"
  , tree_view_options : {
    list_view : GGRC.mustache_path + "/base_objects/tree.mustache"
    , child_options : [{
      model : null
      , find_params : {
        "destination_type" : "System"
        , "source_type" : "Project"
        , relationship_type_id : "project_has_process"
      }
      , parent_find_param : "source_id"
      , draw_children : true
      , find_function : "findRelated"
      , related_side : "source"
      , create_link : true
    }]}
  , links_to : {
    "System" : {}
    , "Process" : {}
    , "Program" : {}
    , "Product" : {}
    , "Facility" : {}
    , "OrgGroup" : {}
    , "Project" : {}
    , "DataAsset" : {}
    , "Market" : {}
    }
  , init : function() {
    var that = this;
    this._super && this._super.apply(this, arguments);
    this.risk_tree_options.child_options.splice(1, 1);
    $(function(){
      that.tree_view_options.child_options[0].model = CMS.Models.Process;
    });

    this.validatePresenceOf("title");
  }
}, {});

can.Model.Cacheable("CMS.Models.Facility", {
  root_object : "facility"
  , root_collection : "facilities"
  , category : "business"
  , findAll : "/api/facilities"
  , create : "POST /api/facilities"
  , update : "PUT /api/facilities/{id}"
  , destroy : "DELETE /api/facilities/{id}"
  , tree_view_options : {
    list_view : GGRC.mustache_path + "/base_objects/tree.mustache"
    , child_options : [{
      model : null
      , find_params : {
        "destination_type" : "System"
        , "source_type" : "Facility"
        , relationship_type_id : "facility_has_process"
      }
      , parent_find_param : "source_id"
      , draw_children : true
      , find_function : "findRelated"
      , related_side : "source"
      , create_link : true
    }, {
      model : null
      , find_params : {
        "destination_type" : "Facility"
        , "source_type" : "Facility"
        , relationship_type_id: "facility_relies_upon_facility"
      }
      , parent_find_param : "destination_id"
      , draw_children : true
      , start_expanded : false
      , find_function : "findRelatedSource"
      , related_side : "destination"
      , single_object : false
      , create_link : true
    }]}
  , links_to : {
    "System" : {}
    , "Process" : {}
    , "Program" : {}
    , "Product" : {}
    , "Facility" : {}
    , "OrgGroup" : {}
    , "Project" : {}
    , "DataAsset" : {}
    , "Market" : {}
    }
  , init : function() {
    var that = this
    this._super && this._super.apply(this, arguments);
    $(function(){
      that.tree_view_options.child_options[0].model = CMS.Models.Process;
    });
    this.tree_view_options.child_options[1].model = this;
    this.risk_tree_options.child_options[1] = can.extend(true, {}, this.tree_view_options.child_options[1]);
    this.risk_tree_options.child_options[1].create_link = false;

    this.validatePresenceOf("title");
  }
}, {});

can.Model.Cacheable("CMS.Models.Product", {
  root_object : "product"
  , root_collection : "products"
  , category : "business"
  , findAll : "/api/products"
  , create : "POST /api/products"
  , update : "PUT /api/products/{id}"
  , destroy : "DELETE /api/products/{id}"
  , attributes : {
    type : "CMS.Models.Option.model"
  }
  , defaults : {
    type : {}
  }
  , tree_view_options : {
    list_view : GGRC.mustache_path + "/base_objects/tree.mustache"
    , child_options : [{
      model : null
      , find_params : {
        "destination_type" : "System"
        , "source_type" : "Product"
        , relationship_type_id : "product_has_process"
      }
      , parent_find_param : "source_id"
      , draw_children : true
      , find_function : "findRelated"
      , related_side : "source"
      , create_link : true
    }, {
      model : null
      , find_params : {
        "destination_type" : "Product"
        , "source_type" : "Product"
        , relationship_type_id: "product_relies_upon_product"
      }
      , parent_find_param : "destination_id"
      , draw_children : true
      , start_expanded : false
      , find_function : "findRelatedSource"
      , related_side : "destination"
      , single_object : false
      , create_link : true
    }]}
  , links_to : {
    "System" : {}
    , "Process" : {}
    , "Program" : {}
    , "Product" : {}
    , "Facility" : {}
    , "OrgGroup" : {}
    , "Project" : {}
    , "DataAsset" : {}
    , "Product" : {}
    , "Market" : {}
    }
  , init : function() {
    var that = this
    this._super && this._super.apply(this, arguments);
    $(function(){
      that.tree_view_options.child_options[0].model = CMS.Models.Process;
    });
    this.tree_view_options.child_options[1].model = this;
    this.risk_tree_options.child_options[1] = can.extend(true, {}, this.tree_view_options.child_options[1]);
    this.risk_tree_options.child_options[1].create_link = false;

    this.validatePresenceOf("title");
  }
}, {
  attr : function(key, val) {
    if(key === "type" && typeof val === "undefined" && this[key] && !this[key].selfLink) {
      this[key].refresh();
    }
    return this._super.apply(this, arguments);
  }
});

can.Model.Cacheable("CMS.Models.Option", {
  root_object : "option"
  , root_collection : "options"
}, {});

can.Model.Cacheable("CMS.Models.DataAsset", {
  root_object : "data_asset"
  , root_collection : "data_assets"
  , category : "business"
  , findAll : "/api/data_assets"
  , create : "POST /api/data_assets"
  , update : "PUT /api/data_assets/{id}"
  , destroy : "DELETE /api/data_assets/{id}"
  , tree_view_options : {
    list_view : GGRC.mustache_path + "/base_objects/tree.mustache"
    , child_options : [{
      model : null
      , find_params : {
        "destination_type" : "System"
        , "source_type" : "DataAsset"
        , relationship_type_id : "data_asset_has_process"
      }
      , parent_find_param : "source_id"
      , draw_children : true
      , find_function : "findRelated"
      , related_side : "source"
      , create_link : true
    }, {
      model : null
      , find_params : {
        "destination_type" : "DataAsset"
        , "source_type" : "DataAsset"
        , relationship_type_id: "data_asset_relies_upon_data_asset"
      }
      , parent_find_param : "destination_id"
      , draw_children : true
      , start_expanded : false
      , find_function : "findRelatedSource"
      , related_side : "destination"
      , single_object : false
      , create_link : true
    }]}
  , links_to : {
    "System" : {}
    , "Process" : {}
    , "Program" : {}
    , "Product" : {}
    , "Facility" : {}
    , "OrgGroup" : {}
    , "Project" : {}
    , "DataAsset" : {}
    , "Market" : {}
    }
  , init : function() {
    var that = this;
    this._super && this._super.apply(this, arguments);
    $(function(){
      that.tree_view_options.child_options[0].model = CMS.Models.Process;
    });
    this.tree_view_options.child_options[1].model = this;
    this.risk_tree_options.child_options[1] = can.extend(true, {}, this.tree_view_options.child_options[1]);
    this.risk_tree_options.child_options[1].create_link = false;

    this.validatePresenceOf("title");
  }
}, {});

can.Model.Cacheable("CMS.Models.Market", {
  root_object : "market"
  , root_collection : "markets"
  , category : "business"
  , findAll : "/api/markets"
  , create : "POST /api/markets"
  , update : "PUT /api/markets/{id}"
  , destroy : "DELETE /api/markets/{id}"
  , tree_view_options : {
    list_view : GGRC.mustache_path + "/base_objects/tree.mustache"
    , child_options : [{
      model : null
      , find_params : {
        "destination_type" : "System"
        , "source_type" : "Market"
        , relationship_type_id : "market_has_process"
      }
      , parent_find_param : "source_id"
      , draw_children : true
      , find_function : "findRelated"
      , related_side : "source"
      , create_link : true
    }]}
  , links_to : {
    "System" : {}
    , "Process" : {}
    , "Program" : {}
    , "Product" : {}
    , "Facility" : {}
    , "OrgGroup" : {}
    , "Project" : {}
    , "DataAsset" : {}
    , "Market" : {}
    }
  , init : function() {
    var that = this;
    this._super && this._super.apply(this, arguments);
    this.risk_tree_options.child_options.splice(1, 1);
    $(function(){
      that.tree_view_options.child_options[0].model = CMS.Models.Process;
    });

    this.validatePresenceOf("title");
  }
}, {});

can.Model.Cacheable("CMS.Models.RiskyAttribute", {
  root_object : "risky_attribute"
  , root_collection : "risky_attributes"
  , category : "risk"
  , findAll : "/api/risky_attributes"
  , create : "POST /api/risky_attributes"
  , update : "PUT /api/risky_attributes/{id}"
  , destroy : "DELETE /api/risky_attributes/{id}"
  , links_to : ["Risk"]
  , init : function() {
    this.validatePresenceOf("title");
    this._super.apply(this, arguments);
  }
}, {});

can.Model.Cacheable("CMS.Models.Risk", {
  root_object : "risk"
  , root_collection : "risks"
  , category : "risk"
  , findAll : function(params) {
    var root_object =  this.root_object
    , root_collection = this.root_collection;
    return $.ajax({
      url : "/api/risks"
      , type : "get"
      , data : params
      , dataType : "json"
    }).then(function(risks) {
      if(risks[root_collection + "_collection"]) {
        risks = risks[root_collection + "_collection"];
      }
      if(risks[root_collection]) {
        risks = risks[root_collection];
      }

      can.each(risks, function(r) {
        if(r[root_object]) {
          r = r[root_object];
        }
        if(r.hasOwnProperty("trigger")) {
          r.risk_trigger = r.trigger;
          delete r.trigger;
        }
      });
      return risks;
    });
  }
  , update : "PUT /api/risks/{id}"
  , destroy : "DELETE /api/risks/{id}"
  , create : function(params) {
    params.trigger = params.risk_trigger;
    return $.ajax({
      type : "POST"
      , url : "/api/risks"
      , data : params
      , dataType : "json"
    });
  }
  , risk_tree_options : { list_view : GGRC.mustache_path + "/risks/tree.mustache", child_options : [], draw_children : false}
  , tree_view_options : {
    list_view : GGRC.mustache_path + "/risks/tree.mustache"
    , child_options : [{
      model : null
      , property : "controls"
      , create_link : true
      , draw_children : false
      , start_expanded : false
    }, {
      model : CMS.Models.RiskyAttribute
      , property : "risky_attributes"
      , draw_children : false
      , start_expanded : false
      , create_link : true
    }]}
  , links_to : {
    "System" : {}
    , "Process" : {}
    , "Product" : {}
    , "Facility" : {}
    , "OrgGroup" : {}
    , "Project" : {}
    , "DataAsset" : {}
    , "Market" : {}
    , "RiskyAttribute" : "RiskRiskyAttribute"
    }
  , init : function() {
    var that = this;
    this._super && this._super.apply(this, arguments);
    $(function() {
      that.tree_view_options.child_options[0].model = CMS.Models.Control;
    });

    this.validatePresenceOf("title");
  }
}, {});

can.Model.Cacheable("CMS.Models.Objective", {
  root_object : "objective"
  , root_collection : "objectives"
  , category : "governance"
  , title_singular : "Control Objective"
  , title_plural : "Control Objectives"
  , findAll : "GET /api/objectives"
  , create : "POST /api/objectives"
  , update : "PUT /api/objectives/{id}"
  , destroy : "DELETE /api/objectives/{id}"
  , links_to : {
      "Section" : "SectionObjective"
  }
  , init : function() {
    this.validatePresenceOf("title");
    this._super.apply(this, arguments);
  }
}, {});

can.Model.Cacheable("CMS.Models.Help", {
  root_object : "help"
  , root_collection : "helps"
  , findAll : "GET /api/help"
  , update : "PUT /api/help/{id}"
  , destroy : "DELETE /api/help/{id}"
  , create : "POST /api/help"
}, {});

can.Model.Cacheable("CMS.Models.Event", {
  root_object : "event"
  , root_collection : "events"
  , findAll : "GET /api/events?__include=revisions,modified_by"
}, {});

can.Model.Cacheable("CMS.Models.Role", {
  root_object : "role"
  , root_collection : "roles"
  , findAll : "GET /api/roles"
  , update : "PUT /api/roles/{id}"
  , destroy : "DELETE /api/roles/{id}"
  , create : "POST /api/roles"
}, {});

CMS.Models.Role.prototype.allowed = function(operation, object_or_class) {
  var cls = typeof object_or_class === "function" ? object_or_class : object_or_class.constructor;
  return !!~can.inArray(cls.model_singular, this.permissions[operation]);
};

CMS.Models.get_instance = function(object_type, object_id, params_or_object) {
  var model = CMS.Models[object_type]
    , params = {}
    , instance = null
    ;

  if (!model)
    return null;

  if (!object_id)
    return null;

  if (!!params_or_object) {
    if ($.isFunction(params_or_object.serialize))
      $.extend(params, params_or_object.serialize());
    else
      $.extend(params, params_or_object || {});
  }

  instance = model.findInCacheById(object_id);
  if (!instance) {
    if (params.selfLink) {
      params.id = object_id;
      instance = new model(params);
    } else
      instance = new model({
          id: object_id
        , href: (params_or_object || {}).href
        });
  }
  return instance;
};

CMS.Models.get_link_type = function(instance, attr) {
  var type
    , model
    ;

  type = instance[attr + "_type"];
  if (!type) {
    model = instance[attr] && instance[attr].constructor;
    if (model)
      type = model.getRootModelName();
    else if (instance[attr])
      type = instance[attr].type;
  }
  return type;
};

})(this.can);
