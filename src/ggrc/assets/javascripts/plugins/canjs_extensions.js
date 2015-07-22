/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/
(function($, can) {
  // a few core CanJS extensions below.
  // Core validation for fields not being "blank", i.e.
  // having no content when outside spaces are trimmed away.
  can.Model.validationMessages.non_blank = can.Map.validationMessages.non_blank = 'cannot be blank';
  can.Model.validateNonBlank = can.Map.validateNonBlank = function (attrNames, options) {
    can.Map.validate.call(this, attrNames, options, function (value) {
      if (value === undefined || value === null || typeof value.trim === "function" && value.trim() === '') {
        return this.constructor.validationMessages.non_blank;
      }
    });
  };
  can.Model.validateContact = can.Map.validateContact = function (attrNames, options) {
    this.validate.call(this, attrNames, options, function (newVal, prop) {
      var reified_contact = this.contact ? this.contact.reify() : false,
          contact_has_email_address = reified_contact ? reified_contact.email : false;

      // This check will not work until the bug introduced with commit 8a5f600c65b7b45fd34bf8a7631961a6d5a19638
      // is resolved.
      if (!contact_has_email_address) {
        return "No valid contact selected for assignee";
      }
    });
  };

  // Adding reduce, a generally useful array comprehension.
  //  Bitovi decided against including it in core CanJS, but
  //  adding it here for easy universal use across can.List
  //  as well as arrays.
  if (!can.reduce) {
    can.reduce = function(a, f, i) {
      if (a == null) return null;
      return [].reduce.apply(a, arguments.length < 3 ? [f] : [f, i]);
    };
  }


  // Turn camelSpace strings into Camel Space strings
  can.spaceCamelCase = function (string) {
    return can.underscore(string)
      .split("_")
      .map(can.capitalize)
      .join(" ");
  };
  can.camelCaseToUnderscore = function (string) {
    return string.replace(/([A-Z])/g, "_$1").toLowerCase();
  };
})(jQuery, can);
