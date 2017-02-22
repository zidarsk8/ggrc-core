/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, CMS, RefreshQueue) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/object-list-item/person-list-item.mustache');
  var tag = 'person-list-item';
  /**
   * Person List Item Component
   */
  can.Component.extend({
    tag: tag,
    template: tpl,
    viewModel: {
      define: {
        person: {
          value: {},
          set: function (newVal, setVal) {
            var objectToLoad;
            if (newVal.email) {
              setVal(newVal);
            } else {
              objectToLoad = new CMS.Models.Person({id: newVal.id});
              new RefreshQueue().enqueue(objectToLoad).trigger()
                .done(function (person) {
                  person = Array.isArray(person) ? person[0] : person;
                  setVal(person);
                })
                .fail(function () {
                  setVal({});
                  GGRC.Errors.notifier('error',
                    'Failed to fetch data for person ' + newVal.id + '.');
                });
            }
          }
        },
        personEmail: {
          get: function () {
            return this.attr('person.email') || false;
          }
        },
        personName: {
          get: function () {
            return this.attr('person.name') || this.attr('personEmail');
          }
        },
        showOnlyEmail: {
          get: function () {
            return this.attr('person.show_email') || false;
          }
        },
        hasNoAccess: {
          get: function () {
            return this.attr('person.system_wide_role') === 'No Access';
          }
        }
      }
    }
  });
})(window.can, window.GGRC, window.CMS, window.RefreshQueue);
