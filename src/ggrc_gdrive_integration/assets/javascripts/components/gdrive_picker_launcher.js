/*
 * Copyright (C) 2016 Google Inc.
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $) {
  'use strict';

  GGRC.Components('gDrivePickerLauncher', {
    tag: 'ggrc-gdrive-picker-launcher',
    template: can.view(GGRC.mustache_path + '/gdrive/gdrive_file.mustache'),
    scope: {
      instance: null,
      folder_instance: null,
      deferred: '@',
      icon: '@',
      link_text: '@',
      link_class: '@',
      click_event: '@',
      verify_event: '@',
      modal_description: '@',
      modal_title: '@',
      modal_button: '@',
      trigger_upload: function (scope, el, ev) {
        // upload files without a parent folder (risk assesment)
        var that = this;
        var verify_dfd = $.Deferred();
        var folder_id = el.data('folder-id');
        var dfd;

        // Create and render a Picker object for searching images.
        function createPicker() {
          window.oauth_dfd.done(function (token, oauth_user) {
            var dialog;
            var view;
            var docsView;
            var docsUploadView;
            var picker = new google.picker.PickerBuilder()
                    .setOAuthToken(gapi.auth.getToken().access_token)
                    .setDeveloperKey(GGRC.config.GAPI_KEY)
                    .setCallback(pickerCallback);

            if (el.data('type') === 'folders') {
              view = new google.picker.DocsView(google.picker.ViewId.FOLDERS)
                  .setIncludeFolders(true)
                  .setSelectFolderEnabled(true);
              picker.addView(view);
            } else {
              docsUploadView = new google.picker.DocsUploadView()
                .setParent(folder_id);
              docsView = new google.picker.DocsView()
                .setParent(folder_id);

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
            that.attr('pending', true);
            return new RefreshQueue().enqueue(files).trigger().then(function (files) {
              var doc_dfds = that.handle_file_upload(files);
              $.when.apply($, doc_dfds).then(function () {
                // Trigger modal:success event on scope
                can.trigger(that, 'modal:success', {arr: can.makeArray(arguments)});
                el.trigger('modal:success', {arr: can.makeArray(arguments)});
                that.attr('pending', false);
              });
            });
          } else if (data[ACTION] === CANCEL) {
            // TODO: hadle canceled uplads
            el.trigger('rejected');
          }
        }

        if (scope.attr('verify_event')) {
          GGRC.Controllers.Modals.confirm({
            modal_description: scope.attr('modal_description'),
            modal_confirm: scope.attr('modal_button'),
            modal_title: scope.attr('modal_title'),
            button_view: GGRC.mustache_path + '/gdrive/confirm_buttons.mustache'
          }, verify_dfd.resolve);
        } else {
          verify_dfd.resolve();
        }

        verify_dfd.done(function () {
          dfd = GGRC.Controllers.GAPI.authorize(['https://www.googleapis.com/auth/drive.file']);
          dfd.then(function () {
            gapi.load('picker', {callback: createPicker});
          });
        });
      },

      trigger_upload_parent: function (scope, el, ev) {
        // upload files with a parent folder (audits and workflows)
        var that = this;
        var verify_dfd = $.Deferred();
        var parent_folder_dfd;
        var folder_instance;

        folder_instance = this.folder_instance || this.instance;
        function is_own_folder(mapping, instance) {
          if (mapping.binding.instance !== instance) {
            return false;
          }
          if (!mapping.mappings ||
              mapping.mappings.length < 1 ||
              mapping.instance === true) {
            return true;
          }
          return can.reduce(mapping.mappings, function (current, mp) {
            return current || is_own_folder(mp, instance);
          }, false);
        }

        if (scope.attr('verify_event')) {
          GGRC.Controllers.Modals.confirm({
            modal_description: scope.attr('modal_description'),
            modal_confirm: scope.attr('modal_button'),
            modal_title: scope.attr('modal_title'),
            button_view: GGRC.mustache_path + '/gdrive/confirm_buttons.mustache'
          }, verify_dfd.resolve);
        } else {
          verify_dfd.resolve();
        }

        verify_dfd.done(function () {
          if (that.instance.attr('_transient.folder')) {
            parent_folder_dfd = $.when([{instance: folder_instance.attr('_transient.folder')}]);
          } else {
            parent_folder_dfd = folder_instance.get_binding('extended_folders').refresh_instances();
          }
          can.Control.prototype.bindXHRToButton(parent_folder_dfd, el);

          parent_folder_dfd.done(function (bindings) {
            var parent_folder;
            if (bindings.length < 1 || !bindings[0].instance.selfLink) {
              // no ObjectFolder or cannot access folder from GAPI
              el.trigger('ajax:flash', {
                warning: 'Can\'t upload: No GDrive folder found'
              });
              return;
            }

            parent_folder = can.map(bindings, function (binding) {
              return can.reduce(binding.mappings, function (current, mp) {
                return current || is_own_folder(mp, that.instance);
              }, false) ? binding.instance : undefined;
            });
            parent_folder = parent_folder[0] || bindings[0].instance;

            // NB: resources returned from uploadFiles() do not match the properties expected from getting
            // files from GAPI -- "name" <=> "title", "url" <=> "alternateLink".  Of greater annoyance is
            // the "url" field from the picker differs from the "alternateLink" field value from GAPI: the
            // URL has a query parameter difference, "usp=drive_web" vs "usp=drivesdk".  For consistency,
            // when getting file references back from Picker, always put them in a RefreshQueue before
            // using their properties. --BM 11/19/2013
            parent_folder.uploadFiles().then(function (files) {
              that.attr('pending', true);
              return new RefreshQueue().enqueue(files).trigger().then(function (fs) {
                return $.when.apply($, can.map(fs, function (f) {
                  if (!~can.inArray(parent_folder.id, can.map(f.parents, function (p) {
                    return p.id;
                  }))) {
                    return f.copyToParent(parent_folder);
                  }
                  return f;
                }));
              });
            }).done(function () {
              var files = can.map(can.makeArray(arguments), function (file) {
                return CMS.Models.GDriveFile.model(file);
              });
              var doc_dfds = that.handle_file_upload(files);

              $.when.apply($, doc_dfds).then(function () {
                can.trigger(that, 'modal:success', {arr: can.makeArray(arguments)});
                el.trigger('modal:success', {arr: can.makeArray(arguments)});
                that.attr('pending', false);
              });
            });
          });
        });
      },

      handle_file_upload: function (files) {
        var that = this;
        var doc_dfds = [];
        var dfd;

        can.each(files, function (file) {
          // Since we can re-use existing file references from the picker, check for that case.
          dfd = CMS.Models.Document.findAll({
            link: file.alternateLink})
          .then(function (d) {
            var doc_dfd;
            var object_doc;

            if (d.length < 1) {
              d.push(new CMS.Models.Document({
                context: that.instance.context || {id: null},
                title: file.title,
                link: file.alternateLink
              }));
            }
            if (that.deferred || !d[0].isNew()) {
              doc_dfd = $.when(d[0]);
            } else {
              doc_dfd = d[0].save();
            }

            doc_dfd = doc_dfd.then(function (doc) {
              if (that.deferred) {
                that.instance.mark_for_addition('documents', doc, {
                  context: that.instance.context || {id: null}
                });
              } else {
                object_doc = new CMS.Models.ObjectDocument({
                  context: that.instance.context || {id: null},
                  documentable: that.instance,
                  document: doc
                }).save();
              }

              return $.when(
                CMS.Models.ObjectFile.findAll({
                  file_id: file.id, fileable_id: d[0].id
                }),
                object_doc
              ).then(function (ofs) {
                if (ofs.length < 1) {
                  if (that.deferred) {
                    doc.mark_for_addition('files', file, {
                      context: that.instance.context || {id: null}
                    });
                  } else {
                    return new CMS.Models.ObjectFile({
                      context: that.instance.context || {id: null},
                      file: file,
                      fileable: doc
                    }).save();
                  }
                }})
              .then(function () {
                return doc;
              });
            });
            return doc_dfd;
          });
          doc_dfds.push(dfd);
        });
        return doc_dfds;
      }
    },
    events: {
      init: function () {
        if (!this.scope.link_class) {
          this.scope.attr('link_class', 'btn');
        }
      },
      '{scope} modal:success': function (_scope, _event) {
        var instance = this.scope.instance.reify();
        instance.refresh();
      }
    }
  });
})(this.can, this.can.$);
