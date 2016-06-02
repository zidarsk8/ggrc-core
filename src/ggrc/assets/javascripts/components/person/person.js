/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: peter@reciprocitylabs.com
  Maintained By: peter@reciprocitylabs.com
*/

/**
 * A component that renders a single Person item, fetching the object from the
 * server if necessary.
 */
(function (GGRC, can) {
  'use strict';

  // the component's configuration object (i.e. its constructor's prototype)
  var component = {
    tag: 'person',

    template: can.view(
      GGRC.mustache_path +
      '/components/person/person.mustache'
    ),

    scope: {
      personObj: null
    },

    _EV_REMOVE_CLICK: 'person-remove',

    /**
     * The component's entry point. Invoked when a new component instance has
     * been created.
     *
     * @param {Object} element - the (unwrapped) DOM element that triggered the
     *   creation of the component instance
     * @param {Object} options - the component instantiation options
     */
    init: function (element, options) {
      var $el = $(element);
      var personId = Number($el.attr('person-id'));
      var scope = this.scope;
      var person = scope.attr('personObj');
      var editableVal = $el.attr('editable');
      var editable;

      if (editableVal === '' || editableVal === 'false') {
        editable = false;
      } else if (editableVal === 'true') {
        editable = true;
      } else {
        editable = Boolean(scope.attr('editable'));
      }
      scope.attr('editable', editable);

      if (person && _.isEmpty(person.serialize()) && _.isNaN(personId)) {
        console.warn('`personObj` or `personId` are missing');
        return;
      }

      if (!person) {
        person = CMS.Models.Person.cache[personId];
      }
      // For some reason the cache sometimes contains partially loaded objects,
      // thus we also need to check if "email" (a required field) is present.
      // If it is, we can be certain that we can use the object from the cache.
      if (person && person.attr('email')) {
        scope.attr('personObj', person);
        return;
      }

      if (_.isNaN(personId) || personId <= 0) {
        personId = person.attr('id');
      }

      // but if not in cache, we need to fetch the person object...
      CMS.Models.Person
        .findOne({id: personId})
        .then(function (person) {
          scope.attr('personObj', person);
        }, function () {
          $el.trigger(
            'ajax:flash',
            {error: 'Failed to fetch data for person ' + personId + '.'});
        });
    },

    events: {
      /**
       * Event handler when a user clicks the trash icon.
       *
       * @param {jQuery.Element} $el - the source of the event `ev`
       * @param {jQuery.Event} ev - the event object
       */
      'a.unmap click': function ($el, ev) {
        // the handler is registered on the component's root element,
        // thus it needs to be triggered on it (and not on the $el)
        this.element.triggerHandler({
          type: component._EV_REMOVE_CLICK,
          person: this.scope.personObj
        });
      }
    }
  };

  GGRC.Components('personItem', component);
})(window.GGRC, window.can);
