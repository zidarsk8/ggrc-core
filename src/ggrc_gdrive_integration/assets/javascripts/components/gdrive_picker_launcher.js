/*
 * Copyright (C) 2017 Google Inc.
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../utils/gdrive-picker-utils.js';
import errorTpl from './templates/gdrive_picker_launcher_upload_error.mustache';

(function (can, $, GGRC, CMS) {
  'use strict';

  GGRC.Components('gDrivePickerLauncher', {
    tag: 'ggrc-gdrive-picker-launcher',
    template: can.view(GGRC.mustache_path + '/gdrive/gdrive_file.mustache'),
    viewModel: {
      define: {
        isInactive: {
          get: function () {
            return this.attr('disabled');
          }
        }
      },
      assessmentTypeObjects: [],
      instance: {},
      deferred: '@',
      link_class: '@',
      click_event: '@',
      itemsUploadedCallback: '@',
      confirmationCallback: '@',
      pickerActive: false,
      disabled: false,
      sanitizeSlug: function (slug) {
        return slug.toLowerCase().replace(/\W+/g, '-');
      },
      removeOldSuffix: function (fileName) {
        var delPos = fileName.lastIndexOf('_ggrc_');
        return delPos > 0 ? fileName.substring(0, delPos) : fileName;
      },
      addFileSuffix: function (fileName) {
        var assesmentSlug =
          this.sanitizeSlug(this.attr('instance').attr('slug'));
        var suffixArr = ['ggrc', assesmentSlug];

        suffixArr = suffixArr.concat(
          this.attr('assessmentTypeObjects').map(function (obj) {
            return this.sanitizeSlug(obj.attr('revision.content.slug'));
          }.bind(this)).attr()
        );

        return fileName.match(/\.(\w+)$/) ?
          // file name with extension
          fileName.replace(/^(.*)\.(\w+)$/, (match, name, fileExt) => {
              return this.removeOldSuffix(name) + '_' + suffixArr.join('_') +
                      '.' + fileExt;
          }) :
          // file name without extension
          this.removeOldSuffix(fileName) + '_' + suffixArr.join('_');
      },
      /**
       * Copys or renames files adding new suffixes to the file names
       * @param  {Object} [opts={}] Options object.
       * @param  {Array}  files     Array of files models
       * @return {Promise}          Promise which resolves to array of new files
       */
      addFilesSuffixes: function (opts = {}, files) {
        var fileRenameBatch = gapi.client.newBatch();
        var fileRenameDfd = can.Deferred();
        var errors = [];
        var originalFileNames = {};
        var newParentId = opts.dest && opts.dest.id;

        files.forEach((file) => {
          var req;
          var requestBody = {};

          // TODO: maybe pick the one format (the one that comes after refresh)?
          var originalFileName = file.attr('title') ||
            file.attr('originalFilename') || file.attr('name');

          var newFileName = this.addFileSuffix(originalFileName);

          var parents = (file.parents && file.parents.attr()) || [];
          var existsInParent = Boolean(
            parents.find((parent) => parent.id === newParentId)
          );

          // We change the file if it's a new upload
          // or file with the same name already exists in the directory
          var changeExistingFile = file.newUpload ||
            (existsInParent && originalFileName === newFileName);

          var reqPath = changeExistingFile ? `/drive/v3/files/${file.id}`
            : `/drive/v3/files/${file.id}/copy`;
          var reqMethod = changeExistingFile ? 'PATCH' : 'POST';

          file.attr('title', newFileName);
          file.attr('name', newFileName);
          originalFileNames[file.id] = originalFileName;

          requestBody.name = newFileName;

          // If there're no such file in the destination directory
          // we'll move or copy it there
          if ( newParentId && !existsInParent ) {
            requestBody.parents = [newParentId];
          }

          // updating filenames on GDrive
          req = gapi.client.request({
            path: reqPath,
            method: reqMethod,
            params: {
              alt: 'json',
            },
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
          });

          fileRenameBatch.add(req, {
            id: file.id, // settings request id to file id to find the failed file later
          });
        });

        // Batch promise always resolves even when some of requests failed
        // so we manually parsing the response object to find errors
        fileRenameBatch.then((batchRes) => {
          var newFiles = [];
          can.each(batchRes.result, function (response, fileId) {
            if ( response.status === 200 ) {
              newFiles.push(response.result);
            } else {
              errors.push({
                fileName: originalFileNames[fileId],
              });
              console.error(
                `File ${originalFileNames[fileId]} failed to be renamed.`,
                response.result.error
              );
            }
          });

          if ( newFiles.length ) {
            // if we have successfully renamed files, showing errors just for
            // the failed ones
            if ( errors.length ) {
              GGRC.Errors.notifier('error', errorTpl, {
                errors: errors,
              });
            }

            this.refreshFilesModel(CMS.Models.GDriveFile.models(newFiles))
              .then(fileRenameDfd.resolve, fileRenameDfd.reject);
          } else {
            fileRenameDfd.reject(new Error(
                `Failed to attach uploaded files.
                An error occurred while adding suffixes.`));
          }
        });

        return fileRenameDfd;
      },
      beforeCreateHandler: function (files) {
        var tempFiles = files.map(function (file) {
          return {
            title: this.addFileSuffix(file.name),
            link: file.url,
            created_at: new Date(),
            isDraft: true
          };
        }.bind(this));
        this.dispatch({
          type: 'onBeforeAttach',
          items: tempFiles
        });
        return files;
      },
      onClickHandler: function (scope, el, event) {
        var eventType = this.attr('click_event');
        var handler = this[eventType] || function () {};
        var confirmation = can.isFunction(this.confirmationCallback) ?
          this.confirmationCallback() :
          null;
        var args = arguments;
        var that = this;

        event.preventDefault();
        can.when(confirmation).then(function () {
          handler.apply(that, args);
        });
      },
      trigger_upload: function (scope, el) {
        // upload files without a parent folder (risk assesment)
        var that = this;
        var dfd;
        var picker;
        var folderId = el.data('folder-id');

        // Create and render a Picker object for searching images.
        function createPicker() {
          GGRC.Controllers.GAPI.oauth_dfd
            .done(function () {
              var dialog;
              var view;
              var docsView;
              var docsUploadView;

              picker = new google.picker.PickerBuilder()
                .setOAuthToken(gapi.auth.getToken().access_token)
                .setDeveloperKey(GGRC.config.GAPI_KEY)
                .setMaxItems(10)
                .setCallback(pickerCallback);

              if (el.data('type') === 'folders') {
                view = new google.picker.DocsView(google.picker.ViewId.FOLDERS)
                  .setIncludeFolders(true)
                  .setSelectFolderEnabled(true);
                picker.addView(view);
              } else {
                docsUploadView = new google.picker.DocsUploadView()
                  .setParent(folderId);
                docsView = new google.picker.DocsView()
                  .setParent(folderId);

                picker.addView(docsUploadView)
                  .addView(docsView)
                  .enableFeature(google.picker.Feature.MULTISELECT_ENABLED);
              }
              picker = picker.build();
              picker.setVisible(true);

              dialog = GGRC.Utils.getPickerElement(picker);
              if (dialog) {
                dialog.style.zIndex = 4001; // our modals start with 2050
              }
            });
        }

        function pickerCallback(data) {
          var files;
          var PICKED = google.picker.Action.PICKED;
          var ACTION = google.picker.Response.ACTION;
          var DOCUMENTS = google.picker.Response.DOCUMENTS;
          var CANCEL = google.picker.Action.CANCEL;

          if (data[ACTION] === PICKED) {
            files = CMS.Models.GDriveFile.models(data[DOCUMENTS]);
            scope.attr('pickerActive', false);
            that.beforeCreateHandler(files);

            that.refreshFilesModel(files)
              .then(that.addFilesSuffixes.bind(that, {}))
              .then(function (files) {
                that.handle_file_upload(files).then(function (docs) {
                  // Trigger modal:success event on scope
                  can.trigger(that, 'modal:success', {arr: docs});
                  el.trigger('modal:success', {arr: docs});
                });
              })
              .fail(function (error) {
                that.dispatch({
                  type: 'resetItems',
                });
                if ( error ) {
                  GGRC.Errors.notifier('error', error && error.message);
                }
              });
          } else if (data[ACTION] === CANCEL) {
            el.trigger('rejected');
          }

          GGRC.Utils.GDrivePicker.ensurePickerDisposed(picker, data);
        }

        dfd = GGRC.Controllers.GAPI.reAuthorize(gapi.auth.getToken());
        dfd.done(function () {
          gapi.load('picker', {callback: createPicker});
        });
      },

      refreshFilesModel: function (files) {
        return new RefreshQueue().enqueue(files).trigger();
      },

      trigger_upload_parent: function (scope, el) {
        // upload files with a parent folder (audits and workflows)
        var that = this;
        var parentFolderDfd;
        var folderInstance = this.folder_instance || this.instance;

        function isOwnFolder(mapping, instance) {
          if (mapping.binding.instance !== instance) {
            return false;
          }
          if (!mapping.mappings ||
            mapping.mappings.length < 1 ||
            mapping.instance === true) {
            return true;
          }
          return can.reduce(mapping.mappings, function (current, mp) {
            return current || isOwnFolder(mp, instance);
          }, false);
        }

        if (that.instance.attr('_transient.folder')) {
          parentFolderDfd = can.when(
            [{instance: folderInstance.attr('_transient.folder')}]
          );
        } else {
          parentFolderDfd = folderInstance
            .get_binding('extended_folders')
            .refresh_instances();
        }
        can.Control.prototype.bindXHRToButton(parentFolderDfd, el);

        parentFolderDfd
          .done(function (bindings) {
            var parentFolder;
            if (bindings.length < 1 || !bindings[0].instance.selfLink) {
              // no ObjectFolder or cannot access folder from GAPI
              el.trigger('ajax:flash', {
                warning: 'Can\'t upload: No GDrive folder found'
              });
              return;
            }

            parentFolder = can.map(bindings, function (binding) {
              return can.reduce(binding.mappings, function (current, mp) {
                return current || isOwnFolder(mp, that.instance);
              }, false) ? binding.instance : undefined;
            });
            parentFolder = parentFolder[0] || bindings[0].instance;

            // NB: resources returned from uploadFiles() do not match the
            // properties expected from getting files from GAPI --
            // "name" <=> "title", "url" <=> "alternateLink". Of greater
            // annoyance is the "url" field from the picker differs from the
            // "alternateLink" field value from GAPI: the URL has a query
            // parameter difference, "usp=drive_web" vs "usp=drivesdk". For
            // consistency, when getting file references back from Picker,
            // always put them in a RefreshQueue before using their properties.
            // --BM 11/19/2013
            parentFolder.uploadFiles()
              .then(that.refreshFilesModel.bind(that))
              .then(that.beforeCreateHandler.bind(that))
              .then(that.addFilesSuffixes.bind(that, {dest: parentFolder}))
              .then(function (files) {
                that.handle_file_upload(files).then(function (docs) {
                  can.trigger(that, 'modal:success', {arr: docs});
                  el.trigger('modal:success', {arr: docs});
                });
              })
              .fail(function () {
                // This case happens when user have no access to write in audit folder
                var error = _.last(arguments);
                if (error && error.code === 403) {
                  GGRC.Errors.notifier('error', GGRC.Errors.messages[403]);

                  can.trigger(that, 'modal:success');
                  el.trigger('modal:success');
                } else if ( error ) {
                  that.dispatch({
                    type: 'resetItems'
                  });

                  GGRC.Errors.notifier('error', error && error.message);
                }
              });
          });
      },

      handle_file_upload: function (files) {
        var that = this;

        var dfdDocs = files.map(function (file) {
          return new CMS.Models.Document({
            context: that.instance.context || {id: null},
            title: file.title,
            link: file.alternateLink
          }).save().then(function (doc) {
            var objectDoc;

            if (that.deferred) {
              that.instance.mark_for_addition('documents', doc, {
                context: that.instance.context || {id: null}
              });
            } else {
              objectDoc = new CMS.Models.Relationship({
                context: that.instance.context || {id: null},
                source: that.instance,
                destination: doc
              }).save();
            }

            return objectDoc;
          });
        });
        // waiting for all docs promises
        return can.when.apply(can, dfdDocs).then(function () {
          return can.makeArray(arguments);
        });
      }
    },
    events: {
      '{viewModel} modal:success': function () {
        var instance = this.viewModel.instance;
        var itemsUploadedCallback = this.viewModel.itemsUploadedCallback;

        if (can.isFunction(itemsUploadedCallback)) {
          itemsUploadedCallback();
        } else {
          instance.reify();
          instance.refresh();
        }
      },
      '{viewModel} resetItems': function () {
        var itemsUploadedCallback = this.viewModel.itemsUploadedCallback;

        if (can.isFunction(itemsUploadedCallback)) {
          itemsUploadedCallback();
        }
      }
    }
  });
})(window.can, window.can.$, window.GGRC, window.CMS);
