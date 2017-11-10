/*
  Copyright (C) 2017 Google Inc., authors, and contributors
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.assessmentInfoPane', function () {
  let vm;

  beforeEach(function () {
    vm = GGRC.Components.getViewModel('assessmentInfoPane');
    vm.attr('instance', {});
  });

  describe('editMode attribute', function () {
    const editableStatuses = ['Not Started', 'In Progress', 'Rework Needed'];
    const nonEditableStates = ['In Review', 'Completed', 'Deprecated'];
    const allStatuses = editableStatuses.concat(nonEditableStates);

    describe('get() method', function () {
      it('returns false if instance is archived', function () {
        vm.attr('instance.archived', true);

        allStatuses.forEach((status) => {
          vm.attr('instance.status', status);
          expect(vm.attr('editMode')).toBe(false);
        });
      });

      describe('if instance is not archived', function () {
        it('returns true if instance status is editable otherwise false',
        function () {
          allStatuses.forEach((status) => {
            vm.attr('instance.status', status);
            expect(vm.attr('editMode'))
              .toBe(editableStatuses.includes(status));
          });
        });
      });
    });
  });
});
