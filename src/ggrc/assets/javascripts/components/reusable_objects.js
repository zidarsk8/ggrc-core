/*!
 Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: ivan@reciprocitylabs.com
 Maintained By: ivan@reciprocitylabs.com
 */

(function (can, $) {
  can.Component.extend({
    tag: 'reuse-objects',
    scope: {
      parentInstance: null,
      /*
       * Is passed to child component (reusable-object) and it tracks
       * the values(objects) that should be reused
       *
       * {
       *    {method}-{instance.type}-{instance.id}: `true/false`,
       *    ...
       * }
       *
       * {method} - createRelationship, createEvidenceRelationship
       * {instance.type} - child object type
       * {instance.id} - child object id
       */
      reusedObjects: new can.Map(),
      isLoading: false,
      /*
       * Reuse objects
       *
       * Checks reusedObjects truthy values, creates appropriate relationship
       * and notifies user on their creation
       *
       * @param {Object} scope - component scope
       * @param {jQuery.Object} el - clicked element
       * @param {Object} ev - click event handler
       */
      reuseIt: function (scope, el, ev) {
        var reused = this.attr('reusedObjects');
        var relatedDfds = [];
        var when;

        if (el.hasClass('disabled') || this.attr('isLoading')) {
          return;
        }
        this.attr('isLoading', true);
        relatedDfds = can.map(can.Map.keys(reused), function (prop) {
          var executer;
          var id;
          var type;

          if (!reused.attr(prop)) {
            return;
          }
          prop = prop.split('-');
          executer = this[prop[0]];
          id = Number(prop[2]);
          type = can.spaceCamelCase(prop[1]).replace(/ /g, '');

          relatedDfds.push(executer.call(this, {
            id: id,
            type: type
          }));
        }.bind(this));

        when = $.when.apply($, relatedDfds);
        when.then(function () {
          can.map(can.Map.keys(reused), function (prop) {
            reused.attr(prop, false);
          });
          $(document.body).trigger('ajax:flash', {
            success: 'Selected evidences are reused'
          });
          this.attr('isLoading', false);
        }.bind(this));
        GGRC.delay_leaving_page_until(when);
      },
      /*
       * Creates an Relationship between parent instance and destination object
       *
       * @param {Object} destination - Should have `id` and `type`
       * @return {Object} - Returns newly created Relationship as jQuery deferred
       */
      createRelationship: function (destination) {
        var source;
        var dest;

        if (!destination) {
          return $.Deferred().resolve();
        }

        source = this.attr('parentInstance');
        dest = CMS.Models.get_instance({
          id: destination.id,
          type: destination.type
        });

        return new CMS.Models.Relationship({
          source: source.stub(),
          destination: dest,
          context: source.context
        }).save();
      },
      /*
       * Creates an Object Document Relationship  between parent instancere and destination object
       *
       * @param {Object} destination - Should have `id` and `type`
       * @return {Object} - Returns newly created Relationship as jQuery deferred
       */
      createEvidenceRelationship: function (destination) {
        var source;
        var dest;

        if (!destination) {
          return $.Deferred().resolve();
        }

        source = this.attr('parentInstance');
        dest = CMS.Models.get_instance({
          id: destination.id,
          type: destination.type
        });

        return new CMS.Models.ObjectDocument({
          context: source.context,
          documentable: source,
          document: dest
        }).save();
      }
    },
    helpers: {
      /*
       * Check if `Reuse` button should be enabled
       *
       * @param {Object} options - Mustache options object
       */
      disableReuse: function (options) {
        var list = [];
        var reused = this.attr('reusedObjects');
        can.each(can.Map.keys(reused), function (prop) {
          if (reused.attr(prop)) {
            list.push(prop);
          }
        });

        if (!list.length) {
          return options.fn();
        }
        return options.inverse();
      }
    }
  });

  /*
   * Child component that tracks checkbox changes
   *
   * Values that we pass in:
   * - reusable - If reusable checkbox should be visible
   * - method - Which method from parent (reuse-objects) component should be used
   *            for makining relationship
   * - list - List on which set if item should be reused
   */
  can.Component.extend({
    tag: 'reusable-object',
    template: '<content></content>',
    scope: {
      list: null
    },
    helpers: {
      isDisabled: function (instance, options) {
        var isMapped = GGRC.Utils.is_mapped(
          this.attr('baseInstance'), instance, this.attr('mapping'));

        if (isMapped) {
          return options.fn(options.contexts);
        }
        return options.inverse(options.context);
      }
    }
  });
})(window.can, window.can.$);
