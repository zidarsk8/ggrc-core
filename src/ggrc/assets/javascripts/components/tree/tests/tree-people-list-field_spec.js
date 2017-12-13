/*
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../tree-people-list-field';

describe('tree-people-list-field component', () => {
  let vm;

  beforeEach(() => {
    vm = getComponentVM(Component);
  });

  describe('getPeopleList() method', () => {
    it('doesn\'t trigger \'loadItems\' for empty source', (done) => {
      vm.attr('source', []);
      spyOn(vm, 'loadItems');
      vm.getPeopleList().then((result) => {
        expect(result.length).toBe(0);
        expect(vm.loadItems).not.toHaveBeenCalled();
        done();
      });
    });

    it('doesn\'t trigger \'loadItems\' for not defined source', (done) => {
      vm.attr('source', null);
      spyOn(vm, 'loadItems');
      vm.getPeopleList().then((result) => {
        expect(result.length).toBe(0);
        expect(vm.loadItems).not.toHaveBeenCalled();
        done();
      });
    });

    it('triggers \'loadItems\' for people without email', (done) => {
      let source = [{}, {}, {}];
      vm.attr('source', source);
      spyOn(vm, 'loadItems').and.returnValue(can.Deferred().resolve(source));
      vm.getPeopleList().then((result) => {
        expect(result.length).toBe(3);
        expect(vm.loadItems).toHaveBeenCalled();
        done();
      });
    });

    it('doesn\'t trigger \'loadItems\' for people with email', (done) => {
      let source = [{email: 'foo'}, {email: 'bar'}, {email: 'baz'}];
      vm.attr('source', source);
      spyOn(vm, 'loadItems').and.returnValue(can.Deferred().resolve(source));
      vm.getPeopleList().then((result) => {
        expect(result.length).toBe(source.length);
        expect(vm.loadItems).not.toHaveBeenCalled();
        done();
      });
    });
  });
});
