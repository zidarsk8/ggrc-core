/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  'use strict';

  GGRC.Components('multiselectDropdown', {
    tag: 'multiselect-dropdown',
    template: can.view(
      GGRC.mustache_path +
      '/components/dropdown/multiselect_dropdown.mustache'
    ),
    viewModel: {
      _stateWasUpdated: '',
      selected: [],
      plural: '@',
      placeholder: '@',
      element: '',
      define: {
        elementWidth: {
          type: 'number',
          value: 240
        },
        _displayValue: {
          get: function () {
            return this.attr('selected').map(function (item) {
              return item.attr('value');
            }).join(', ');
          }
        },
        _selectedAll: {
          type: 'boolean',
          value: false,
          get: function () {
            var options = this.attr('options') || [];

            return Array.prototype.every.call(options, function (item) {
              return item.attr('checked');
            });
          },
          set: function (value) {
            var options = this.attr('options') || [];

            options.forEach(function (option) {
              option.attr('checked', value);
            });

            return value;
          }
        },
        isOpen: {
          type: 'boolean',
          value: false
        },
        options: {
          type: '*'
        }
      },
      updateSelected: function (item) {
        var selected = this.attr('selected');
        var index = -1;

        this.attr('_stateWasUpdated', true);

        if (item.checked) {
          selected.push(item);
          return;
        }

        index = selected.map(function (selectedItem) {
          return selectedItem.value;
        }).indexOf(item.value);

        if (index > -1) {
          selected.splice(index, 1);
        }
      },
      dropdownClosed: function (el, ev, scope) {
        // don't trigger event if state didn't change
        if (!this.attr('_stateWasUpdated')) {
          return;
        }

        this.attr('_stateWasUpdated', false);
        can.trigger(el, 'multiselect:closed', [this.attr('selected')]);
      },
      changeOpenCloseState: function (el, ev) {
        if (!this.attr('isOpen')) {
          if (this.attr('canBeOpen')) {
            this.attr('canBeOpen', false);
            this.attr('isOpen', true);
          }
        } else {
          this.attr('isOpen', false);
          this.attr('canBeOpen', false);
          this.dropdownClosed(this.element);
        }
      },
      openDropdown: function (el, ev) {
        // we should save element of component.
        // it necessary for 'can.trigger'
        if (el && !this.element) {
          this.element = el;
        }

        // this attr needed when page has any components
        this.attr('canBeOpen', true);
      },
      dropdownBodyClick: function (ev) {
        ev.stopPropagation();
      }
    },
    events:
    {
      '{options} change': function (scope, ev, propertyName) {
        var target = ev.target;

        // igore all propetries except 'checked'
        if (propertyName.indexOf('checked') === -1) {
          return;
        }

        this.viewModel.updateSelected(target);
      },
      '{window} click': function (el, ev) {
        this.viewModel.changeOpenCloseState('', ev);
      }
    }
  });
})(window.can, window.can.$);
