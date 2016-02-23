/*!
 Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: urban@reciprocitylabs.com
 Maintained By: urban@reciprocitylabs.com
 */

(function (can, $) {
  can.Component.extend({
    tag: 'reuse-objects',
    scope: {
      parentInstance: null,
      reusedObjects: new can.List(),
      create_relationship: function (destination) {
        var source;
        var dest;

        if (!this.scope || !destination) {
          return $.Deferred().resolve();
        }

        source = this.scope.attr('parentInstance');
        dest = CMS.Models.get_instance({
          id: destination.id,
          type: can.spaceCamelCase(destination.type).replace(/ /g, '')
        });

        return new CMS.Models.Relationship({
          source: source.stub(),
          destination: dest,
          context: source.context
        }).save();
      },
      create_evidence_relationship: function (destination) {
        var source;
        var dest;

        if (!this.scope || !destination) {
          return $.Deferred().resolve();
        }

        source = this.scope.attr('parentInstance');
        dest = CMS.Models.get_instance({
          id: destination.id,
          type: can.spaceCamelCase(destination.type).replace(/ /g, '')
        });

        return new CMS.Models.ObjectDocument({
          context: source.context,
          documentable: source,
          document: dest
        }).save();
      }
    },
    events: {
      '[reusable=true] input[type=checkbox] change': function (el, ev) {
        var reused = this.scope.attr('reusedObjects');
        var object = el.parent();
        var key = {
          type: object.attr('data-object-type'),
          id: object.attr('data-object-id'),
          method: object.parents('[reusable=true]').attr('reuse-method')
        };
        var index = _.findIndex(reused, key);
        if (index >= 0) {
          reused.splice(index, 1);
          return;
        }
        reused.push(key);
      },
      '.js-trigger-reuse click': function (el, ev) {
        var reused = this.scope.attr('reusedObjects');
        var relatedDfds = can.map(reused, function (object) {
          var executer = this.scope[object.method].bind(this);
          return executer(object);
        }.bind(this));
        GGRC.delay_leaving_page_until($.when.apply($, relatedDfds));
      }
    }
  });

  can.Component.extend({
    tag: 'reusable-object',
    template: '<content></content>',
    scope: {
      is_reusable: null
    },
    events: {
      'inserted': function (el, ev) {
        if (el.parents('[reusable=true]').length === 1) {
          this.scope.attr('is_reusable', true);
        }
      }
    },
    helpers: {
      if_reusable: function (options) {
        if (this.attr('is_reusable') === true) {
          return options.fn();
        }
        return options.inverse();
      }
    }
  });
})(window.can, window.can.$);
