/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: ivan@reciprocitylabs.com
  Maintained By: ivan@reciprocitylabs.com
*/

describe('GGRC.Components.dropdown', function () {
  'use strict';

  describe('rendering option list', function () {
    var template;

    beforeAll(function () {
      template = can.view.mustache('<dropdown options-list="list"></dropdown>');
    });

    it('when input is an array of strings', function () {
      var list = ['a', 'b', 'c', 'd'];
      var frag = template({
        list: list
      });
      frag = $(frag);

      expect(frag.find('option').length).toEqual(list.length);
      $.each(frag.find('option'), function (index, el) {
        el = $(el);
        expect(el.attr('label')).toEqual(list[index]);
        expect(el.val()).toEqual(list[index]);
      });
    });

    it('when input is an array of values', function () {
      var list = [{
        title: 'a',
        value: 1
      }, {
        title: 'b',
        value: 2
      }, {
        title: 'c',
        value: 3
      }, {
        title: 'd',
        value: 4
      }];
      var frag = template({
        list: list
      });
      frag = $(frag);

      expect(frag.find('option').length).toEqual(list.length);
      $.each(frag.find('option'), function (index, el) {
        var item = list[index];
        el = $(el);
        expect(el.attr('label')).toEqual(item.title);
        expect(el.val()).toEqual(String(item.value));
      });
    });

    it('when input is an array of grouped values', function () {
      var list = [{
        title: 'a',
        value: 1
      }, {
        group: 'AA',
        subitems: [{
          title: 'aa',
          value: 11
        }, {
          title: 'ab',
          value: 12
        }, {
          title: 'ac',
          value: 13
        }, {
          title: 'ad',
          value: 14
        }]
      }, {
        group: 'BB',
        subitems: [{
          title: 'ba',
          value: 21
        }, {
          title: 'bb',
          value: 22
        }, {
          title: 'bc',
          value: 23
        }, {
          title: 'bd',
          value: 24
        }]
      }];
      var frag = template({
        list: list
      });
      var groups = _.filter(list, function (item) {
        return item.group;
      });
      frag = $(frag);

      expect(frag.find('optgroup').length).toEqual(groups.length);
      $.each(frag.find('optgroup'), function (index, el) {
        var item = groups[index];
        el = $(el);
        expect(el.attr('label')).toEqual(item.group);
      });
      $.each(frag.find('optgroup:first options'), function (index, el) {
        var subitem = list[1].subitems[index];
        el = $(el);
        expect(el.attr('label')).toEqual(subitem.title);
        expect(el.val()).toEqual(String(subitem.value));
      });
    });
  });
});
