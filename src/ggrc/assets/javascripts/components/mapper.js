/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function(can, $) {
  $("body").on("click",
  "[data-toggle='modal-selector'], \
   [data-toggle='modal-relationship-selector'], \
   [data-toggle='multitype-object-modal-selector'], \
   [data-toggle='multitype-multiselect-modal-selector'], \
   [data-toggle='multitype-modal-selector']",
  function (ev) {
    console.log('Click ', arguments);
    ev.preventDefault();

    GGRC.Controllers.ModalSelector.launch($(ev.currentTarget), {});
  });
})(window.can, window.can.$);
