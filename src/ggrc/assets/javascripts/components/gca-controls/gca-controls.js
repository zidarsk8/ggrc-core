/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';
  var CAUtils = GGRC.Utils.CustomAttributes;
  var tpl = can.view(GGRC.mustache_path +
    '/components/gca-controls/gca-controls.mustache');

  /**
   * This component renders edit controls for Global Custom Attributes
   */

  GGRC.Components('gcaControls', {
    tag: 'gca-controls',
    template: tpl,
    viewModel: {
      instance: {},
      items: [],
      modifiedFields: {},
      initGlobalAttributes: function () {
        var cavs;
        CAUtils.ensureGlobalCA(this.attr('instance'));
        cavs = CAUtils.getCustomAttributes(this.attr('instance'),
          CAUtils.CUSTOM_ATTRIBUTE_TYPE.GLOBAL);

        this.attr('items',
          cavs.map(function (cav) {
            return CAUtils.convertToFormViewField(cav);
          })
        );
      },
      updateGlobalAttribute: function (event, field) {
        this.attr('modifiedFields').attr(field.id, event.value);

        CAUtils.applyChangesToCustomAttributeValue(
          this.attr('instance.custom_attribute_values'),
          this.attr('modifiedFields')
        );

        this.attr('modifiedFields', {}, true);
      }
    },
    init: function () {
      this.viewModel.initGlobalAttributes();
    }
  });
})(window.can, window.GGRC);
