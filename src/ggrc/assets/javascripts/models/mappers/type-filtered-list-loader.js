/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can) {
  'use strict';

  GGRC.ListLoaders.StubFilteredListLoader("GGRC.ListLoaders.TypeFilteredListLoader", {
  }, {
      init: function (source, model_names) {
        var filter_fn = function (result) {
          var i, model_name;
          for (i=0; i<model_names.length; i++) {
            model_name = model_names[i];
            if (typeof model_name !== 'string')
              model_name = model_name.shortName;
            if (result.instance.constructor
                && result.instance.constructor.shortName === model_name)
              return true;
          }
          return false;
        };

        this._super(source, filter_fn);
      }
  });
})(window.GGRC, window.can);
