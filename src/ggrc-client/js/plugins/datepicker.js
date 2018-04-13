/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/
(function ($, moment) {
  // On-demand creation of datepicker() objects
  let $body = $('body');
  let format = {
    changeMonth: true,
    changeYear: true,
    prevText: '',
    nextText: '',
    dateFormat: 'mm/dd/yy',
  };

  $body.on('focus', '[data-toggle="datepicker"]', function (ev) {
    let $this = $(this);

    if ($this.data('datepicker')) {
      return;
    }
    $this.datepicker(format);

    if ($this.is('[data-before], [data-after]')) {
      $this.trigger('change');
    }
  });

  // On-demand creation of datepicker() objects, initial date today or later
  $body.on('focus', '[data-toggle="datepicker_future_without_weekends"]',
    function (ev) {
      let $this = $(this);

      let noWeekendsFormat = Object.assign({
        beforeShowDay: $.datepicker.noWeekends,
      }, format);

      if ($this.data('datepicker')) {
        return;
      }
      $this.datepicker(noWeekendsFormat)
        .datepicker('option', 'minDate', new Date());
    }
  );
})(jQuery, moment);
