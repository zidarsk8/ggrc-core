/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can) {
  'use strict';

  let tag = 'object-selection';
  /**
   * Object Selection component
   */
  can.Component.extend('objectSelection', {
    tag: tag,
    viewModel: {
      selectedItems: [],
      items: [],
      // This is an array by default replace with deferred on actual load
      allItems: [],
      disabledIds: [],
      refreshSelection: null,
      allSelected: false,
      selectAllCheckboxValue: false,
      select: function (id, type) {
        if (this.indexOfSelected(id, type) < 0) {
          this.attr('selectedItems').push({
            id: id,
            type: type,
          });
          this.markItem(id, type, true);
        } else {
          console.warn('Same Object is Selected Twice!' +
            ' id: ', id, ' type:', type);
        }
      },
      deselect: function (id, type) {
        let list = this.attr('selectedItems');
        let index = this.indexOfSelected(id, type);
        if (index >= 0) {
          list.splice(index, 1);
          this.markItem(id, type, false);
          this.attr('allSelected', false);
        }
      },
      indexOfSelected: function (id, type) {
        let list = this.attr('selectedItems');
        let index = -1;
        list.each(function (item, i) {
          if (id === item.attr('id') && type === item.attr('type')) {
            index = i;
            return false;
          }
        });
        return index;
      },
      markItem: function (id, type, isSelected) {
        this.attr('items').each(function (item) {
          if (id === item.attr('id') && type === item.attr('type')) {
            item.attr('markedSelected', isSelected);
            return false;
          }
        });
      },
      toggleItems: function (isSelected) {
        this.attr('items').each(function (item) {
          if (!item.attr('isDisabled')) {
            item.attr('markedSelected', isSelected);
          }
        });
      },
      markSelectedItems: function () {
        this.attr('selectedItems').each(function (selected) {
          this.markItem(selected.attr('id'), selected.attr('type'), true);
        }.bind(this));
      },
      emptySelection: function () {
        this.attr('allSelected', false);
        // Remove all selected items
        this.attr('selectedItems').replace([]);
        // Remove visual selection
        this.toggleItems(false);
      },
      deselectAll: function () {
        this.emptySelection();
      },
      selectAll: function () {
        let selectedItems;
        let disabledIds = this.attr('disabledIds');
        this.attr('allSelected', true);
        // Replace with actual items loaded from Query API
        this.attr('allItems')
          .done(function (allItems) {
            selectedItems = allItems.filter(function (item) {
              return disabledIds.indexOf(item.id) < 0;
            });
            this.attr('selectedItems').replace(selectedItems);
            // Add visual selection
            this.toggleItems(true);
          }.bind(this))
          .fail(function () {
            this.clearSelection();
          }.bind(this));
      },
    },
    events: {
      '{viewModel} refreshSelection': function (scope, ev, refreshSelection) {
        if (refreshSelection) {
          this.viewModel.emptySelection();
        }
      },
      '{viewModel.items} add': function () {
        this.viewModel.markSelectedItems();
      },
      'object-selection-item selectItem': function (el, ev, id, type) {
        this.viewModel.select(id, type);
      },
      'object-selection-item deselectItem': function (el, ev, id, type) {
        this.viewModel.deselect(id, type);
      },
      '{viewModel} selectAllCheckboxValue': function (scope, ev, value) {
        if (value) {
          this.viewModel.selectAll();
        } else {
          this.viewModel.deselectAll();
        }
      },
    },
  });
})(window.can);
