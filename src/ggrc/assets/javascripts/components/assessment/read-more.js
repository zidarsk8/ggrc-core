/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var namespace = 'assessment';
  var cmpName = 'read-more';
  var tpl = can.view(GGRC.mustache_path +
    '/components/' + namespace + '/' + cmpName + '.mustache');
  var tag = 'assessment-read-more';
  var rootCls = '.assessment-read-more';
  var bodyCls = rootCls + '__body';
  var bodyContentCls = bodyCls + '-content';
  var readMore = 'Read More';
  var readLess = 'Read Less';
  var defaultMaxHeight = '108px';
  /**
   * Assessment specific read more view component
   */
  GGRC.Components('assessmentReadMore', {
    tag: tag,
    template: tpl,
    scope: {
      text: null,
      isExpanded: false,
      showButton: false,
      btnText: readMore,
      maxHeight: defaultMaxHeight,
      toggle: function () {
        var newValue = !this.attr('isExpanded');
        this.attr('isExpanded', newValue);
        this.attr('maxHeight', newValue ? '100%' : defaultMaxHeight);
        this.attr('btnText', newValue ? readLess : readMore);
      },
      recalculate: function () {
        var el = this.attr('$rootEl');
        if (this.attr('text')) {
          this.attr('showButton',
            el.find(bodyCls).outerHeight() <
            el.find(bodyContentCls).outerHeight());
        }
      },
      restoreDefault: function () {
        can.batch.start();
        this.attr('showButton', false);
        this.attr('isExpanded', false);
        this.attr('btnText', readMore);
        can.batch.stop();
      }
    },
    events: {
      init: function (el) {
        this.scope.attr('$rootEl', el);
      },
      '{scope} text': function () {
        this.scope.restoreDefault();
        this.scope.recalculate();
      },
      '{window} resize': function () {
        this.scope.restoreDefault();
        this.scope.recalculate();
      }
    }
  });
})(window.can, window.GGRC);
