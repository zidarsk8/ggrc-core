/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

if(!window.GGRC) {
  window.GGRC = {};
}
if(!GGRC.config) {
  GGRC.config = {};
}
GGRC.config.GDRIVE_ROOT_FOLDER = '0ByeYJ052BwIZb2hoTWtjcDV2dTg';
GGRC.config.GDRIVE_SCRIPT_ID = 'AKfycbxb-W3rUBTKFF6Ua_eJ5PH9RAvGVL7W3aDqtmnbnUc7PD0FY3zo';

describe("GDrive integration models", function() {

  beforeEach(function() {
    spyOn(GGRC.Controllers.GAPI, "authorize").and.callFake(function() {
      return $.when();
    });
  });

  describe("CMS.Models.GDriveFolder", function() {
       //randomly fails with:

       //Chrome 39.0.2171 (Linux) GDrive integration models CMS.Models.GDriveFolder ::findAll calls the root when parentfolderid is not supplied FAILED
       // Error: spyOn could not find an object to spy upon for request()
       //       at Object.<anonymous> (/vagrant/src/ggrc_gdrive_integration/assets/js_specs/models/gdrive_models_spec.js:24:19)
       //       Chrome 39.0.2171 (Linux): Executed 129 of 146 (1 FAILED) (0.228 secs / 0.182 secs)
              
    /*
    describe("::findAll", function() {
      

      it("calls the root when parentfolderid is not supplied", function() {
        var returned;
        spyOn(gapi.client, 'request').and.returnValue(new $.Deferred().resolve());
        CMS.Models.GDriveFolder.findAll();
        expect(gapi.client.request.calls.mostRecent().args[0].path).toMatch(/\?q=.*'root'%20in%20parents/);
      });
    });
    */

    describe("::findChildFolders", function() {
      beforeEach(function() {
        spyOn(CMS.Models.GDriveFolder, "findAll");
      });
      it("performs a findAll with a supplied string as parentfolderid", function() {
        CMS.Models.GDriveFolder.findChildFolders("foo");
        expect(CMS.Models.GDriveFolder.findAll).toHaveBeenCalledWith({ parents : "foo" });
      });
      it("performs a findAll with a supplied object's id as parentfolderid", function() {
        CMS.Models.GDriveFolder.findChildFolders({id : "bar"});
        expect(CMS.Models.GDriveFolder.findAll).toHaveBeenCalledWith({ parents : "bar" });
      });
    });
  });

});
