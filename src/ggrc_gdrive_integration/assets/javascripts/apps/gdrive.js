/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: Bradley Momberger
 * Maintained By: Bradley Momberger
 */

(function($, CMS, GGRC) {

  $.extend(true, CMS.Models.Program.attributes, {
    "object_folders" : "CMS.Models.ObjectFolder.stubs"
  });
  GGRC.Mappings.Program.object_folders = new GGRC.ListLoaders.DirectListLoader("ObjectFolder", "folderable");

  $.extend(true, CMS.Models.Audit.attributes, {
    "object_folders" : "CMS.Models.ObjectFolder.stubs"
  });
  can.getObject("GGRC.Mappings.Audit", true).object_folders = new GGRC.ListLoaders.DirectListLoader("ObjectFolder", "folderable");

  $.extend(true, CMS.Models.Request.attributes, {
    "object_folders" : "CMS.Models.ObjectFolder.stubs"
  });
  can.getObject("GGRC.Mappings.Request", true).object_folders = new GGRC.ListLoaders.DirectListLoader("ObjectFolder", "folderable");

  $.extend(true, CMS.Models.Response.attributes, {
    "object_files" : "CMS.Models.ObjectFile.stubs"
  });
  can.getObject("GGRC.Mappings.Response", true).object_files = new GGRC.ListLoaders.DirectListLoader("ObjectFile", "fileable");

  // GGRC.JoinDescriptor.from_arguments_list([
  //   [["Program", "Audit", "Request"], "GDriveFolder", "ObjectFolder", "folder", "folderable"]
  //   , ["Response", "GDriveFile", "ObjectFile", "file", "fileable"]
  // ]);


})(this.can.$, this.CMS, this.GGRC);