/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $, utils) {
  GGRC.Components('csvImportWidget', {
    tag: "csv-import",
    template: "<content></content>",
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
                text: 'Choose file to import'
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
          return utils.Controllers.hasWarningType({type: item.name});
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
          'import': null
        });
        element.find(".csv-upload").val("");
      },
      requestImport: function (file) {
        var formData = new FormData();
        this.attr('state', 'analyzing');
        this.attr('isLoading', true);
        this.attr('filename', file.name);
        formData.append('id', file.id);

        this.requestData = {
          type: 'POST',
          url: this.attr('importUrl'),
          data: formData,
          cache: false,
          contentType: false,
          processData: false,
          headers: {
            'Content-Type': 'application/json',
            'X-test-only': 'true',
            'X-requested-by': 'GGRC'
          }
        };
        $.ajax(this.requestData)
          .then(this.prepareDataForCheck.bind(this))
          .then(function (checkObject) {
            this.beforeProcess(
              checkObject.check,
              checkObject.data,
              this.element
            );
          }.bind(this))
          .fail(function (data) {
            this.attr('state', 'select');
            GGRC.Errors.notifier('error', data.responseJSON.message);
          }.bind(this))
          .always(function () {
            this.attr('isLoading', false);
          }.bind(this));
      }
    },
    events: {
      ".state-reset click": function (el, ev) {
        ev.preventDefault();
        this.scope.resetFile(this.element);
      },
      ".state-import click": function (el, ev) {
        ev.preventDefault();
        this.scope.attr('state', 'importing');
        this.scope.requestData.headers['X-test-only'] = 'false';

        $.ajax(this.scope.requestData)
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
      'a.state-select[data-toggle=gdrive-picker] click': function (el, ev) {
        var that = this;
        var allowedTypes = ['text/csv', 'application/vnd.google-apps.document',
          'application/vnd.google-apps.spreadsheet'];
        var dfd = GGRC.Controllers
          .GAPI.authorize(['https://www.googleapis.com/auth/drive']);

        dfd.done(function () {
          gapi.load('picker', {
            callback: createPicker
          });
        });

        // Create and render a Picker object for searching images.
        function createPicker() {
          window.oauth_dfd.done(function (token, oauth_user) {
            var dialog;
            var docsUploadView;
            var docsView;
            var picker = new google.picker.PickerBuilder()
                  .setOAuthToken(gapi.auth.getToken().access_token)
                  .setDeveloperKey(GGRC.config.GAPI_KEY)
                  .setCallback(pickerCallback);

            docsUploadView = new google.picker.DocsUploadView();
            docsView = new google.picker.DocsView()
              .setMimeTypes(allowedTypes);

            picker.addView(docsUploadView)
              .addView(docsView);

            picker = picker.build();
            picker.setVisible(true);
            // use undocumented fu to make the Picker be "modal"
            // this is the "mask" displayed behind the dialog box div
            $('div.picker-dialog-bg').css('zIndex', 4000);  // there are multiple divs of that sort
            // and this is the dialog box modal div, which we must display on top of our modal, if any

            dialog = GGRC.Utils.getPickerElement(picker);
            if (dialog) {
              dialog.style.zIndex = 4001; // our modals start with 2050
            }
          });
        }

        function pickerCallback(data) {
          var file;
          var model;
          var PICKED = google.picker.Action.PICKED;
          var ACTION = google.picker.Response.ACTION;
          var DOCUMENTS = google.picker.Response.DOCUMENTS;

          if (data[ACTION] === PICKED) {
            model = CMS.Models.GDriveFile;
            file = model.models(data[DOCUMENTS])[0];

            if (file && _.any(allowedTypes, function (type) {
              return type === file.mimeType;
            })) {
              that.scope.requestImport(file);
            } else {
              GGRC.Errors.notifier('error',
                'Something other than a csv-file was chosen. ' +
                'Please choose a csv-file.');
            }
          }
        }
      }
    }
  });
})(window.can, window.can.$, GGRC.Utils);
