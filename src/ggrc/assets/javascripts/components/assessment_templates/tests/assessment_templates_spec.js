/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.assessmentTemplates', function () {
  'use strict';

  var Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('assessmentTemplates');
  });

  describe('_selectInitialTemplate() method', function () {
    var mapper;
    var method;  // the method under test
    var templates;

    beforeAll(function () {
      method = Component.prototype.scope._selectInitialTemplate;
    });

    beforeEach(function () {
      mapper = new can.Map({
        assessmentTemplate: ''
      });

      templates = [
        {
          title: 'No Template',
          value: ''
        },
        {
          group: 'FooBarBaz objects',
          subitems: [
            {title: 'object Foo', value: 'foo'},
            {title: 'object Bar', value: 'bar'},
            {title: 'object Baz', value: 'baz'}
          ]
        },
        {
          group: 'Animal objects',
          subitems: [
            {title: 'Elephant Dumbo', value: 'elephant'},
            {title: 'Flying Pig', value: 'pig'},
            {title: 'Tiny Mouse', value: 'mouse'}
          ]
        }
      ];
    });

    it('gracefully handles a missing mapper object', function () {
      try {
        method(templates, null);
      } catch (err) {
        fail('Handling a non-existing mapper object failed: ' + err.msg);
      }
    });

    it('selects the first item from the first option group', function () {
      mapper.attr('assessmentTemplate', 'template-123');
      method(templates, mapper);
      expect(mapper.assessmentTemplate).toEqual('foo');
    });

    it('leaves the current template unchanged if only a dummy value in ' +
      'the templates list',
      function () {
        mapper.attr('assessmentTemplate', 'template-123');
        templates.splice(1);  // keep only the 1st (dummy) option

        method(templates, mapper);

        expect(mapper.assessmentTemplate).toEqual('template-123');
      }
    );

    it('leaves the current template unchanged if first object group empty',
      function () {
        mapper.attr('assessmentTemplate', 'template-123');
        templates[1].subitems.length = 0;
        spyOn(console, 'warn');  // just to silence it

        method(templates, mapper);

        expect(mapper.assessmentTemplate).toEqual('template-123');
      }
    );

    it('issues a warning if an empty group is encountered', function () {
      var expectedMsg = [
        'GGRC.Components.assessmentTemplates: ',
        'An empty template group encountered, possible API error'
      ].join('');

      spyOn(console, 'warn');
      templates[1].subitems.length = 0;

      method(templates, mapper);

      expect(console.warn).toHaveBeenCalledWith(expectedMsg);
    });

    it('selects the first non-dummy value if it precedes all object groups',
      function () {
        mapper.attr('assessmentTemplate', 'template-123');
        templates.splice(1, 0, {title: 'No Group Template', value: 'single'});

        method(templates, mapper);

        expect(mapper.assessmentTemplate).toEqual('single');
      }
    );
  });
});
