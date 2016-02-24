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
      disableReuse: true,
      reuseIt: function (scope, el, ev) {
        var reused;
        var relatedDfds;

        if (el.hasClass('disabled')) {
          return;
        }
        reused = this.attr('reusedObjects');
        relatedDfds = can.map(reused, function (object) {
          var executer = this[object.method].bind(this);
          return executer(object.item);
        }.bind(this));
        GGRC.delay_leaving_page_until($.when.apply($, relatedDfds));
      },
      createRelationship: function (destination) {
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
      createEvidenceRelationship: function (destination) {
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
      '{scope.reusedObjects} change': function (list) {
        this.scope.attr('disableReuse', !list.length);
      }
    }
  });

  can.Component.extend({
    tag: 'reusable-object',
    template: '<content></content>',
    scope: {
      selectObject: function (instance, el, ev) {
        var status = el.prop('checked');
        var list = this.attr('list');
        var index;

        if (status) {
          list.push({
            item: instance,
            method: this.attr('method')
          });
        } else {
          index = _.findIndex(list, function (item) {
            if (!item.instance || item.instance.id) {
              return false;
            }
            return item.instance.id === instance.id &&
              item.instance.type === instance.type;
          });
          list.splice(index, 1);
        }
      }
    }
  });
})(window.can, window.can.$);
