/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
/*
describe('GGRC.Components.customAttributesObject', function () {
  'use strict';

  var Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('customAttributesObject');
  });

  describe('save() method', function () {
    var save;  // the method under test
    var scope;
    var scope_;
    var customAttributeValues;
    var noConflictAssessment;
    var hasConflictAssessment;
    var noConflictSave;
    var hasConflictSave;

    beforeAll(function () {
      noConflictSave = function () {
        var deferred = can.Deferred().resolve();
        this.attr('value', this.attr('value').split(':')[0]);
        return deferred.promise();
      };

      hasConflictSave = function () {
        var deferred = $.Deferred().resolve();
        this.attr('value', 'changed');
        return deferred.promise();
      };
    });

    beforeEach(function () {
      scope_ = Component.prototype.scope;

      scope = new can.Map({
        setModified: scope_.setModified,
        valueId: '0',
        def: {
          id: 0
        }
      });

      save = scope_.save.bind(scope);

      spyOn(GGRC.Errors, 'notifier');

      customAttributeValues = [
        {id: 1},
        {id: 0, attribute_object: {id: 2}}
      ];

      noConflictAssessment = {
        save: noConflictSave.bind(scope),
        custom_attribute_values: customAttributeValues
      };
      hasConflictAssessment = {
        save: hasConflictSave.bind(scope),
        custom_attribute_values: customAttributeValues
      };
    });

    it('should show success message on no conflict on input fields',
      function () {
        scope.attr('instance', noConflictAssessment);
        scope.attr('type', 'input');
        scope.attr('value', 'test');

        save();

        expect(GGRC.Errors.notifier).toHaveBeenCalledWith('success', 'Saved');
      }
    );

    it('should not show success message on conflict on input fields',
      function () {
        scope.attr('instance', hasConflictAssessment);
        scope.attr('type', 'input');
        scope.attr('value', 'test');

        save();

        expect(GGRC.Errors.notifier).not.toHaveBeenCalled();
      }
    );

    it('should show success message on no conflict on map person fields',
      function () {
        scope.attr('instance', noConflictAssessment);
        scope.attr('type', 'person');
        scope.attr('value', 'Person:2');

        save();

        expect(GGRC.Errors.notifier).toHaveBeenCalledWith('success', 'Saved');
      }
    );

    it('should not show success message on conflict on map person fields',
      function () {
        scope.attr('instance', hasConflictAssessment);
        scope.attr('type', 'person');
        scope.attr('value', 'Person:1');

        save();

        expect(GGRC.Errors.notifier).not.toHaveBeenCalled();
      }
    );
  });
});
*/
