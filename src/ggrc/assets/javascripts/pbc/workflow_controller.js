/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: brad@reciprocitylabs.com
 * Maintained By: brad@reciprocitylabs.com
 */


(function(can, $) {

can.Control("GGRC.Controllers.PbcWorkflows", {

}, {

  "{CMS.Models.Audit} created" : function(model, ev, instance) {
    if(instance instanceof CMS.Models.Audit) {
      this.create_objective(instance)
      .then(this.proxy("map_objective_to_program", instance.program.reify()))
      .then(function(object_objective) {
        return object_objective.objective.reify();
      })
      .then(this.proxy("create_request", instance))
      .then(this.proxy("create_response"));
    }
  }

  , create_objective : function(audit) {
    return new CMS.Models.Objective({
      title : "Generic request"
      , context : audit.context
      , owner : audit.owner || CMS.Models.Person.model(GGRC.current_user)
    }).save();
  }

  , map_objective_to_program : function(program, objective) {
    return new CMS.Models.ObjectObjective({
      objectiveable : program.stub()
      , objective : objective.stub()
      , context : objective.context
    }).save();
  }

  , create_request : function(audit, objective) {
    return new CMS.Models.Request({
      assignee : audit.owner || CMS.Models.Person.model(GGRC.current_user)
      , audit : audit.stub()
      , start_at : new Date()
      , end_at : moment().add(30, "days").toDate()
      , objective : objective.stub()
      , request_type : "documentation"
      , context : audit.context
    }).save().done(function(req) {
      objective.attr("title", objective.title + " " + req.attr("id")).save();
      return req;
    });
  }

  , create_response : function(request) {
    return new CMS.Models[request.response_model_class()]({
      pbc_response : "Generic response"
      , request : request.stub()
      , context : request.context
      , owner : request.assignee
    }).save();
  }

});

$(function() {
  $(document.body).ggrc_controllers_pbc_workflows();
});

})(this.can, this.can.$);