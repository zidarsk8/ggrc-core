/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: brad@reciprocitylabs.com
 * Maintained By: brad@reciprocitylabs.com
 */

(function (can, $) {
  can.Control('GGRC.Controllers.PbcWorkflows', {}, {
    '{CMS.Models.Assessment} created': function (model, ev, instance) {
      var auditDfd;
      var objectDfd;

      if (!(instance instanceof CMS.Models.Assessment)) {
        return;
      }

      auditDfd = this._create_relationship(instance,
          instance.audit, instance.audit.context);
      objectDfd = this._create_relationship(instance,
          instance.object, instance.audit.context);
      instance.delay_resolving_save_until($.when(auditDfd, objectDfd));
    },
    '{CMS.Models.Issue} created': function (model, ev, instance) {
      var auditDfd;
      var controlDfd;
      var programDfd;
      var assessmentDfd;

      if (!(instance instanceof CMS.Models.Issue)) {
        return;
      }

      auditDfd = this._create_relationship(instance, instance.audit);
      controlDfd = this._create_relationship(instance, instance.control);
      programDfd = this._create_relationship(instance, instance.program);
      assessmentDfd = this._create_relationship(instance, instance.assessment);
      instance.delay_resolving_save_until($.when(auditDfd, controlDfd,
          programDfd, assessmentDfd));
    },
    '{CMS.Models.Section} created': function (model, ev, instance) {
      var directiveDfd;

      if (!(instance instanceof CMS.Models.Section)) {
        return;
      }

      directiveDfd = this._create_relationship(instance, instance.directive);
      instance.delay_resolving_save_until($.when(directiveDfd));
    },
    '{CMS.Models.UserRole} created': function (model, ev, instance) {
      var dfd;
      if (!(instance instanceof CMS.Models.UserRole)) {
        return;
      }
      if (instance.role_name !== 'Auditor') {
        return;
      }
      // Find the program context
      dfd = instance.refresh_all('context', 'related_object', 'program',
          'context');
      dfd.then(function (programContext) {
        // Find existing auditor roles for program context
        return $.when(
            programContext,
            CMS.Models.UserRole.findAll({context_id: programContext.id,
                person_id: instance.person.id}),
            CMS.Models.Role.findAll({name: 'ProgramReader'}));
      }).then(function (programContext, auditorProgramRoles, readerRoles) {
        // Check if there are any existing roles for the user and program context
        if (auditorProgramRoles.length) {
          return null;
        }
        // If no program role exists for the user, we create a reader role
        return new CMS.Models.UserRole({
          person: instance.person,
          role: readerRoles[0].stub(),
          context: programContext
        }).save();
      });
      instance.delay_resolving_save_until(dfd);
    },
    _create_relationship: function (source, destination, context) {
      if (!destination) {
        return $.Deferred().resolve();
      }
      if (!context) {
        context = source.context;
      }
      return new CMS.Models.Relationship({
        source: source.stub(),
        destination: destination,
        context: context
      }).save();
    }
  });

  $(function () {
    $(document.body).ggrc_controllers_pbc_workflows();
  });
})(this.can, this.can.$);
