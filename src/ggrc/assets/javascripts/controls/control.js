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
    object_documents : "CMS.Models.ObjectDocument.models"
    , documents : "CMS.Models.Document.models"
    //, implementing_controls : "CMS.Models.Control.models"
    , control_sections : "CMS.Models.ControlSection.models"
    //, implemented_controls : "CMS.Models.Control.models"
    , directive : "CMS.Models.Directive.model"
    , sections : "CMS.Models.Section.models"
    , programs : "CMS.Models.Program.models"
    , object_controls : "CMS.Models.ObjectControl.models"
  }
  , tree_view_options : {
      list_view : "/static/mustache/controls/tree.mustache"
    , child_options : [{
        model : can.Model.Cacheable
      , list_view : GGRC.mustache_path + "/base_objects/list.mustache"
    }]
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
    "type" : {id : 1}
    , "selected" : false
    , "title" : ""
    , "slug" : ""
    , "description" : ""
    , object_controls : []
  }
  , tree_view_options : {
    draw_children : true
    , child_options : [{
      model : can.Model.Cacheable
      , property : "business_objects"
      , list_view : GGRC.mustache_path + "/base_objects/tree.mustache"
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
    this.attr("business_objects", new can.Model.List(
      can.map(
        this.object_controls,
        function(os) {return os.controllable || new can.Model({ selfLink : "/" }); }
      )
    ));
    this.object_controls.bind("change", function(ev, attr, how) {
      if(/^(?:\d+)?(?:\.updated)?$/.test(attr)) {
        that.business_objects.replace(
          can.map(
            that.object_controls,
            function(os, i) {
              if(os.controllable) {
                return os.controllable;
              } else {
                os.refresh({ "__include" : "controllable" }).done(function(d) {
                  that.business_objects.attr(i, d.controllable);
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
