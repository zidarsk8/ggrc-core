/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: swizec@reciprocitylabs.com
    Maintained By: swizec@reciprocitylabs.com
*/

can.Component.extend({
  tag: "assessment-generator-button",
  template: "{{{> /static/mustache/base_objects/generate_assessments_button.mustache}}}",
  scope: {
    audit: null
  },
  events: {
    'a click': function() {
      if (this.scope.loading) {
        return;
      }
      this._generate_control_assessments();
    },

    _generate_control_assessments: function(controls) {
      var assessments_list = this.scope.audit.get_binding("related_control_assessments").list,
          controls_list = this.scope.audit.get_binding("program_controls").list,
          assessments_dfd = this._refresh(assessments_list),
          controls_dfd = this._refresh(controls_list),
          ignore_controls, dfd;

      dfd = $.when(assessments_dfd, controls_dfd).then(function (assessments, controls) {
        ignore_controls = _.map(assessments, function(ca) {
          return ca.control.id;
        });
        return $.when.apply($, can.map(controls, function(control) {
          if (_.includes(ignore_controls, control.id)) {
            return;
          }
          return this._generate(control);
        }.bind(this)));
      }.bind(this));
      this._enter_loading_state(dfd);
      dfd.always(this._notify.bind(this));
    },

    _refresh: function (bindings) {
      var refresh_queue = new RefreshQueue();
      can.each(bindings, function(binding) {
          refresh_queue.enqueue(binding.instance);
      });
      return refresh_queue.trigger();
    },

    _generate: function(control, count, dfd) {
      count = count || 0;
      dfd = dfd || new $.Deferred();

      var assessment = new CMS.Models.ControlAssessment({
          audit: this.scope.audit,
          control: control.stub(),
          context: this.scope.audit.context,
          title: control.title + " assessment" + (count ? " " + count : ""),
          test_plan: control.test_plan
      });
      assessment.save().done(function () {
        dfd.resolve(assessment);
      }).fail(function (error, type, code) {
        if (code === "FORBIDDEN"
          && error.responseText.match(/(title values must be unique)|(Duplicate entry)/)) {
          this._generate(control, count + 1, dfd);
        } else {
          return dfd.reject(error);
        }
      }.bind(this));
      return dfd;
    },

    _notify: function() {
      this._exit_loading_state();

      var assessments = arguments,
        count = _.filter(assessments, function(assessment) {
          return  !_.isNull(assessment) && !(assessment.state && assessment.state() === "rejected");
        }).length,
        errors = _.filter(assessments, function(assessment) {
          return assessment.state && assessment.state() === "rejected";
        }).length,
        msg;

      if (errors < 1) {
        if (count === 0) {
          msg = {
            success: "Every Control already has a Control Assessment!"
          };
        } else {
          msg = {
            success: "<span class='user-string'>" + count + "</span> Control Assessments successfully created."
          };
        }
      } else {
        msg = {
          error: "An error occured when creating Control Assessments."
        };
      }

      $(document.body).trigger("ajax:flash", msg);
    },

    _enter_loading_state: function (deferred) {
      var $i = this.element.find("a > i"),
          icon = $i.attr("class");

      $i.attr("class", "grcicon-loading");
      $(document.body).trigger("ajax:flash",
                               {warning: "Generating Control Assessments"});

      this.scope.icon = icon;
      this.scope.loading = true;
      GGRC.delay_leaving_page_until(deferred);
    },

    _exit_loading_state: function () {
      this.element.find("a > i")
            .attr("class", this.scope.icon);

      this.scope.loading = false;
    }
  }
});
