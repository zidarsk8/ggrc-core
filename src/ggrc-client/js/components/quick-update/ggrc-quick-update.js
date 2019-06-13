/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

/*
  This component is for quickly updating the properties of an object through form fields.

  Field updates trigger updates to the model automatically, even on the server.
*/
export default can.Component.extend({
  tag: 'ggrc-quick-update',
  leakScope: true,
  viewModel: can.Map.extend({
    instance: null,
  }),
  events: {
    'input, select change': function (el) {
      let isCheckbox = el.is('[type=checkbox][multiple]');
      let isDropdown = el.is('select');
      if (isCheckbox) {
        if (!this.viewModel.instance[el.attr('name')]) {
          this.viewModel.instance.attr(el.attr('name'), new can.List());
        }
        this.viewModel.instance
          .attr(el.attr('name'))
          .replace(
            _.filteredMap(
              this.element.find(
                'input[name="' + el.attr('name') + '"]:checked'),
              (el) => $(el).val())
          );
        this.element.find('input:checkbox').prop('disabled', true);
      } else {
        this.viewModel.instance.attr(el.attr('name'), el.val());
        if (isDropdown) {
          el.closest('dropdown-component').viewModel().attr('isDisabled', true);
        }
      }
      this.viewModel.instance.save().then(function () {
        if (isCheckbox) {
          this.element.find('input:checkbox').prop('disabled', false);
        } else if (isDropdown) {
          el.closest('dropdown-component').viewModel()
            .attr('isDisabled', false);
        }
      }.bind(this));
    },
  },
});
