/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: brad@reciprocitylabs.com
 * Maintained By: brad@reciprocitylabs.com
 */


(function(can, $) {

can.Control("GGRC.Controllers.PbcWorkflows", {

}, {
  "{CMS.Models.ControlAssessment} created": function(model, ev, instance) {

    if(!(instance instanceof CMS.Models.ControlAssessment)) {
      return;
    }

    var audit_dfd, control_dfd;

    audit_dfd = this._create_relationship(instance, instance.audit);
    control_dfd = this._create_relationship(instance, instance.control);
    instance.delay_resolving_save_until($.when(audit_dfd, control_dfd));

  },
  "{CMS.Models.Issue} created": function(model, ev, instance) {

    if(!(instance instanceof CMS.Models.Issue)) {
      return;
    }

    var audit_dfd, control_dfd, program_dfd, control_assessment_dfd;

    audit_dfd = this._create_relationship(instance, instance.audit);
    control_dfd = this._create_relationship(instance, instance.control);
    program_dfd = this._create_relationship(instance, instance.program);
    control_assessment_dfd = this._create_relationship(instance, instance.control_assessment);
    instance.delay_resolving_save_until($.when(audit_dfd, control_dfd));

  },
  "{CMS.Models.Section} created": function(model, ev, instance) {

    if(!(instance instanceof CMS.Models.Section)) {
      return;
    }

    if(!(instance.directive instanceof CMS.Models.Directive)) {
      return;
    }

    var directive_dfd;

    directive_dfd = this._create_relationship(instance, instance.directive);
    instance.delay_resolving_save_until($.when(section_dfd, directive_dfd));

  },
  _create_relationship: function(source, destination) {

    if (!destination) {
      return $.Deferred().resolve();
    }

    return new CMS.Models.Relationship({
      source: source.stub(),
      destination: destination,
      context: source.context,
    }).save();
  }
});

$(function() {
  $(document.body).ggrc_controllers_pbc_workflows();
});

})(this.can, this.can.$);
