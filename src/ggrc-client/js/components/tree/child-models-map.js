/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import DisplayPrefs from '../../models/local-storage/display-prefs';
import * as businessModels from '../../models/business-models/index';

const childModelsMap = can.Map.extend({
  displayPrefs: null,
  container: {},
  init: function () {
    DisplayPrefs.getSingleton().then(function (displayPrefs) {
      this.attr('displayPrefs', displayPrefs);
    }.bind(this));
  },
  getModels: function (parentType) {
    if (!this.attr('container.' + parentType)) {
      let savedModels = this.attr('displayPrefs')
        .getChildTreeDisplayList(parentType);

      if (savedModels) {
        // filter types that do not exist
        savedModels = savedModels.filter((type) => businessModels[type]);
      }

      this.attr('container').attr(parentType, savedModels);
    }
    return this.attr('container.' + parentType);
  },
  setModels: function (parentType, newModels) {
    this.attr('container').attr(parentType, newModels);

    this.attr('displayPrefs').setChildTreeDisplayList(parentType,
      newModels);
  },
});

export default new childModelsMap();
