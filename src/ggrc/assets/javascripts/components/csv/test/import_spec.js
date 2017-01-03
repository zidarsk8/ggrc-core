/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.csvImportWidget', function () {
  'use strict';

  var Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('csvImportWidget');
  });

  describe('scope.states() method', function () {
    var method;  // the method under test
    var fakeScope;

    beforeEach(function () {
      fakeScope = new can.Map({});
      method = Component.prototype.scope.states.bind(fakeScope);
    });

    describe('the returned "import" state config\'s isDisabled() method',
      function () {
        var isDisabled;  // the method under test

        /**
         * A factory function for dummy import block info objects.
         *
         * @param {String} objectType - the name of the block, usually the object
         *   type that is represented by it, e.g. "Assessment"
         * @param {Object} rowCounts - the object containing the counts for
         *   different groups of of rows
         *   @param {Number} [rowCounts.totalRows=0] - the number of all rows
         *     in the block, must equal (created + updated + deleted + ignored)
         *   @param {Number} [rowCounts.created=0] - total rows to create
         *   @param {Number} [rowCounts.updated=0] - total rows to update
         *   @param {Number} [rowCounts.deleted=0] - total rows to delete
         *   @param {Number} [rowCounts.ignored=0] - total rows to ignore
         *
         * @return {can.Map} - a new dummy import block info instance
         */
        function makeImportBlock(objectType, rowCounts) {
          var COUNT_FIELD_NAMES = ['created', 'updated', 'deleted', 'ignored'];
          var COUNT_ERR = 'Invalid row counts, the sum of created, updated, ' +
              'deleted, and ignored must equal the total row count.';

          var blockOptions = {
            name: objectType,
            rows: rowCounts.totalRows || 0
          };
          var combinedCount = 0;

          COUNT_FIELD_NAMES.forEach(function (field) {
            blockOptions[field] = rowCounts[field] || 0;
            combinedCount += blockOptions[field];
          });

          if (combinedCount !== blockOptions.rows) {
            throw new Error(COUNT_ERR);
          }

          return new can.Map(blockOptions);
        }

        beforeEach(function () {
          var importStateConfig;
          fakeScope.attr('state', 'import');
          importStateConfig = method();
          isDisabled = importStateConfig.isDisabled;
        });

        it('returns true when import blocks list not available', function () {
          var result;
          fakeScope.attr('import', null);
          result = isDisabled();
          expect(result).toBe(true);
        });

        it('returns true when import blocks list is empty', function () {
          var result;
          fakeScope.attr('import', []);
          result = isDisabled();
          expect(result).toBe(true);
        });

        it('returns true if all blocks in the list empty', function () {
          var result;
          var importBlocks = [
            makeImportBlock('Assessment', {totalRows: 0}),
            makeImportBlock('Market', {totalRows: 0})
          ];
          fakeScope.attr('import', importBlocks);

          result = isDisabled();

          expect(result).toBe(true);
        });

        it('returns true for non-empty block that have all rows ignored',
          function () {
            var result;
            var importBlocks = [
              makeImportBlock('Assessment', {totalRows: 4, ignored: 4})
            ];
            fakeScope.attr('import', importBlocks);

            result = isDisabled();

            expect(result).toBe(true);
          }
        );

        it('returns false if there are non-empty blocks containing ' +
          'non-ignored lines',
          function () {
            var result;
            var importBlocks = [
              makeImportBlock('Assessment', {totalRows: 4, ignored: 4}),
              makeImportBlock('Market', {totalRows: 0, ignored: 0}),
              makeImportBlock(
                'Contract', {totalRows: 3, created: 1, ignored: 2})
            ];
            fakeScope.attr('import', importBlocks);

            result = isDisabled();

            expect(result).toBe(false);
          }
        );
      }
    );
  });
});
