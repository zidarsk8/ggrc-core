/*!
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $, CMS, GGRC) {
  var random = Date.now();
  var scopes = new can.List(['https://www.googleapis.com/auth/userinfo.email']);

  new GGRC.Mappings('ggrc_gdrive_integration', {
    revisionable: {
      _canonical: {
        revisions: "GDriveFileRevision"
      },
      revisions: new GGRC.ListLoaders.DirectListLoader("GDriveFileRevision", "id")
    },
    GDriveFolder: {
      _mixins: ["revisionable"],
      _canonical: {
        permissions: "GDriveFolderPermission"
      },
      permissions: new GGRC.ListLoaders.DirectListLoader("GDriveFolderPermission", "id")
    },
    GDriveFile: {
      _mixins: ["revisionable"],
      _canonical: {
        permissions: "GDriveFilePermission"
      },
      permissions: new GGRC.ListLoaders.DirectListLoader("GDriveFilePermission", "id")
    }
  });

  GGRC.gapi_request_with_auth =
    $.proxy(GGRC.Controllers.GAPI, 'gapi_request_with_auth');
  $(function () {
    $(document.body).ggrc_controllers_gapi({scopes: scopes});
  });

  window['resolvegapi' + random] = function (gapi) {
    GGRC.Controllers.GAPI.gapidfd.resolve(gapi);
    delete window['resolvegapi' + random];
  };
  $('head').append('<script type="text/javascript" src="https://apis.google.com/js/client.js?onload=resolvegapi' + random + '"></script>');

  can.view.mustache('picker-tag-default',
    '<ggrc-gdrive-folder-picker ' +
    '{{#if instance.archived}}' +
    'readonly=true' +
    '{{/if}}' +
    '{{^is_allowed "update" instance context="for"}}' +
    'readonly=true{{/is_allowed}}' +
    ' instance="instance"/>');
  GGRC.register_hook('Audit.tree_view_info', 'picker-tag-default');
  GGRC.register_hook('Audit.storage_folder_picker',
    GGRC.mustache_path + '/audits/gdrive_folder_picker.mustache');

  GGRC.register_hook('Role.option_detail', GGRC.mustache_path +
    '/roles/gdrive_option_detail.mustache');

  GGRC.register_hook('Workflow.storage_folder_picker',
    GGRC.mustache_path + '/workflows/gdrive_folder_picker.mustache');
})(window.can, window.can.$, window.CMS, window.GGRC);
