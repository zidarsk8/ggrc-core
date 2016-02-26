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
      reusedObjects: new can.Map(),
      reuseIt: function (scope, el, ev) {
        var reused = this.attr('reusedObjects');
        var relatedDfds = [];
        var when;

        if (el.hasClass('disabled')) {
          return;
        }

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
        });
        GGRC.delay_leaving_page_until(when);
      },
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

  can.Component.extend({
    tag: 'reusable-object',
    template: '<content></content>',
    scope: {
      list: null
    }
  });
})(window.can, window.can.$);
