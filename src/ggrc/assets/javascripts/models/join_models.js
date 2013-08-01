(function(can, $) {

can.Model.Cacheable("can.Model.Join", {
  join_keys : null
  , setup : function() {
    this._super.apply(this, arguments);
  }
  , init : function() {
    this._super && this._super.apply(this, arguments);
    //this.reinit();
    if(this === can.Model.Join) {
      this.bind("created.reinit destroyed.reinit", function(ev, instance) {
        instance.reinit();
        //can.proxy(this, "reinit"));
      });
    }
  }
}, {
    init : function() {
      this._super && this._super.apply(this, arguments);
      this.reinit();
    }
  , reinit : function() {//ev, data) {
      var self = this
        ;

      this.init_join_objects();
/*    can.each(this.constructor.join_keys, function(cls, attr_name) {
      var attr_val = self[attr_name];
      self.attr(attr_name, CMS.Models.get_instance(
        attr_val && attr_val.constructor.model_singular ? attr_val.constructor.model_singular : cls.model_singular
        , self[attr_name + "_id"] || (attr_val && attr_val.id)
        ));

      self[attr_name] && self[attr_name].refresh();
    });*/

    this.each(function(value, name) {
      if (value === null)
      self.removeAttr(name);
    });
  }
  , getOtherSide : function(obj) {
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

  , init_join_object_with_type: function(attr) {
      var object_id = this[attr + "_id"] || (this[attr] || {}).id
        , object_type = this[attr + "_type"] || (this[attr] || {}).type
        ;

      if (object_id && object_type)
        this.attr(attr, CMS.Models.get_instance(
              object_type
            , object_id
            , this[attr]
            ) || this[attr]);
    }

  , init_join_object: function(attr, model_name) {
      var object_id = this[attr + "_id"] || (this[attr] || {}).id;

      if (object_id)
        this.attr(attr, CMS.Models.get_instance(
              model_name
            , object_id
            , this[attr]
            ) || this[attr]);
    }

  , init_join_objects: function() {
      var that = this
        ;

      can.each(this.constructor.join_keys, function(model, attr) {
        if (model === can.Model.Cacheable)
          that.init_join_object_with_type(attr);
        else
          that.init_join_object(attr, model.shortName);
      });
    }
/*
  , init_object: function() {
      var that = this;
      this.init_join_objects();

      this.each(function(value, name) {
        if (value === null)
          that.removeAttr(name);
      });
    }

  , setup_reinit: function(init_super) {
      function reinit() {
        typeof init_super === "function" && init_super.call(this);
        this.init_object();
      }

      this.bind("created", can.proxy(reinit, this));
      reinit.call(this);
      this.bind("destroyed", function(ev) {
        can.each(ev.target.constructor.join_keys, function(cls, key) {
          ev.target[key].refresh();
        });
      });
    }*/
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
  reinit: function() {
    var that = this;

    //typeof this._super_init === "function" && this._super_init.call(this);
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
});

can.Model.Join("CMS.Models.ObjectSection", {
    root_object: "object_section"
  , root_collection: "object_sections"
  , join_keys : {
      "section" : CMS.Models.Section
    , "sectionable" : can.Model.Cacheable
  }
  , findAll: "GET /api/object_sections"
  , create: "POST /api/object_sections"
  , destroy: "DELETE /api/object_sections/{id}"
}, {
/*    init: function() {
      this.setup_reinit(this._super);
    }*/
});

can.Model.Join("CMS.Models.ObjectControl", {
    root_object: "object_control"
  , root_collection: "object_controls"
  , join_keys : {
      "control" : CMS.Models.Control
    , "controllable" : can.Model.Cacheable
  }
  , findAll: "GET /api/object_controls"
  , create: "POST /api/object_controls"
  , destroy: "DELETE /api/object_controls/{id}"
}, {
/*    init: function() {
      this.setup_reinit(this._super);
    }*/
});

can.Model.Join("CMS.Models.ObjectObjective", {
    root_object: "object_objective"
  , root_collection: "object_objectives"
  , join_keys : {
      "objective" : CMS.Models.Objective
    , "objectiveable" : can.Model.Cacheable
  }
  , findAll: "GET /api/object_objectives"
  , create: "POST /api/object_objectives"
  , destroy: "DELETE /api/object_objectives/{id}"
}, {
/*    init: function() {
      this.setup_reinit(this._super);
    }*/
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
});

can.Model.Join("CMS.Models.ObjectiveControl", {
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
});

can.Model.Join("CMS.Models.UserRole", {
  root_object : "user_role"
  , root_collection : "user_roles"
  , findAll : "GET /api/user_roles"
  , update : "PUT /api/user_roles/{id}"
  , create : "POST /api/user_roles"
  , destroy : "DELETE /api/user_roles/{id}"
  , join_keys : {
      person : CMS.Models.Person
    , role : CMS.Models.Role
  }
}, {
/*  init : function() {
    var _super = this._super;
    function reinit() {
      var that = this;

      typeof _super === "function" && _super.call(this);
      this.attr("person", CMS.Models.get_instance(
        "Person",
        this.person_id || (this.person && this.person.id), this.person));
      this.attr("role", CMS.Models.get_instance(
        "Role",
        this.role_id || (this.role && this.role.id), this.role));

      this.each(function(value, name) {
        if (value === null)
        that.removeAttr(name);
      });
    }

    this.bind("created", can.proxy(reinit, this));

    reinit.call(this);
  }*/

});


can.Model.Join("CMS.Models.ControlSection", {
  root_collection : "control_sections"
  , root_object : "control_section"
  , create : "POST /api/control_sections"
  , destroy : "DELETE /api/control_sections/{id}"
  , join_keys : {
    section : CMS.Models.Section
    , control : CMS.Models.Control
  }
  /*, attributes : {
    section : "CMS.Models.Section.model"
    , control : "CMS.Models.Control.model"
  }
  , init : function() {
    var that = this;
    this._super.apply(this, arguments);
    this.bind("created destroyed", function(ev, inst) {
      if(that !== inst.constructor) return;
      var section =
        CMS.Models.Section.findInCacheById(inst.section.id)
        || CMS.Models.Section.findInCacheById(inst.section.id);
      var control = 
        CMS.Models.RegControl.findInCacheById(inst.control.id)
        || CMS.Models.Control.findInCacheById(inst.control.id);

      section && section.refresh();
      control && control.refresh();
    });
  }*/
}, {
  serialize : function(name) {
    var serial;
    if(!name) {
      serial = this._super();
      serial.section && (serial.section = this.section.stub());
      serial.control && (serial.control = this.control.stub());
      return serial;
    } else {
      return this._super.apply(this, arguments);
    }
  }
});

can.Model.Join("CMS.Models.SectionObjective", {
  root_collection : "section_objectives"
  , root_object : "section_objective"
  , findAll : "GET /api/section_objectives"
  , create : "POST /api/section_objectives"
  , destroy : "DELETE /api/section_objectives/{id}"
  , join_keys : {
      section : CMS.Models.Section
    , objective : CMS.Models.Objective
  }
  , attributes : {
      section : "CMS.Models.Section.model"
    , objective : "CMS.Models.Objective.model"
  }
  /*, init : function() {
    var that = this;
    this._super.apply(this, arguments);
    this.bind("created destroyed", function(ev, inst) {
      if(that !== inst.constructor) return;
      var section =
        CMS.Models.Section.findInCacheById(inst.section.id)
        || CMS.Models.Section.findInCacheById(inst.section.id);
      var objective = 
        CMS.Models.Objective.findInCacheById(inst.objective.id);

      section && section.refresh();
      objective && objective.refresh();
    });
  }*/
}, {
/*    init: function() {
      this.setup_reinit(this._super);
    }*/
/*  , serialize : function(name) {
    var serial;
    if(!name) {
      serial = this._super();
      serial.section && (serial.section = this.section.stub());
      serial.objective && (serial.objective = this.objective.stub());
      return serial;
    } else {
      return this._super.apply(this, arguments);
    }
  }*/
});

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

can.Model.Join("GGRC.Models.ProgramControl", {
  root_collection : "program_controls"
  , root_object : "program_control"
  , join_keys : {
    "program" : CMS.Models.Program
    , "control" : CMS.Models.Control
  }
  , create : "POST /api/program_controls"
  , destroy : "DELETE /api/program_controls"
}, {

});

})(this.can, this.can.$);
