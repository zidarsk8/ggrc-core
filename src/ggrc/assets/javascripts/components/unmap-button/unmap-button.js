/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, CMS) {
  'use strict';

  var defaultType = 'Relationship';

  GGRC.Components('unmapButton', {
    tag: 'unmap-button',
    template: can.view(GGRC.mustache_path +
      '/components/unmap-button/unmap-button.mustache'),
    viewModel: {
      mappingType: '@',
      objectProp: '@',
      destination: {},
      source: {},
      onClick: function () {
        this.unmapInstance();
      },
      unmapInstance: function () {
        this.getMapping()
          .refresh()
          .done(function (item) {
            item.destroy()
              .then(function () {
                this.attr('destination').dispatch('refreshInstance');
              }.bind(this));
          }.bind(this));
      },
      getMapping: function () {
        var type = this.attr('mappingType') || defaultType;
        var destinations;
        var sources;
        var mapping;
        if (type === defaultType) {
          destinations = this.attr('destination.related_destinations')
          .concat(this.attr('destination.related_sources'));
          sources = this.attr('source.related_destinations')
          .concat(this.attr('source.related_sources'));
        } else {
          destinations = this.attr('destination')
              .attr(this.attr('objectProp')) || [];
          sources = this.attr('source')
              .attr(this.attr('objectProp')) || [];
        }
        destinations = destinations
          .map(function (item) {
            return item.id;
          });
        sources = sources
          .map(function (item) {
            return item.id;
          });
        mapping = destinations
          .filter(function (dest) {
            return sources.indexOf(dest) > -1;
          })[0];
        mapping = mapping ? {id: mapping} : {};
        return new CMS.Models[type](mapping);
      }
    }
  });
})(window.can, window.GGRC, window.CMS);
