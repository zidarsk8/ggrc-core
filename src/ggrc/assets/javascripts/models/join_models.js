(function(can, $) {

can.Model.Cacheable("can.Model.Join", {
  join_keys : null
  , setup : function() {
    this._super.apply(this, arguments);
  }
}, {
  getOtherSide : function(obj) {
    var that = this;
    var keys = $.extend({}, this.constructor.join_keys);
    can.each(keys, function(cls, key) {
      if((that[key] && that[key] === obj)
        || (that[key] ? that[key].id : that[key + "_id"]) === obj.id
            && (obj instanceof cls || obj.type === cls.model_singular)
      ) {
        delete keys[key];
      }
    });
    keys = Object.keys(keys);
    if(keys.length === 1) {
      return this[keys[0]];
    } else {
      return null;
    }
  }
});

can.Model.Join("CMS.Models.Relationship", {
    root_object: "relationship"
  , root_collection: "relationships"
  , join_keys : {
    source : can.Model.Cacheable
    , destination : can.Model.Cacheable
  }
  , findAll: "GET /api/relationships"
  , create: "POST /api/relationships"
  , destroy: "DELETE /api/relationships/{id}"
}, {
  init: function() {
    var _super = this._super;
    function reinit() {
      var that = this;

      typeof _super === "function" && _super.call(this);
      this.attr("source", CMS.Models.get_instance(
        this.source_type || this.source.type
        , this.source_id || this.source.id
        , this.source) || this.source);
      this.attr("destination", CMS.Models.get_instance(
        this.destination_type || this.destination.type
        , this.destination_id || this.destination.id
        , this.destination) || this.destination);

      this.each(function(value, name) {
        if (value === null)
        that.removeAttr(name);
      });
    }

    this.bind("created", can.proxy(reinit, this));

    reinit.call(this);
  }
});

can.Model.Join("CMS.Models.ProgramDirective", {
  root_object : "program_directive"
  , root_collection : "program_directives"
  , join_keys : {
    "program" : CMS.Models.Program
    , "directive" : CMS.Models.Directive
  }
  , create: "POST /api/program_directives"
  , destroy : "DELETE /api/program_directives/{id}"
}, {
  init : function() {
    var _super = this._super;
    function reinit() {
      var that = this;

      typeof _super === "function" && _super.call(this);
      this.attr("program", CMS.Models.get_instance(
        "Program",
        this.program_id || (this.program && this.program.id)));
      this.attr("directive", CMS.Models.get_instance(
        (this.directive ? this.directive.type : "Directive"),
        this.directive_id || (this.directive && this.directive.id)));

      this.each(function(value, name) {
        if (value === null)
        that.removeAttr(name);
      });
    }

    this.bind("created", can.proxy(reinit, this));

    reinit.call(this);
  }
});

can.Model.Cacheable("CMS.Models.ObjectiveControl", {
  root_object : "objective_control"
  , root_collection : "objective_controls"
  , join_keys : {
      "objective" : CMS.Models.Objective
    , "control" : CMS.Models.Control
    }
  , findAll: "GET /api/objective_controls"
  , create: "POST /api/objective_controls"
  , destroy : "DELETE /api/objective_controls/{id}"
}, {
  init : function() {
    var _super = this._super;
    function reinit() {
      var that = this;

      typeof _super === "function" && _super.call(this);
      this.attr("objective", CMS.Models.get_instance(
        "Objective",
        this.objective_id || (this.objective && this.objective.id)));
      this.attr("control", CMS.Models.get_instance(
        "Control",
        this.control_id || (this.control && this.control.id)));

      this.each(function(value, name) {
        if (value === null)
        that.removeAttr(name);
      });
    }

    this.bind("created", can.proxy(reinit, this));

    reinit.call(this);
  }
});

can.Model.Cacheable("CMS.Models.SectionObjective", {
  root_object : "section_objective"
  , root_collection : "section_objectives"
  , join_keys : {
      "section" : CMS.Models.Section
    , "objective" : CMS.Models.Objective
    }
  , findAll: "GET /api/section_objectives"
  , create: "POST /api/section_objectives"
  , destroy : "DELETE /api/section_objectives/{id}"
}, {
  init : function() {
    var _super = this._super;
    function reinit() {
      var that = this;

      typeof _super === "function" && _super.call(this);
      this.attr("section", CMS.Models.get_instance(
        "Section",
        this.section_id || (this.section && this.section.id)));
      this.attr("objective", CMS.Models.get_instance(
        "Objective",
        this.objective_id || (this.objective && this.objective.id)));

      this.each(function(value, name) {
        if (value === null)
        that.removeAttr(name);
      });
    }

    this.bind("created", can.proxy(reinit, this));

    reinit.call(this);
  }
});

can.Model.Join("CMS.Models.SystemControl", {
  root_object : "system_control"
  , root_collection : "system_controls"
  , join_keys : {
    "system" : CMS.Models.System
    , "control" : CMS.Models.Control
  }
  , findAll: "GET /api/system_controls"
  , create: "POST /api/system_controls"
  , destroy : "DELETE /api/system_controls/{id}"
}, {
  init : function() {
    var _super = this._super;
    function reinit() {
      var that = this;

      typeof _super === "function" && _super.call(this);
      this.attr("system", CMS.Models.get_instance(
        "System",
        this.system_id || (this.system && this.system.id)));
      this.attr("control", CMS.Models.get_instance(
        "Control",
        this.control_id || (this.control && this.control.id)));

      this.each(function(value, name) {
        if (value === null)
        that.removeAttr(name);
      });
    }

    this.bind("created", can.proxy(reinit, this));

    reinit.call(this);
  }
});

can.Model.Join("CMS.Models.SystemSystem", {
  root_object : "system_system"
  , root_collection : "system_systems"
  , join_keys : {
    "parent" : CMS.Models.System
    , "child" : CMS.Models.System
  }
  , findAll: "GET /api/system_systems"
  , create: "POST /api/system_systems"
  , destroy : "DELETE /api/system_systems/{id}"
}, {
  init : function() {
    var _super = this._super;
    function reinit() {
      var that = this;

      typeof _super === "function" && _super.call(this);
      this.attr("parent", CMS.Models.get_instance(
        "System",
        this.parent_id || (this.parent && this.parent.id)));
      this.attr("child", CMS.Models.get_instance(
        "System",
        this.child_id || (this.child && this.child.id)));

      this.each(function(value, name) {
        if (value === null)
        that.removeAttr(name);
      });
    }

    this.bind("created", can.proxy(reinit, this));

    reinit.call(this);
  }
});

can.Model.Join("CMS.Models.UserRole", {
  root_object : "user_role"
  , root_collection : "user_roles"
  , findAll : "GET /api/user_roles"
  , update : "PUT /api/user_roles/{id}"
  , create : "POST /api/user_roles"
}, {});

can.Model.Join("GGRC.Models.DirectiveControl", {
  join_keys : {
    "directive" : CMS.Models.Directive
    , "control" : CMS.Models.Control
  }
  , findAll : function(params) {
    throw "ERROR : DirectiveControl is not yet implemented";
  }
  , findOne : function(params) {
    throw "ERROR : DirectiveControl is not yet implemented";
  }
  , update : function(params) {
    throw "ERROR : DirectiveControl is not yet implemented";
  }
  , create : function(params) {
    throw "ERROR : DirectiveControl is not yet implemented";
  }
  , destroy : function(params) {
    throw "ERROR : DirectiveControl is not yet implemented";
  }
}, {

});

})(this.can, this.can.$);
