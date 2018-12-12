/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Cacheable from '../cacheable';
import {getCustomAttributableModels} from '../../plugins/utils/models-utils';

/* class CustomAttributable
  *
  * CustomAttributable does not query the backend, it is used to display a
  * list of objects in the custom attributes widget. It inherits from
  * cacheable because it needs getBinding to properly display
  * CustomAttributeDefinitions as children
  *
  */
export default Cacheable('CMS.Models.CustomAttributable', {
  findAll: function () {
    let types = _.orderBy(getCustomAttributableModels(),
      'category', false);

    return can.when(can.map(types, (type, i) => {
      return new this(Object.assign({}, type, {
        id: i,
      }));
    }));
  },
}, {
  // Cacheable checks if selfLink is set when the findAll deferred is done
  selfLink: '/custom_attribute_list',
});
