/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

let $body = $('body');
let $window = $(window);

// We remove loading class
$window.on('load', function () {
  $('html').removeClass('no-js');
});

// Make all external links open in new window.
jQuery(function ($) {
  $body.on('click', 'a[href]:not([target])', function (e) {
    if (!e.isDefaultPrevented()) {
      if (/^http/.test(this.protocol)
        && this.hostname !== window.location.hostname) {
        e.preventDefault();
        window.open(this.href);
      }
    }
  });
});

$(function () {
  $('body').on(
    'click',
    '[data-toggle="user-roles-modal-selector"]',
    async function (ev) {
      let $this = $(this);
      let options = $this.data('modal-selector-options');
      let dataSet = Object.assign({}, $this.data());
      let objectParams = $this.attr('data-object-params');
      const {
        getOptionSet,
        'default': userRolesModalSelector,
      } = await import(
        /* webpackChunkName: "userRoleModalSelector" */
        './controllers/contributions'
      );
      dataSet.params = objectParams && JSON.parse(
        objectParams.replace(/\\n/g, '\\n')
      );

      can.each($this.data(), function (v, k) {
        //  This is just a mapping of keys to underscored keys
        let newKey = k.replace(
          /[A-Z]/g,
          function (str) {
            return '_' + str.toLowerCase();
          }
        );

        dataSet[newKey] = v;
        //  If we changed the key at all, delete the original
        if (newKey !== k) {
          delete dataSet[k];
        }
      });

      if (typeof options === 'string') {
        options = getOptionSet(options, dataSet);
      }

      ev.preventDefault();
      ev.stopPropagation();

      // Trigger the controller
      userRolesModalSelector.launch($this, options);
    });
});

function openMapperByElement(ev, disableMapper) {
  let btn = $(ev.currentTarget);
  let data = {};

  can.each(btn.data(), function (val, key) {
    data[can.camelCaseToUnderscore(key)] = val;
  });

  if (data.tooltip) {
    data.tooltip.hide();
  }

  if (!data.clickable) {
    ev.preventDefault();
  }

  import(/* webpackChunkName: "mapper" */ './controllers/mapper/mapper')
    .then((mapper) => {
      mapper.ObjectMapper.openMapper(data, disableMapper, btn);
    });
}

$body.on('openMapper', (el, ev, disableMapper) => {
  openMapperByElement(ev, disableMapper);
});

$body.on('click', ['unified-mapper', 'unified-search']
  .map((val) => `[data-toggle="${val}"]`).join(', '), (ev, disable) => {
  openMapperByElement(ev, disable);
});
