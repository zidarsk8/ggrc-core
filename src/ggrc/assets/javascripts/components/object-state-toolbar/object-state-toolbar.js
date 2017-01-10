/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tag = 'object-state-toolbar';
  var tpl = can.view(GGRC.mustache_path +
    '/components/object-state-toolbar/object-state-toolbar.mustache');
  /**
   * Object State Toolbar Component allowing Object state modification
   */
  can.Component.extend('objectStateToolbar', {
    tag: tag,
    template: tpl,
    viewModel: {
      instance: null,
      hasVerifiers: false,
      isCurrentUserVerifier: false,
      isDisabled: function () {
        return !!this.attr('instance._disabled');
      },
      errorMsg: function () {
        return this.attr('instance._mandatory_msg');
      },
      isInProgressOrNotStarted: function () {
        return this.attr('instance.status') === 'In Progress' ||
          this.attr('instance.status') === 'Not Started';
      },
      isInProgress: function () {
        return this.attr('instance.status') === 'In Progress';
      },
      isInReview: function () {
        return this.attr('instance.status') === 'Ready for Review';
      },
      hasErrors: function () {
        return this.attr('instance._mandatory_msg');
      },
      checkIsCurrentUserVerifier: function (verifiers) {
        var isVerifier = false;
        verifiers.each(function (verifier) {
          if (verifier.instance.email === GGRC.current_user.email) {
            isVerifier = true;
            return false;
          }
        });
        return isVerifier;
      },
      refreshVerifiers: function () {
        this.attr('instance')
          .get_binding('related_verifiers')
          .refresh_instances()
          .done(function (verifiers) {
            this.attr('hasVerifiers', !!verifiers.length);
            this.attr('isCurrentUserVerifier',
              this.checkIsCurrentUserVerifier(verifiers));
          }.bind(this));
      }
    },
    init: function () {
      this.viewModel.refreshVerifiers();
    },
    events: {
      '{viewModel.instance} related_sources': function () {
        this.viewModel.refreshVerifiers();
      },
      '{viewModel.instance} related_destinations': function () {
        this.viewModel.refreshVerifiers();
      }
    }
  });
})(window.can, window.GGRC);
