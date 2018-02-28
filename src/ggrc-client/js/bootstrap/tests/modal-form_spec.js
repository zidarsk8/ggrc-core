/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './test-template.mustache';
import '../modal-form';

describe('Flash message', function () {
  it('should trigger ajax:flash with extra data', function () {
    let triggerData = {
      error: can.mustache(template),
      data: {
        errors: [
          {
            msg: 'first error',
          },
          {
            msg: '2nd error',
          },
        ],
      },
    };

    spyOn($.prototype, 'trigger');

    $(document.body).trigger('ajax:flash', triggerData);

    expect($.prototype.trigger)
      .toHaveBeenCalledWith('ajax:flash', triggerData);
  });
});
