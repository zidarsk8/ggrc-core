/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.revisionsComparer', function () {
  'use strict';

  var Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('RevisionsComparer');
  });

  describe('prepareInstances() method', function () {
    var fakeData;
    var method;  // the method under test

    beforeEach(function () {
      method = Component.prototype.scope.prepareInstances;
      fakeData = [
        {
          id: 1,
          content: new can.Map({id: 1}),
          resource_type: 'Control'
        }, {
          id: 2,
          content: new can.Map({id: 1}),
          resource_type: 'Control'
        }
      ];
    });

    it('returns instances of necessary type and with isRevision', function () {
      var result = method(fakeData);
      result.forEach(function (item) {
        expect(item.instance instanceof CMS.Models.Control).toBeTruthy();
        expect(item.instance.type).toBe('Control');
        expect(item.instance.isRevision).toBe(true);
      });
    });

    it('returns the same length of instances as passed', function () {
      var result = method(fakeData);
      expect(result.length).toBe(fakeData.length);
    });

    it('returns the same data as passed with extra properties', function () {
      var result = method(fakeData);
      var data = fakeData;
      result.forEach(function (item, index) {
        expect(item.instance.id).toEqual(data[index].content.id);
      });
    });

    it('adds person stubs to access control list items', function () {
      var result;

      fakeData.forEach(function (item, i) {
        var acl = new can.List([
          {ac_role_id: i * 10, person_id: i * 10},
          {ac_role_id: i * 10, person_id: i * 10}
        ]);
        item.content.attr('access_control_list', acl);
      });

      result = method(fakeData);

      function checkAclItem(item) {
        expect(item.person).toBeDefined();
        expect(item.person.type).toEqual('Person');
        expect(item.person.id).toEqual(item.person_id);
      }

      result.forEach(function (item) {
        item.instance.access_control_list.forEach(checkAclItem);
      });
    });
  });

  describe('getInfopanes() method', function () {
    var fakeHTML;
    var method;  // the method under test

    beforeEach(function () {
      method = Component.prototype.scope.getInfopanes;
      fakeHTML = $('<div>' +
                      '<div class="info">' +
                        '<div class="tier-content"></div>' +
                      '</div>' +
                      '<div class="info">' +
                        '<div class="tier-content"></div>' +
                      '</div>' +
                    '</div>');
    });

    it('returns all info panes under the given element', function () {
      var result = method(fakeHTML);
      expect(result.length).toBe(2);
    });
  });

  describe('getCAPanes() method', function () {
    var fakeHTML;
    var method;  // the method under test

    beforeEach(function () {
      method = Component.prototype.scope.getCAPanes;
      fakeHTML = $('<div>' +
                      '<div class="info">' +
                        '<custom-attributes></custom-attributes>' +
                      '</div>' +
                      '<div class="info">' +
                        '<custom-attributes></custom-attributes>' +
                      '</div>' +
                    '</div>');
    });

    it('returns all panes with custom attributes', function () {
      var result = method(fakeHTML);
      expect(result.length).toBe(2);
    });
  });

  describe('getAttachmentsDfds() method', function () {
    var method;
    var revisions;

    beforeEach(function () {
      var prepareInstancesMethod = Component.prototype.scope.prepareInstances;
      var fakeData = [
        {
          id: 1,
          content: new can.Map({id: 1}),
          resource_type: 'Control'
        }, {
          id: 2,
          content: new can.Map({id: 1}),
          resource_type: 'Control'
        }
      ];

      method = Component.prototype.scope.getAttachmentsDfds
        .bind(Component.prototype.scope);
      revisions = new can.List(prepareInstancesMethod(fakeData));
    });

    it('getAttachmentsDfds() should return 2 dfds', function () {
      var dfds = method(revisions);
      expect(dfds.length).toEqual(2);
    });

    it('getAttachmentsDfds() should return 3 dfds', function () {
      var dfds;
      revisions[0].attr('instance').folders = [{id: 'EWheNKvwjhrcwWer'}];
      dfds = method(revisions);
      expect(dfds.length).toEqual(3);
    });

    it('getAttachmentsDfds() should return 4 dfds', function () {
      var dfds;
      revisions[0].attr('instance').folders = [{id: 'EWheNKvwjhrcwWer'}];
      revisions[1].attr('instance').folders = [{id: 'vewbetWhercwWer'}];
      dfds = method(revisions);
      expect(dfds.length).toEqual(4);
    });

    it('getAttachmentsDfds() should return empty array', function () {
      var dfds = method();
      expect(dfds.length).toEqual(0);
    });
  });
});
