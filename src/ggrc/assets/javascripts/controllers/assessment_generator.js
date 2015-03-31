/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: swizec@reciprocitylabs.com
    Maintained By: swizec@reciprocitylabs.com
*/

can.Control("CMS.Controllers.AssessmentGenerator", {
  defaults: {
    audit: null
  }
}, {
  init: function (el, options) {
    typeof this._super === "function" && this._super.apply(this, [el]);

    this.audit = options.audit;
    this.options = options;
  },

  generate_control_assessments: function (controls) {
    var refresh_assessments = this._refresh_assessments();

      refresh_assessments.then(function () {
        var control_assessments = arguments,
            ignore_controls = _.map(control_assessments, function (ca) {
              return ca.control.id;
            });

        can.each(controls, function (control) {
          if (!_.includes(ignore_controls, control.instance.id)) {
            this._generate(control);
          }
        }.bind(this));
      }.bind(this));
  },

  // promise map pattern found on http://stackoverflow.com/questions/20688803/jquery-deferred-in-each-loop
  _refresh_assessments: function () {
    return $.when.apply($, can.map(this.audit.get_binding("related_control_assessments").list, function (control_assessment) {
        var def = new $.Deferred();
        control_assessment.instance.refresh().then(function (control_assessment) {
          def.resolve(control_assessment);
        });
        return def;
    })).promise();
  },

  _generate: function (control, count) {
    count = typeof count == undefined ? 0 : count;

    var assessment = new CMS.Models.ControlAssessment(
        {audit: this.audit,
         control: control.instance,
         context: this.audit.context,
         title: control.instance.title+" assessment"+(count ? " "+count : "")});

    return assessment
          .save()
          .fail(function (error, type, code) {
            if (code === "FORBIDDEN" 
                && error.responseText.match(/title values must be unique/)) {
                this.generate(control, count+1);
            }
          });
  }
});
