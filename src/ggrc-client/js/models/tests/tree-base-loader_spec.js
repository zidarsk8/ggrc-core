/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.ListLoaders.TreeBaseLoader', function () {
  'use strict';
  let treeBaseLoader;
  let person;
  let audit;

  beforeEach(function () {
    person = new CMS.Models.Person();
    audit = new CMS.Models.Audit();
    treeBaseLoader = new GGRC.ListLoaders.TreeBaseLoader(null, person);
  });

  describe('makeResult() method', function () {
    let method;
    let getUserRolesSpy;
    let dfd;
    let binding;

    beforeEach(function () {
      dfd = $.when();
      binding = {
        instance: audit
      };
      method = treeBaseLoader.makeResult;
      getUserRolesSpy = spyOn(CMS.Models.Person, 'getUserRoles')
        .and.returnValue(dfd);
    });

    it('should be able to retrieve audit and program person\'s user roles' +
      ' on Audit page',
      function () {
        method(person, binding);
        expect(getUserRolesSpy)
          .toHaveBeenCalledWith(binding.instance, person, 'program');
      }
    );
  });
});
