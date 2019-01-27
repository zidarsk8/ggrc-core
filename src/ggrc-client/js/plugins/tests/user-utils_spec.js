/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import * as UserUtils from '../utils/user-utils';
import Person from '../../models/business-models/person';

describe('User Utils', function () {
  describe('cacheCurrentUser() method', function () {
    let currentUser;

    beforeAll(() => {
      currentUser = GGRC.current_user;
    });

    afterAll(() => {
      GGRC.current_user = currentUser;
    });

    it('should add current user to cache', function () {
      GGRC.current_user = {
        name: 'TestCurrentUser',
        id: 0,
      };

      UserUtils.cacheCurrentUser();

      let currenUserFromCache = Person.findInCacheById(0);

      expect(currenUserFromCache.name).toBe('TestCurrentUser');
    });
  });
});
