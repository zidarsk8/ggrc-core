/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, CMS, $) {
  'use strict';

  GGRC.Components('unmapPersonButton', {
    tag: 'unmap-person-button',
    viewModel: {
      destination: {},
      source: {},
      unmapInstance: function () {
        let objectPerson = this.getObjectMapping();
        let userRole = this.getRoleMapping();

        let dfds = [this.deleteObject(userRole),
          this.deleteObject(objectPerson)];

        $.when.apply($, dfds)
          .done(function () {
            this.attr('destination').dispatch('refreshInstance');
            can.trigger('unmap', {params: [
              this.attr('source'),
              this.attr('destination')]});
          }.bind(this));
      },
      getObjectMapping: function () {
        let destinationType = this.attr('destination.type');
        let mappingType;
        let sources;
        let destinations;
        let mapping;

        sources = this.attr('source.object_people');
        destinations = this.attr('destination.object_people');
        mappingType = 'ObjectPerson';

        sources = sources
          .map(function (item) {
            return item.id;
          });
        mapping = destinations
          .filter(function (dest) {
            return isWorkflow ?
              sources.indexOf(dest.person.id) > -1 :
              sources.indexOf(dest.id) > -1;
          })[0];

        return new CMS.Models[mappingType](mapping || {});
      },
      getRoleMapping: function () {
        let contextId = this.attr('destination.context.id');
        let roles = this.attr('source.user_roles');

        roles = roles.map(function (role) {
          return new CMS.Models.UserRole({id: role.id});
        }).filter(function (role) {
          return role.context_id === contextId;
        });

        return roles.length ? roles[0] : new CMS.Models.UserRole({});
      },
      deleteObject: function (obj) {
        let deferred = can.Deferred();
        obj
          .refresh()
          .then(function (item) {
            item
              .destroy()
              .then(function () {
                deferred.resolve();
              });
          });

        return deferred;
      },
    },
    events: {
      click: function () {
        this.viewModel.unmapInstance();
      },
    },
  });
})(window.can, window.GGRC, window.CMS, window.can.$);
