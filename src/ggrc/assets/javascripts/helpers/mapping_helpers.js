/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function () {
  Mustache.registerHelper('if_mapping_ready',
    function (mappingName, instance, options) {
      var mappingDeferred = Mustache.resolve(instance)
        .get_mapping_deferred(mappingName);

      var dfd = new $.Deferred();

      mappingDeferred.then(function (mapping) {
        var resolveDfd = function () {
          dfd.resolve();
          mapping.unbind('length', resolveDfd);
        };

        if (mapping.length > 0) {
          // mapping is already ready
          dfd.resolve();
        } else {
          mapping.bind('length', resolveDfd);
        }
      });

      return Mustache.defer_render('span', function () {
        return options.fn(options.contexts);
      }, dfd);
    });
})();
