/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  'use strict';

  GGRC.Components('relatedReferenceUrls', {
    tag: 'related-reference-urls',
    viewModel: {
      element: null,
      define: {
        urls: {
          value: function () {
            return [];
          }
        },
        value: {
          type: 'string',
          value: ''
        },
        isFormVisible: {
          type: 'boolean',
          value: false
        },
        isDisabled: {
          type: 'boolean',
          value: false
        },
        isNotEditable: {
          type: 'boolean',
          value: false
        }
      },
      /**
       * @description Moves focus to the create url input element
       */
      moveFocusToInput: function () {
        let inputElements = this.element.find('input');
        if (inputElements.length) {
          inputElements[0].focus();
        }
      },
      /**
       * @description Validates user input
       *
       * @param  {String} data Data for validation
       * @return {Boolean} - If incoming string is empty it returns false,
       * otherwise true
       */
      validateUserInput: function (data) {
        return data.length > 0;
      },
      /**
       * Handle changes during toggling form visibility.
       *
       * @param  {Boolean} isVisible - New value for form visibility
       * @param  {Boolean} [keepValue=false] - Whether to preserve the existing
       *   value of the form input field or not.
       */

      toggleFormVisibility: function (isVisible, keepValue) {
        this.attr('isFormVisible', isVisible);
        if (!keepValue) {
          this.attr('value', '');
        }
        if (isVisible) {
          this.moveFocusToInput();
        }
      },
      /**
       * @description Handles create url form submitting
       *
       * @param  {String} url - url to create
       * @return {Boolean} - it returns false to prevent page refresh
       */
      submitCreateReferenceUrlForm: function (url) {
        let existingUrls;
        let trimmedUrl = url.trim();
        let isValid = this.validateUserInput(trimmedUrl);

        // non-valid user input case - empty string
        if (!isValid) {
          GGRC.Errors.notifier('error', 'Please enter a URL.');
          this.toggleFormVisibility(true);
          return false;
        }

        // duplicate URLs check
        existingUrls = _.map(this.attr('urls'), 'link');

        if (_.contains(existingUrls, trimmedUrl)) {
          GGRC.Errors.notifier('error', 'URL already exists.');
          this.toggleFormVisibility(true, true);
          return false;
        }

        this.createReferenceUrl(trimmedUrl);

        this.toggleFormVisibility(false);
        return false;
      },
      /**
       * @description Dispatches 'createReferenceUrl' event with appropriate
       * data payload
       *
       * @param  {String} url - url to create
       */
      createReferenceUrl: function (url) {
        this.dispatch({
          type: 'createReferenceUrl',
          payload: url
        });
      },
      /**
       * @description Dispatches 'removeReferenceUrl' event with appropriate
       * data payload
       *
       * @param  {string} url - url to delete
       */
      removeReferenceUrl: function (url) {
        this.dispatch({
          type: 'removeReferenceUrl',
          payload: url
        });
      }
    },
    events: {
      /**
       * @description Handler for 'inserted' event to save reference
       * to component element
       */
      inserted: function () {
        this.viewModel.attr('element', this.element);
      }
    }
  });
})(window.can, window.can.$);
