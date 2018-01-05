/*
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Ctrl from '../info_pin_controller';

describe('CMS.Controllers.InfoPin', function () {
  let ctrlInst;

  beforeEach(function () {
    let fakeElement = document.createElement('div');
    ctrlInst = new Ctrl(fakeElement, {});
  });

  describe('existModals() method', function () {
    describe('returns true', function () {
      it('if there are modals on top of the info pane', function () {
        const modal = $('<div class="modal"></div>');
        $('body').append(modal);
        expect(ctrlInst.existModals()).toBe(true);
        modal.remove();
      });

      it('if there are an element with the role equals to "dialog" on top ' +
      'of the info pane', function () {
        const dialog = $('<div role="dialog"></div>');
        $('body').append(dialog);
        expect(ctrlInst.existModals()).toBe(true);
        dialog.remove();
      });
    });
  });

  describe('isEscapeKeyException() method', function () {
    describe('returns true', function () {
      let pinContentContainer;

      beforeEach(function () {
        pinContentContainer = $('<div class="pin-content"></div>');
      });

      describe('if passed target is inside the info pane and', function () {
        it('is content editable', function () {
          const target = $('<div></div>');
          target.attr('contenteditable', 'true');
          pinContentContainer.append(target);
          expect(ctrlInst.isEscapeKeyException(target)).toBe(true);
        });

        it('is button', function () {
          const target = $('<button></button>');
          pinContentContainer.append(target);
          expect(ctrlInst.isEscapeKeyException(target)).toBe(true);
        });

        it('is input', function () {
          const target = $('<input></input>');
          pinContentContainer.append(target);
          expect(ctrlInst.isEscapeKeyException(target)).toBe(true);
        });

        it('is textarea', function () {
          const target = $('<textarea></textarea>');
          pinContentContainer.append(target);
          expect(ctrlInst.isEscapeKeyException(target)).toBe(true);
        });

        it('has role attribute equals to "button"', function () {
          const target = $('<a role="button"></a>');
          pinContentContainer.append(target);
          expect(ctrlInst.isEscapeKeyException(target)).toBe(true);
        });

        it('has ".btn" class', function () {
          const target = $('<a class="btn"></a>');
          pinContentContainer.append(target);
          expect(ctrlInst.isEscapeKeyException(target)).toBe(true);
        });
      });
    });
  });

  describe('"{window} keyup"() method', function () {
    describe('when info pane is visible, escape key was pressed, ' +
    'event.target has .pin-content class or contains element inside itself ' +
    'with such class and there are no modals on top of the info pane',
    function () {
      let event;
      let methodName;

      beforeEach(function () {
        const ESCAPE_KEY_CODE = 27;
        const pinContentContainer = $('<div class="pin-content"></div>');
        methodName = '{window} keyup';
        event = {
          keyCode: ESCAPE_KEY_CODE,
          stopPropagation: jasmine.createSpy('stopPropagation'),
          target: pinContentContainer,
        };
        spyOn(ctrlInst, 'isPinVisible').and.returnValue(true);
        spyOn(ctrlInst, 'existModals').and.returnValue(false);
        spyOn(ctrlInst, 'isEscapeKeyException').and.returnValue(false);
      });

      it('closes info pane', function () {
        spyOn(ctrlInst, 'close');
        ctrlInst[methodName]({}, event);
        expect(ctrlInst.close).toHaveBeenCalled();
      });

      it('stops propagation for passed event', function () {
        ctrlInst[methodName]({}, event);
        expect(event.stopPropagation).toHaveBeenCalled();
      });
    });
  });

  describe('isPinVisible() method', function () {
    it('returns true if info pane is open', function () {
      ctrlInst.changeMaximizedState(true);
      expect(ctrlInst.isPinVisible()).toBe(true);
    });

    it('returns false if info pane is closed', function () {
      ctrlInst.close();
      expect(ctrlInst.isPinVisible()).toBe(false);
    });
  });
});
