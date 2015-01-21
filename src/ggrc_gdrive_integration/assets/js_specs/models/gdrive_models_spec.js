if(!window.GGRC) {
  window.GGRC = {};
}
if(!GGRC.config) {
  GGRC.config = {};
}
GGRC.config.GDRIVE_ROOT_FOLDER = '0ByeYJ052BwIZb2hoTWtjcDV2dTg';
GGRC.config.GDRIVE_SCRIPT_ID = 'AKfycbxb-W3rUBTKFF6Ua_eJ5PH9RAvGVL7W3aDqtmnbnUc7PD0FY3zo';


describe("working tests", function () {
    it("will have to update to jasmine 2.0 ways", function () {
    });
});


xdescribe("GDrive integration models", function() {

  beforeEach(function() {
    spyOn(GGRC.Controllers.GAPI, "authorize").andCallFake(function() {
      return $.when();
    });
  });

  describe("CMS.Models.GDriveFolder", function() {

    describe("::findAll", function() {

      it("calls the root when parentfolderid is not supplied", function() {
        var returned;
        spyOn(gapi.client, 'request').andReturn(new $.Deferred().resolve());
        CMS.Models.GDriveFolder.findAll();
        expect(gapi.client.request.mostRecentCall.args[0].path).toMatch(/\?q=.*'root'%20in%20parents/);
      });
    });

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
