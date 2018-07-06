/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './multiselect-dropdown-wrapper.mustache';

export default can.Component.extend({
  tag: 'multiselect-dropdown-wrapper',
  template: template,
  viewModel: {
    placeholder: '@',
    define: {
      /*
        Multiselect-dropdown wrapper when data should be fetched first
        {modelName}: Name of CMS.Model to fetch
        {(selected)}: Two-way binding parent`s target attribute
      */
      modelName: {
        set(newModelName) {
          if (CMS.Models[newModelName]) {
            CMS.Models[newModelName].findAll()
              .done(this.prepareOptions.bind(this));

            return newModelName;
          }
        },
      },
    },
    prepareOptions: function (items) {
      let selected = this.attr('selected');
      let preparedOptions = [];
      let selectedInternal = [];

      items.forEach((item)=> {
        let isSelected = _.find(selected, (selectedItem)=> {
          return selectedItem.id === item.id;
        });

        let option = {
          value: item.name,
          id: item.id,
          checked: isSelected ? true : false,
        };

        preparedOptions.push(option);

        if (isSelected) {
          selectedInternal.push(option);
        }
      });

      // preparedOptions sent down to multiselect-dropdown
      this.attr('preparedOptions', preparedOptions);

      // selectedInternal is input models
      // converted into multiselect-dropdown format
      this.attr('selectedInternal', selectedInternal);
    },
  },
  events: {
    /*
      Update received from multiselect-dropdown
      Retrieved from Model.cache by Id and sent up to parent`s 'selected'
    */
    'multiselect-dropdown multiselect:changed':
      function (element, event, newSelected) {
        let self = this;

        /* reuse object to allow sort-by properly react
        on selected change */
        let selected = self.viewModel.attr('selected') || [];
        // remove all old items
        selected.splice(0);
        // add all new items from Cache
        newSelected.forEach((item) => {
          selected.push(CMS.Models[self.viewModel.modelName]
            .findInCacheById(item.id));
        });
      },
  },
});
