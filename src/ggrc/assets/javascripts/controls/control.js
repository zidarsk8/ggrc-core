/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require models/cacheable
(function(namespace, $){
can.Model.Cacheable("CMS.Models.Control", {
  // static properties
    root_object : "control"
  , root_collection : "controls"
  , category : "governance"
  , create : "POST /api/controls"
  , update : "PUT /api/controls/{id}"
  , destroy : "DELETE /api/controls/{id}"
  , attributes : {
      owner : "CMS.Models.Person.model"
    , modified_by : "CMS.Models.Person.model"
    , object_people : "CMS.Models.ObjectPerson.models"
    , people : "CMS.Models.Person.models"
    , object_documents : "CMS.Models.ObjectDocument.models"
    , documents : "CMS.Models.Document.models"
    , categories : "CMS.Models.Category.models"
    , assertions : "CMS.Models.Category.models"
    , control_controls : "CMS.Models.ControlControl.models"
    , implemented_controls : "CMS.Models.Control.models"
    , implementing_control_controls : "CMS.Models.ControlControl.models"
    , implementing_controls : "CMS.Models.Control.models"
    , objective_controls : "CMS.Models.ObjectiveControl.models"
    , objectives : "CMS.Models.Objective.models"
    , directive : "CMS.Models.Directive.model"
    , control_sections : "CMS.Models.ControlSection.models"
    , sections : "CMS.Models.Section.models"
    , program_controls : "CMS.Models.ProgramControl.models"
    , programs : "CMS.Models.Program.models"
    , system_controls : "CMS.Models.SystemControl.models"
    , systems : "CMS.Models.System.models"
    , control_risks : "CMS.Models.ControlRisk.models"
    , risks : "CMS.Models.Risk.models"
    , object_controls : "CMS.Models.ObjectControl.models"
    , type : "CMS.Models.Option.model"
    , kind : "CMS.Models.Option.model"
    , means : "CMS.Models.Option.model"
    , verify_frequency : "CMS.Models.Option.model"
  }
  , links_to : {
    "Section" : "ControlSection"
    , "Regulation" : "DirectiveControl"
    , "Policy" : "DirectiveControl"
    , "Contract" : "DirectiveControl"
    , "Risk" : {}
    , "Program" : "ProgramControl"
  }

  , defaults : {
      "selected" : false
    , "title" : ""
    , "slug" : ""
    , "description" : ""

    , object_people : []
    , people : []
    , object_documents : []
    , documents : []
    , categories : []
    , assertions : []
    , control_controls : []
    , implemented_controls : []
    , implementing_control_controls : []
    , implementing_controls : []
    , objective_controls : []
    , objectives : []
    , control_sections : []
    , sections : []
    , program_controls : []
    , programs : []
    , system_controls : []
    , systems : []
    , control_risks : []
    , risks : []
    , object_controls : []
  }

  , mappings: {
      people_mappings: {
          attr: "object_people"
        , target_attr: "person"
      }
    , business_object_mappings: {
          attr: "object_controls"
        , target_attr: "controllable"
      }
    , section_mappings: {
          attr: "control_sections"
        , target_attr: "section"
      }
    , objective_mappings: {
          attr: "objective_controls"
        , target_attr: "objective"
      }
    }

  , tree_view_options : {
      show_view : GGRC.mustache_path + "/controls/tree.mustache"
    , footer_view : GGRC.mustache_path + "/controls/tree_footer.mustache"
    , draw_children : true
    , child_options : [{
    /*    model : "Section"
      , property : "section_mappings"
      , show_view : "/static/mustache/sections/tree.mustache"
    }, {*/
        model : "Person"
      , property : "people_mappings"
      , show_view : "/static/mustache/people/tree.mustache"
    }, {
        model : "Objective"
      , property : "objective_mappings"
      , show_view : "/static/mustache/objectives/tree.mustache"
    }, {
        model : can.Model.Cacheable
      , property : "business_object_mappings"
      , show_view : GGRC.mustache_path + "/base_objects/tree.mustache"
      , title_plural : "Business Objects"
    }]
  }

  , init : function() {
    this.validatePresenceOf("title");
    this._super.apply(this, arguments);
  }
}
, {
// prototype properties
  init : function() {
    var that = this;
    this.attr({
      "content_id" : Math.floor(Math.random() * 10000000)
    });
    this._super();
    this._init_mappings();
  }

  , bind_section : function(section) {
    var that = this;
    this.bind("change.section" + section.id, function(ev, attr, how, newVal, oldVal) {
      if(attr !== 'implementing_controls')
        return;

      var oldValIds = can.map(can.makeArray(oldVal), function(val) { return val.id; });

      if(how === "add" || (how === "set" && newVal.length > oldVal.length)) {
        can.each(newVal, function(el) {
          if($.inArray(el.id, oldValIds) < 0) {
            section.addElementToChildList("linked_controls", CMS.Models.Control.findInCacheById(el.id));
          }
        });
      } else {
        var lcs = section.linked_controls.slice(0);
        can.each(oldVal, function(el) {
          if($.inArray(el, newVal) < 0) {
            lcs.splice($.inArray(el, lcs), 1);
          }
        });
        section.attr(
          "linked_controls"
          , lcs
        );
      }
    });
  }
  , unbind_section : function(section) {
    this.unbind("change.section" + section.id);
  }
});

// This creates a subclass of the Control model
CMS.Models.Control("CMS.Models.ImplementedControl", {
	findAll : "GET /api/controls/{id}/implemented_controls"
}, {
});

/*
	Note: This is kind of a hack.  I would like to revisit the structure of the control models later
	in order to just pull the linked ones out of cache, but it takes some clever finagling with
	$.Deferred and it's too much work to think through at the moment.  In the meantime, implementing
	controls as a separate model from Regulation or Company controls works for my needs (comparing IDs)
	--BM 12/10/2012
*/
CMS.Models.ImplementedControl("CMS.Models.ImplementingControl", {
	findAll : "GET /api/controls/{id}/implementing_controls"
}, {});


// This creates a subclass of the Control model
CMS.Models.Control("CMS.Models.RegControl", {
	findAll : "GET /api/programs/{id}/controls"
  , attributes : {
    implementing_controls : "CMS.Models.ImplementingControl.models"
  }
	, map_ccontrol : function(params, control) {
		return can.ajax({
			url : "/mapping/map_ccontrol"
			, data : params
			, type : "post"
			, dataType : "json"
			, success : function() {
				if(control) {
					var ics;
					if(params.u) {
						//unmap
						ics = new can.Model.List();
						can.each(control.implementing_controls, function(ctl) {
              //TODO : Put removal functionality into the Cacheable, in the vein of addElementToChildList,
              //  and update this code to simply remove the unmap code.
              //We are needing to manually trigger changes in Model.List due to CanJS being unable to
              //  trigger template changes for lists automatically.
							if(ctl.id !== params.ccontrol)
							{
								ics.push(ctl);
							}
              control.attr("implementing_controls", ics);
              control.updated();
            });
          } else {
            //map
            control.addElementToChildList("implementing_controls", CMS.Models.Control.findInCacheById(params.ccontrol));
          }
				}
			}
		});
	}
}, {
	init : function() {
		this._super();
		this.attr((this.control ? "control." : "") + "type", "regulation");
	}
	, map_ccontrol : function(params) {
		return this.constructor.map_ccontrol(can.extend({}, params, {rcontrol : this.id}), this);
	}

});

})(this, can.$);
