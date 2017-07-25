/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

'use strict';

describe('GGRC.Utils.AdvancedSearch', function () {
  describe('buildFilter() method', function () {
    it('builds correct statuses with "ANY" operator', function () {
      var items = [
        GGRC.Utils.AdvancedSearch.create.state({
          items: ['Active', 'Draft', 'Deprecated'],
          operator: 'ANY'
        })
      ];
      var expectedResult = '("Status"="Active" ' +
                           'OR "Status"="Draft" ' +
                           'OR "Status"="Deprecated")';

      expect(GGRC.Utils.AdvancedSearch.buildFilter(items))
        .toBe(expectedResult);
    });

    it('builds correct statuses with "NONE" operator', function () {
      var items = [
        GGRC.Utils.AdvancedSearch.create.state({
          items: ['Active', 'Draft', 'Deprecated'],
          operator: 'NONE'
        })
      ];
      var expectedResult = '("Status"!="Active" ' +
                           'AND "Status"!="Draft" ' +
                           'AND "Status"!="Deprecated")';

      expect(GGRC.Utils.AdvancedSearch.buildFilter(items))
        .toBe(expectedResult);
    });

    it('builds correct filter string', function () {
      var items = [
        GGRC.Utils.AdvancedSearch.create.state({
          items: ['Active', 'Draft'],
          operator: 'ANY'
        }),
        GGRC.Utils.AdvancedSearch.create.operator('AND'),
        GGRC.Utils.AdvancedSearch.create.attribute({
          field: 'Title',
          operator: '~',
          value: ' test'
        }),
        GGRC.Utils.AdvancedSearch.create.operator('OR'),
        GGRC.Utils.AdvancedSearch.create.group([
          GGRC.Utils.AdvancedSearch.create.attribute({
            field: 'Para',
            operator: '=',
            value: 'meter'
          }),
          GGRC.Utils.AdvancedSearch.create.operator('AND'),
          GGRC.Utils.AdvancedSearch.create.attribute({
            field: 'Other',
            operator: '~=',
            value: 'value '
          })
        ])
      ];
      var expectedResult = '("Status"="Active" OR "Status"="Draft") ' +
                           'AND "Title" ~ "test" ' +
                           'OR ("Para" = "meter" AND "Other" ~= "value")';
      expect(GGRC.Utils.AdvancedSearch.buildFilter(items))
        .toBe(expectedResult);
    });

    it('builds correct mapping filters', function () {
      var items = [
        GGRC.Utils.AdvancedSearch.create.mappingCriteria({
          objectName: 'product',
          filter: GGRC.Utils.AdvancedSearch.create.attribute({
            field: 'title',
            operator: '~',
            value: 'A'
          }),
          mappedTo: GGRC.Utils.AdvancedSearch.create.mappingCriteria({
            objectName: 'system',
            filter: GGRC.Utils.AdvancedSearch.create.attribute({
              field: 'title',
              operator: '~',
              value: 'B'
            })
          })
        }),
        GGRC.Utils.AdvancedSearch.create.operator('AND'),
        GGRC.Utils.AdvancedSearch.create.mappingCriteria({
          objectName: 'control',
          filter: GGRC.Utils.AdvancedSearch.create.attribute({
            field: 'title',
            operator: '~',
            value: 'C'
          }),
          mappedTo: GGRC.Utils.AdvancedSearch.create.group([
            GGRC.Utils.AdvancedSearch.create.mappingCriteria({
              objectName: 'system',
              filter: GGRC.Utils.AdvancedSearch.create.attribute({
                field: 'title',
                operator: '~',
                value: 'D'
              })
            }),
            GGRC.Utils.AdvancedSearch.create.operator('OR'),
            GGRC.Utils.AdvancedSearch.create.mappingCriteria({
              objectName: 'system',
              filter: GGRC.Utils.AdvancedSearch.create.attribute({
                field: 'title',
                operator: '~',
                value: 'E'
              })
            })
          ])
        })
      ];
      var expectedFilters = '#__previous__,1# AND #__previous__,4#';
      var expectedRequest = [
        {
          object_name: 'system',
          type: 'ids',
          filters: {
            expression: {
              left: 'title',
              op: {name: '~'},
              right: 'B'
            },
            keys: ['title'],
            order_by: {
              keys: [],
              order: '',
              compare: null
            }
          }
        },
        {
          object_name: 'product',
          type: 'ids',
          filters: {
            expression: {
              left: {
                left: 'title',
                op: {name: '~'},
                right: 'A'
              },
              op: {name: 'AND'},
              right: {
                object_name: '__previous__',
                op: {name: 'relevant'},
                ids: ['0']
              }
            },
            keys: ['title'],
            order_by: {
              keys: [],
              order: '',
              compare: null
            }
          }
        },
        {
          object_name: 'system',
          type: 'ids',
          filters: {
            expression: {
              left: 'title',
              op: {name: '~'},
              right: 'D'
            },
            keys: ['title'],
            order_by: {
              keys: [],
              order: '',
              compare: null
            }
          }
        },
        {
          object_name: 'system',
          type: 'ids',
          filters: {
            expression: {
              left: 'title',
              op: {name: '~'},
              right: 'E'
            },
            keys: ['title'],
            order_by: {
              keys: [],
              order: '',
              compare: null
            }
          }
        },
        {
          object_name: 'control',
          type: 'ids',
          filters: {
            expression: {
              left: {
                left: 'title',
                op: {name: '~'},
                right: 'C'
              },
              op: {name: 'AND'},
              right: {
                left: {
                  object_name: '__previous__',
                  op: {name: 'relevant'},
                  ids: ['2']
                },
                op: {name: 'OR'},
                right: {
                  object_name: '__previous__',
                  op: {name: 'relevant'},
                  ids: ['3']
                }
              }
            },
            keys: ['title'],
            order_by: {
              keys: [],
              order: '',
              compare: null
            }
          }
        }
      ];
      var request = [];

      var result = GGRC.Utils.AdvancedSearch.buildFilter(items, request);

      expect(result).toBe(expectedFilters);
      expect(JSON.parse(JSON.stringify(request))).toEqual(expectedRequest);
    });
  });
});
