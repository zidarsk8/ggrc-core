/*!
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.relatedReferenceUrls', function () {
  'use strict';

  var viewModel;
  var instance;

  beforeEach(function () {
    viewModel = GGRC.Components.getViewModel('relatedReferenceUrls');
    instance = {};
    viewModel.attr('instance', instance);
  });

  describe('createReferenceUrl() method', function () {
    var method;
    var url;

    beforeEach(function () {
      method = viewModel.createReferenceUrl.bind(viewModel);
      url = 'test.url';
    });

    it('should dispatch createReferenceUrl event', function () {
      spyOn(viewModel, 'dispatch');
      method(url);
      expect(viewModel.dispatch)
        .toHaveBeenCalledWith({
          type: 'createReferenceUrl',
          payload: url
        });
    });
  });

  describe('removeReferenceUrl() method', function () {
    var method;
    var url;

    beforeEach(function () {
      method = viewModel.removeReferenceUrl.bind(viewModel);
      url = 'test.url';
      spyOn(viewModel, 'dispatch');
    });

    it('should dispatch removeReferenceUrl event', function () {
      method(url);
      expect(viewModel.dispatch)
        .toHaveBeenCalledWith({
          type: 'removeReferenceUrl',
          payload: url
        });
    });
  });

  describe('toggleFormVisibility() method', function () {
    var method;

    beforeEach(function () {
      method = viewModel.toggleFormVisibility.bind(viewModel);
      spyOn(viewModel, 'moveFocusToInput');
    });

    it('should set new value for form visibility', function () {
      viewModel.attr('isFormVisible', true);
      method(false);
      expect(viewModel.attr('isFormVisible')).toEqual(false);
    });

    it('should clear create url form input by default', function () {
      viewModel.attr('value', 'foobar');
      method(true);
      expect(viewModel.attr('value')).toEqual('');
    });

    it('does not clear input field value if instructed to do so', function () {
      viewModel.attr('value', 'foobar');
      method(true, true);
      expect(viewModel.attr('value')).toEqual('foobar');
    });

    it('should set focus to form input field if visible', function () {
      viewModel.attr('isFormVisible', false);
      method(true);
      expect(viewModel.moveFocusToInput).toHaveBeenCalled();
    });
  });

  describe('submitCreateReferenceUrlForm() method', function () {
    var method;

    beforeEach(function () {
      method = viewModel.submitCreateReferenceUrlForm.bind(viewModel);
      spyOn(viewModel, 'createReferenceUrl');
      spyOn(viewModel, 'toggleFormVisibility');
      spyOn(GGRC.Errors, 'notifier');
    });

    describe('in case of non-empty input', function () {
      var url;

      beforeEach(function () {
        spyOn(viewModel, 'validateUserInput').and.returnValue(true);
        url = 'test.url';
      });

      it('should validate user input', function () {
        method(url);
        expect(viewModel.validateUserInput)
          .toHaveBeenCalledWith(url);
      });

      it('prevents adding duplicate URLs', function () {
        var matches;

        viewModel.attr('urls', [
          new can.Map({link: 'www.xyz.com', title: 'www.xyz.com'}),
          new can.Map({link: 'www.bar.com', title: 'www.bar.com'}),
          new can.Map({link: 'www.baz.org', title: 'www.baz.org'})
        ]);

        url = 'www.bar.com';
        method(url);

        matches = _.filter(viewModel.attr('urls'), {link: url});
        expect(matches.length).toEqual(1);  // still only 1
        expect(viewModel.createReferenceUrl).not.toHaveBeenCalled();
      });

      it('issues error notification when adding duplicate URLs', function () {
        viewModel.attr('urls', [
          new can.Map({link: 'www.xyz.com', title: 'www.xyz.com'}),
          new can.Map({link: 'www.bar.com', title: 'www.bar.com'}),
          new can.Map({link: 'www.baz.org', title: 'www.baz.org'})
        ]);

        method('www.bar.com');

        expect(GGRC.Errors.notifier).toHaveBeenCalledWith(
            'error', 'URL already exists.');
      });

      it('should create reference url', function () {
        method(url);
        expect(viewModel.createReferenceUrl)
          .toHaveBeenCalledWith(url);
      });

      it('should hide create url form', function () {
        method(url);
        expect(viewModel.toggleFormVisibility)
          .toHaveBeenCalledWith(false);
      });
    });

    describe('in case of empty input', function () {
      var url;

      beforeEach(function () {
        spyOn(viewModel, 'validateUserInput').and.returnValue(false);
        url = '   ';
      });

      it('should validate user input', function () {
        method(url);
        expect(viewModel.validateUserInput)
          .toHaveBeenCalledWith('');
      });

      it('should show create url form', function () {
        method(url);
        expect(viewModel.toggleFormVisibility)
          .toHaveBeenCalledWith(true);
      });

      it('should show notification with error message', function () {
        method(url);
        expect(GGRC.Errors.notifier).toHaveBeenCalledWith(
            'error', 'Please enter a URL.');
      });
    });
  });
});
