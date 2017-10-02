/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import '../../plugins/utils/controllers';
import '../../plugins/utils/modals';
import './csv-template';
import '../show-more/show-more';
import template from './templates/csv-import.mustache';

export default GGRC.Components('csvImportWidget', {
  tag: "csv-import",
  template: template,
  requestData: null,
  scope: {
    importUrl: "/_service/import_csv",
    import: null,
    filename: "",
    isLoading: false,
    state: "select",
    states: function () {
      var state = this.attr("state") || "select",
          states = {
            select: {
              'class': "btn-green",
              text: "Choose CSV file to import"
            },
            analyzing: {
              'class': "btn-white",
              showSpinner: true,
              isDisabled: true,
              text: "Analyzing"
            },
            import: {
              'class': "btn-green",
              text: "Import",
              isDisabled: function () {
                var toImport = this.import;  // info on blocks to import
                var nonEmptyBlockExists;
                var hasErrors;

                if (!toImport || toImport.length < 1) {
                  return true;
                }

                // A non-empty block is a block containing at least one
                // line that is not ignored (due to errors, etc.).
                nonEmptyBlockExists = _.any(toImport, function (block) {
                  return block.rows > block.ignored;
                });

                hasErrors = _.any(toImport, function (block) {
                  return block.block_errors.length;
                });

                return hasErrors || !nonEmptyBlockExists;
              }.bind(this)  // bind the scope object as context
            },
            importing: {
              'class': "btn-white",
              showSpinner: true,
              isDisabled: true,
              text: "Importing"
            },
            success: {
              'class': "btn-green",
              isDisabled: true,
              text: "<i class=\"fa fa-check-square-o white\">"+
                "</i> Import successful"
            }
          };

      return _.extend(states[state], {state: state});
    },
    prepareDataForCheck: function (requestData) {
      var checkResult = {
        hasDeprecations: false,
        hasDeletions: false
      };

      // check if imported data has deprecated or deleted objects
      _.each(requestData, function (element) {
        if (
          checkResult.hasDeprecations &&
          checkResult.hasDeletions
        ) {
          return false;
        }

        if (!checkResult.hasDeletions) {
          checkResult.hasDeletions = (element.deleted > 0);
        }

        if (!checkResult.hasDeprecations) {
          checkResult.hasDeprecations = (element.deprecated > 0);
        }
      });

      return {
        data: requestData,
        check: checkResult
      };
    },
    processLoadedInfo: function (data) {
      this.attr("import", _.map(data, function (element) {
        element.data = [];
        if (element.block_errors.concat(element.row_errors).length) {
          element.data.push({
            status: "errors",
            messages: element.block_errors.concat(element.row_errors)
          });
        }
        if (element.block_warnings.concat(element.row_warnings).length) {
          element.data.push({
            status: "warnings",
            messages: element.block_warnings.concat(element.row_warnings)
          });
        }
        return element;
      }));
      this.attr("state", "import");
    },
    needWarning: function (checkObj, data) {
      var hasWarningTypes = _.every(data, function (item) {
        return GGRC.Utils.Controllers.hasWarningType({type: item.name});
      });
      return hasWarningTypes &&
        (
          checkObj.hasDeletions ||
          checkObj.hasDeprecations
        );
    },
    beforeProcess: function (check, data, element) {
      var operation;
      var needWarning = this.needWarning(check, data);

      if (needWarning) {
        operation = this.getOperationNameFromCheckObj(check);

        GGRC.Utils.Modals.warning(
          {
            objectShortInfo: 'imported object(s)',
            modal_description:
              'In the result of import some Products, Systems or ' +
              'Processes will be ' + operation.past + '.',
            operation: operation.action
          },
          function () {
            this.processLoadedInfo(data);
          }.bind(this),
          function () {
            this.attr('state', 'import');
            this.resetFile(element);
          }.bind(this)
        );
        return;
      }

      this.processLoadedInfo(data);
    },
    getOperationNameFromCheckObj: function (checkObj) {
      var action = _.compact([
        checkObj.hasDeletions ? 'deletion' : '',
        checkObj.hasDeprecations ? 'deprecation' : ''
      ]).join(' and ');
      var pastForm = _.compact([
        checkObj.hasDeletions ? 'deleted' : '',
        checkObj.hasDeprecations ? 'deprecated' : ''
      ]).join(' and ');

      return {
        action: action,
        past: pastForm
      };
    },
    resetFile: function (element) {
      this.attr({
        state: "select",
        filename: "",
        import: null
      });
      element.find(".csv-upload").val("");
    }
  },
  events: {
    ".state-reset click": function (el, ev) {
      ev.preventDefault();
      this.scope.resetFile(this.element);
    },
    ".state-select click": function (el, ev) {
      ev.preventDefault();
      this.element.find(".csv-upload").trigger("click");
    },
    ".state-import click": function (el, ev) {
      ev.preventDefault();
      this.scope.attr("state", "importing");
      this.requestData.headers["X-test-only"] = "false";

      $.ajax(this.requestData)
      .done(function (data) {
        var result_count = data.reduce(function (prev, curr) {
              _.each(Object.keys(prev), function(key) {
                prev[key] += curr[key] || 0;
              });
              return prev;
            }, {created: 0, updated: 0, deleted: 0, ignored: 0});

        this.scope.attr("state", "success");
        this.scope.attr("data", [result_count]);
      }.bind(this))
      .fail(function (data) {
        this.scope.attr("state", "select");
        GGRC.Errors.notifier('error', data.responseJSON.message);
      }.bind(this))
      .always(function () {
        this.scope.attr("isLoading", false);
      }.bind(this));
    },
    ".csv-upload change": function (el, ev) {
      var file = el[0].files[0],
          formData = new FormData();

      this.scope.attr("state", "analyzing");
      this.scope.attr("isLoading", true);
      this.scope.attr("filename", file.name);
      formData.append("file", file);

      this.requestData = {
        type: "POST",
        url: this.scope.attr("importUrl"),
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        headers: {
          "X-test-only": "true",
          "X-requested-by": "GGRC"
        }
      };
      $.ajax(this.requestData)
        .then(this.scope.prepareDataForCheck.bind(this.scope))
        .then(function (checkObject) {
          this.scope.beforeProcess(
            checkObject.check,
            checkObject.data,
            this.element
          );
        }.bind(this))
        .fail(function (data) {
          this.scope.attr("state", "select");
          GGRC.Errors.notifier('error', data.responseJSON.message);
        }.bind(this))
        .always(function () {
          this.scope.attr("isLoading", false);
        }.bind(this));
    }
  }
});
