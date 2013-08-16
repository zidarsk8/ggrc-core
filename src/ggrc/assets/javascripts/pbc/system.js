/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require models/cacheable
//= require pbc/document
//= require pbc/person

can.Model.Cacheable("CMS.Models.SystemOrProcess", {
    root_object : "system_or_process"
    , root_collection : "systems_or_processes"
    , category : "business"
    , findAll : "GET /api/systems_or_processes"
    , tree_view_options : {
      list_view : "/static/mustache/systems/tree.mustache"
      , link_buttons : true
      , child_options : [{
        model : CMS.Models.Control
        , list_view : "/static/mustache/controls/tree.mustache"
        , parent_find_param : "system_controls.system_id"
        , link_buttons : true
        , draw_children : false
      },{
        model : null ///filled in after init.
        , list_view : "/static/mustache/systems/tree.mustache"
        , parent_find_param : "super_system_systems.parent_id"
        , link_buttons: true
      }]
    }
    , serialize : {
    }
    , bind_object_star_events: function() {
        var that = this;

        if (this !== CMS.Models.SystemOrProcess)
          return;

        CMS.Models.ObjectPerson.bind("created", function(ev, obj_person) {
            var sys = that.findInCacheById(obj_person.xable_id); //"this" is Cacheable.  WTF?
            if(sys && obj_person.personable_type === that.xable_type) {
                sys.addElementToChildList("object_people", obj_person);
                sys.addElementToChildList("people", obj_person.person);
            }
        });
        CMS.Models.ObjectPerson.bind("destroyed", function(ev, obj_person) {
            var sys = that.findInCacheById(obj_person.xable_id); //"this" is Cacheable.  WTF?
            if(sys && obj_person.personable_type === that.xable_type) {
                sys.removeElementFromChildList("object_people", obj_person);
                sys.removeElementFromChildList("people", obj_person.person);
            }
        });
        CMS.Models.ObjectDocument.bind("created", function(ev, obj_doc) {
            var sys = that.findInCacheById(obj_doc.xable_id); //"this" is Cacheable.  WTF?
            if(sys && obj_doc.documentable_type === that.xable_type) {
                sys.addElementToChildList("object_documents", obj_doc);
                sys.addElementToChildList("documents", obj_doc.document);
            }
        });
        CMS.Models.ObjectDocument.bind("destroyed", function(ev, obj_doc) {
            var sys = that.findInCacheById(obj_doc.xable_id); //"this" is Cacheable.  WTF?
            if(sys && obj_doc.documentable_type === that.xable_type) {
                sys.removeElementFromChildList("object_documents", obj_doc);
                sys.removeElementFromChildList("documents", obj_doc.document);
            }
        });
    }
    , links_to : {
      "System" : "SystemSystem"
      , "Process" : "SystemSystem"
      , "Control" : "SystemControl"
      , "Product" : {}
      , "Facility" : {}
      , "OrgGroup" : {}
      , "Project" : {}
      , "DataAsset" : {}
      , "Program" : {}
      , "Market" : {}
      , "Risk" : {}
      }
}, {
    system_or_process: function() {
      if (this.attr('is_biz_process'))
        return 'process';
      else
        return 'system';
    }
    , system_or_process_capitalized: function() {
      var str = this.system_or_process();
      return str.charAt(0).toUpperCase() + str.slice(1);
    }
});

CMS.Models.SystemOrProcess("CMS.Models.System", {
    root_object : "system"
  , root_collection : "systems"
  , findAll : "GET /api/systems"
  , create : "POST /api/systems"
  , update : "PUT /api/systems/{id}"
  , destroy : "DELETE /api/systems/{id}"

  , cache : can.getObject("cache", CMS.Models.SystemOrProcess, true)
    , attributes : {
      controls : "CMS.Models.Control.models"
      , sub_systems : "CMS.Models.get_instances"
      , super_systems : "CMS.Models.get_instances"
      , documents : "CMS.Models.Document.models"
      , people : "CMS.Models.Person.models"
      , object_documents : "CMS.Models.ObjectDocument.models"
      , object_people : "CMS.Models.ObjectPerson.models"
      , owner : "CMS.Models.Person.model"
    }
  , init : function() {
    this._super && this._super.apply(this, arguments);
    this.tree_view_options = $.extend({}, CMS.Models.SystemOrProcess.tree_view_options);
    this.tree_view_options.child_options[1].model = this;
    this.validatePresenceOf("title");
  } //don't rebind the ObjectDocument/ObjectPerson events.
}, {
    init : function() {
      this._super && this._super.apply(this, arguments);
      this.attr('is_biz_process', false);
    }
});

CMS.Models.SystemOrProcess("CMS.Models.Process", {
    root_object : "process"
  , root_collection : "processes"
  , model_plural : "Processes"
  , table_plural : "processes"
  , title_plural : "Processes"
  , model_singular : "Process"
  , title_singular : "Process"
  , table_singular : "process"
  , findAll : "GET /api/processes"
  , create : "POST /api/processes"
  , update : "PUT /api/processes/{id}"
  , destroy : "DELETE /api/processes/{id}"
  , cache : can.getObject("cache", CMS.Models.SystemOrProcess, true)
    , attributes : {
      controls : "CMS.Models.Control.models"
      , sub_systems : "CMS.Models.get_instances"
      , super_systems : "CMS.Models.get_instances"
      , documents : "CMS.Models.Document.models"
      , people : "CMS.Models.Person.models"
      , object_documents : "CMS.Models.ObjectDocument.models"
      , object_people : "CMS.Models.ObjectPerson.models"
      , owner : "CMS.Models.Person.model"
    }
  , init : function() {
    this._super && this._super.apply(this, arguments);
    this.tree_view_options = $.extend({}, CMS.Models.SystemOrProcess.tree_view_options);
    this.tree_view_options.child_options[1].model = this;
    this.validatePresenceOf("title");
  } //don't rebind the ObjectDocument/ObjectPerson events.
}, {
    init : function() {
      this._super && this._super.apply(this, arguments);
      this.attr('is_biz_process', true);
    }
});
