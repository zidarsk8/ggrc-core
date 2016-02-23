/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: swizec@reciprocitylabs.com
    Maintained By: swizec@reciprocitylabs.com
*/

can.Component.extend({
  tag: 'assessment-generator-button',
  template: '{{{> /static/mustache/base_objects/generate_assessments_button.mustache}}}',
  scope: {
    audit: null
  },
  events: {
    'a click': function (el, ev) {
      var instance = GGRC.page_instance();
      if (this.scope.loading) {
        return;
      }
      this._results = null;
      GGRC.Controllers.MapperModal.launch(el, {
        object: 'Audit',
        type: 'Control',
        'join-object-id': this.scope.audit.id,
        'join-mapping': 'program_controls',
        getList: true,
        relevantTo: [{
          type: instance.program.type,
          id: instance.program.id
        }],
        template: {
          title: 'Select controls to generate assessments',
          submitButton: 'Generate Assessments',
          count: 'assessment(s) will be generated'
        },
        callback: this._generate_assessments.bind(this)
      });
    },
    _generate_assessments: function (list, options) {
      this._refresh(list).then(function (items) {
        var results = _.map(items, function (item) {
          return this._generate(item);
        }.bind(this));
        this._results = results;
        $.when.apply($, results)
          .then(function () {
            options.context.closeModal();
          })
          .done(this._notify.bind(this))
          .fail(this._notify.bind(this));
      }.bind(this));
    },

    _refresh: function (bindings) {
      var que = new RefreshQueue();
      return que.enqueue(bindings).trigger();
    },

    _generate: function (object) {
      var title = object.title + ' assessment for ' + this.scope.audit.title;
      var data = {
        audit: this.scope.audit,
        object: object.stub(),
        context: this.scope.audit.context,
        title: title,
        owners: [CMS.Models.Person.findInCacheById(GGRC.current_user.id)]
      };
      if (object.test_plan) {
        data.test_plan = object.test_plan;
      }
      return new CMS.Models.Assessment(data).save();
    },

    _notify: function () {
      var success;
      var errors;
      var msg;

      if (!this._results) {
        return;
      }
      success = _.filter(this._results, function (assessment) {
        return !_.isNull(assessment) &&
          !(assessment.state && assessment.state() === 'rejected');
      }).length;
      errors = _.filter(this._results, function (assessment) {
        return assessment.state && assessment.state() === 'rejected';
      }).length;

      if (errors < 1) {
        if (success === 0) {
          msg = {
            success: "Every Control already has an Assessment!"
          };
        } else {
          msg = {
            success: success + " Assessments successfully created."
          };
        }
      } else {
        msg = {
          error: "An error occured when creating Assessments."
        };
      }

      $(document.body).trigger('ajax:flash', msg);
    }
  }
});
