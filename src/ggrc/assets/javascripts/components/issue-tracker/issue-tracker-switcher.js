/*
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

const tag = 'issue-tracker-switcher';

export default GGRC.Components('issueTrackerSwitcher', {
  tag: tag,
  template: '<content/>',
  viewModel: {
    define: {
      isIntegrationEnabled: {
        set: function (newValue, setValue) {
          // convert to bool type. dropdown returns "true" or "false" as string
          let boolValue = this.convertToBool(newValue);

          if (boolValue) {
            this.setDefaults();
          }

          setValue(boolValue);
        },
      },
      defaultTitle: {
        set: function (newValue, setValue) {
          if (newValue && this.attr('canUpdateDefaultTitle')) {
            this.setDefaultIssueTitle(newValue);
          }

          setValue(newValue);
        },
      },
      isParent: {
        get: function () {
          return !this.attr('parent');
        },
      },
      isFirstTimeTurnOn: {
        get: function () {
          // 'issue_tracker' has already created if component_id is filled;
          return !!this.attr('instance.issue_tracker.component_id');
        },
      },
    },
    instance: {},
    parent: null,
    canUpdateDefaultTitle: false,
    setIssueTitle: false,
    convertToBool: function (value) {
      if (typeof value === 'boolean') {
        return value;
      }

      return !(!value || value === 'false');
    },
    setDefaults: function () {
      let issueTracker = this.attr('instance.issue_tracker');

      issueTracker.attr('issue_type',
        issueTracker.attr('issue_type') || 'PROCESS');

      if (this.attr('isParent') || this.attr('isFirstTimeTurnOn')) {
        issueTracker.attr('issue_priority',
          issueTracker.attr('issue_priority') || 'P0');
        issueTracker.attr('issue_severity',
          issueTracker.attr('issue_severity') || 'S0');
      } else {
        this.setDeaultsFromParent('issue_priority');
        this.setDeaultsFromParent('issue_severity');
        this.setDeaultsFromParent('component_id');
        this.setDeaultsFromParent('hotlist_id');

        if (this.attr('setIssueTitle')) {
          // can override issue title in case when user creates new instance
          // instance turns on issue tracker integration first time
          this.attr('canUpdateDefaultTitle', true);
          this.setDefaultIssueTitle();
        }
      }
    },
    setDeaultsFromParent: function (propName) {
      let issueTracker = this.attr('instance.issue_tracker');
      let parentIssueTracker = this.attr('parent.issue_tracker');

      issueTracker.attr(propName,
        issueTracker.attr(propName) || parentIssueTracker.attr(propName));
    },
    setDefaultIssueTitle: function (value) {
      let title = this.attr('instance.title')
      let issueTracker = this.attr('instance.issue_tracker');

      if (value) {
        issueTracker.attr('title', value);
        return;
      }

      // set from instance title
      if (title && !issueTracker.attr('title')) {
        issueTracker.attr('title', title);
      }
    },
  },
});
