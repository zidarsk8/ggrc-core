/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('can.Control', function () {
  'use strict';

  let Control;

  beforeEach(function () {
    Control = can.Control.prototype;
  });

  describe('bindXHRToButton() method', function () {
    let dfd;

    beforeEach(function () {
      dfd = new can.Deferred();
    });

    function callBindXHRToButton(done, actualInnerHtml, newtext, disable) {
      let element = $('<button>' + actualInnerHtml + '</button>');

      // call bindXHRToButton()
      Control.bindXHRToButton(dfd, element, newtext, disable);

      // button should have 'disabled' class after call bindXHRToButton
      expect(element.hasClass('disabled')).toEqual(true);

      if (disable) {
        // button should have 'disabled' attr after call bindXHRToButton
        expect(element.attr('disabled')).toEqual('disabled');
      }

      if (newtext) {
        // button should have 'newText' before dfd.resolve()
        expect(element[0].innerHTML).toEqual(newtext);
      }

      dfd.then(
        setTimeout(function () {
          expect(element[0].innerHTML).toEqual(actualInnerHtml);

          // button should not have 'disabled' class after dfd.resolve()
          expect(element.hasClass('disabled')).toEqual(false);

          if (disable) {
            // button should not have 'disabled' attr after call bindXHRToButton
            expect(element.attr('disabled')).toEqual(undefined);
          }
          done();
        }, 3)
      );

      dfd.resolve();
    }

    it('bindXHRToButton() should save text of button', function (done) {
      callBindXHRToButton(done, 'HELLO WORLD');
    });

    it('bindXHRToButton() should save icon inside button', function (done) {
      callBindXHRToButton(done, '<i class="fa fa-icon"></i>');
    });

    it('bindXHRToButton() should save icon and text inside button',
      function (done) {
        callBindXHRToButton(done, '<i class="fa fa-icon"></i>My text');
      }
    );

    it('bindXHRToButton() should save text of button. Disable button',
      function (done) {
        callBindXHRToButton(done, 'HELLO WORLD', '', true);
      }
    );

    it('bindXHRToButton() should save icon inside button. New text',
      function (done) {
        callBindXHRToButton(done, '<i class="fa fa-icon"></i>', 'My new text');
      }
    );

    it('bindXHRToButton() should save text of button. New text. Disable button',
      function (done) {
        callBindXHRToButton(done, 'HELLO WORLD', '<i class="fa"></i>', true);
      }
    );

    it('bindXHRToButton() should resolve empty element',
      function (done) {
        let element = $('');

        // call bindXHRToButton()
        Control.bindXHRToButton(dfd, element);

        dfd.then(
          setTimeout(function () {
            // button should not have 'disabled' class after dfd.resolve()
            expect(element.hasClass('disabled')).toEqual(false);
            done();
          }, 3)
        );

        dfd.resolve();
      }
    );
  });
});
