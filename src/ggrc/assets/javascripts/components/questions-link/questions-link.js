/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {
  hasQuestions,
  getQuestionsUrl,
} from '../../plugins/utils/ggrcq-utils';

(function (can) {
  'use strict';

  GGRC.Components('questionsLink', {
    tag: 'questions-link',
    template: can.view(
      GGRC.mustache_path +
      '/components/questions-link/questions-link.mustache'
    ),
    viewModel: {
      define: {
        hasQuestions: {
          type: Boolean,
          get: function () {
            var instance = this.attr('instance');
            return hasQuestions(instance.class.title_singular);
          }
        },
        questionsUrl: {
          type: String,
          get: function () {
            var instance = this.attr('instance');
            return getQuestionsUrl(instance);
          }
        }
      },
      instance: null
    }
  });
})(window.can);
