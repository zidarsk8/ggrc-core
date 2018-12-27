/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Cacheable from '../cacheable';
import {getRoleableModels} from '../../plugins/utils/models-utils';

/**
 * A "mixin" denoting a model type that can be assigned custom roles.
 *
 * This "mixin" is thus applied to models in a slightly different way - a
 * model needs to have a static property named `isRoleable` set to true.
 *
 * @class
 */
export default Cacheable('CMS.Models.Roleable', {
  findAll: function () {
    // We do not query the backend, this implementation is used to diplay
    // a list of objects in the Custom Roles widget.
    let types = _.orderBy(getRoleableModels(), 'category', false);

    let instances = can.map(types, (type, i) => {
      let withId = Object.assign({}, type, {id: i});
      return new this(withId);
    });

    return can.when(instances);
  },
}, {
  // Cacheable checks if selfLink is set when the findAll deferred is done
  selfLink: '/custom_roles_list', // TODO: what path here?
});
