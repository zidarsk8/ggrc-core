/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: Bradley Momberger
 * Maintained By: Bradley Momberger
 */

(function() {

  $.extend(true, CMS.Models.Program.attributes, {
    "object_folders" : "CMS.Models.ObjectFolder.stubs"
  });

  $.extend(true, CMS.Models.Audit.attributes, {
    "object_folders" : "CMS.Models.ObjectFolder.stubs"
  });
  $.extend(true, CMS.Models.Request.attributes, {
    "object_folders" : "CMS.Models.ObjectFolder.stubs"
  });
  $.extend(true, CMS.Models.Response.attributes, {
    "object_files" : "CMS.Models.ObjectFile.stubs"
  });

  GGRC.JoinDescriptor.from_arguments_list([
    [["Program", "Audit", "Request"], GGRC.Models.GDriveFolder, "ObjectFolder", "folderable", "folder_id"]
    , ["Response", GGRC.Models.GDriveFile, "ObjectFile", "fileable", "file_id"]
  ]);


})();