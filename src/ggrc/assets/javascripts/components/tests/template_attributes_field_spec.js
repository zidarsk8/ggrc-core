/*!
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.templateAttributesField', function () {
  'use strict';

  var Component;  // the component under test
  var scope;
  var pads = new can.Map({
    COMMENT: 0,
    ATTACHMENT: 1
  });
  var parentScope;

  beforeAll(function () {
    parentScope = new can.Map({
      attr: function () {
        return {};
      }
    });
    Component = GGRC.Components.get('templateAttributesField');
  });

  describe('denormalize_mandatory() method', function () {
    var denormalizeMandatory;

    beforeAll(function () {
      scope = Component.prototype.scope({}, parentScope);
      denormalizeMandatory = scope.denormalize_mandatory;
    });

    it('returns correct denormalized field', function () {
      var field = new can.Map({
        multi_choice_options: 'foo,bar,baz,bam',
        multi_choice_mandatory: '0,1,2,3'
      });
      var result = denormalizeMandatory(field, pads);

      expect(result.length).toEqual(4);
      expect(result[0].attachment).toEqual(false);
      expect(result[0].comment).toEqual(false);
      expect(result[1].attachment).toEqual(false);
      expect(result[1].comment).toEqual(true);
      expect(result[2].attachment).toEqual(true);
      expect(result[2].comment).toEqual(false);
      expect(result[3].attachment).toEqual(true);
      expect(result[3].comment).toEqual(true);
    });

    it('returns false for attachment and comment for missing mandatory',
      function () {
        var field = new can.Map({
          multi_choice_options: 'one,two,three,four,five',
          multi_choice_mandatory: '0,1,2'
        });
        var result = denormalizeMandatory(field, pads);

        expect(result.length).toEqual(5);
        expect(result[0].attachment).toEqual(false);
        expect(result[0].comment).toEqual(false);
        expect(result[1].attachment).toEqual(false);
        expect(result[1].comment).toEqual(true);
        expect(result[2].attachment).toEqual(true);
        expect(result[2].comment).toEqual(false);

        expect(result[3].attachment).toEqual(false);
        expect(result[3].comment).toEqual(false);
        expect(result[4].attachment).toEqual(false);
        expect(result[4].comment).toEqual(false);
      });

    it('returns values only for defined options', function () {
      var field = new can.Map({
        multi_choice_options: 'one,two,three',
        multi_choice_mandatory: '0,1,2,2,0'
      });
      var result = denormalizeMandatory(field, pads);

      expect(result.length).toEqual(3);
      expect(result[0].attachment).toEqual(false);
      expect(result[0].comment).toEqual(false);
      expect(result[1].attachment).toEqual(false);
      expect(result[1].comment).toEqual(true);
      expect(result[2].attachment).toEqual(true);
      expect(result[2].comment).toEqual(false);
    });
  });

  describe('normalize_mandatory() method', function () {
    var normalizeMandatory;

    beforeAll(function () {
      scope = Component.prototype.scope({}, parentScope);
      normalizeMandatory = scope.normalize_mandatory;
    });

    it('returns correct normalized attrs', function () {
      var attrs = new can.List([
        {attachment: false, comment: false},
        {attachment: true, comment: false},
        {attachment: false, comment: true},
        {attachment: true, comment: true}
      ]);
      var result = normalizeMandatory(attrs, pads);

      expect(result).toEqual('0,2,1,3');
    });
  });

  describe('emitting events', function () {
    describe('on-remove event', function () {
      var $root;  // the component's root DOM element
      var onRemoveCallback;

      beforeEach(function () {
        var $body = $('body');
        var docFragment;
        var htmlSnippet;
        var renderer;
        var templateContext;

        onRemoveCallback = jasmine.createSpy('onRemoveCallback');

        htmlSnippet = [
          '<template-field ',
          '  field="fieldDefinition"',
          '  can-on-remove="callMeOnRemove">',
          '</template-field>'
        ].join('');

        templateContext = new can.Map({
          types: new can.List([
            {
              type: 'Text',
              name: 'Text',
              text: 'Enter description'
            }
          ]),
          fieldDefinition: {
            attribute_type: 'Text'
          },
          callMeOnRemove: onRemoveCallback
        });

        renderer = can.view.mustache(htmlSnippet);
        docFragment = renderer(templateContext);
        $body.append(docFragment);

        $root = $body.find('template-field');
      });

      afterEach(function () {
        $root.remove();
      });

      it('invokes the provided handler when element is removed', function () {
        var $btnDelete = $root.find('.fa-trash').closest('a');
        $btnDelete.click();
        expect(onRemoveCallback).toHaveBeenCalled();
      });
    });
  });
});
