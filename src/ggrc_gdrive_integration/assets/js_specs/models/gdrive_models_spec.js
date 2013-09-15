if(!window.GGRC) {
  window.GGRC = {};
}
if(!GGRC.config) {
  GGRC.config = {};
}
GGRC.config.GDRIVE_ROOT_FOLDER = '0ByeYJ052BwIZb2hoTWtjcDV2dTg';
GGRC.config.GDRIVE_SCRIPT_ID = 'AKfycbxb-W3rUBTKFF6Ua_eJ5PH9RAvGVL7W3aDqtmnbnUc7PD0FY3zo';

describe("GDrive integration models", function() {

  describe("GGRC.Models.GDriveFolder", function() {

    describe("::findAll", function() {

      it("takes a parent folder id as a required parameter", function() {
        var returned;
        function ajaxtoreturn() { return returned; }
        GGRC.Models.GDriveFolder.findAll({parentfolderid : '0ByeYJ052BwIZb2hoTWtjcDV2dTg'}).done(function(d) {
          expect(d.length).toBeGreaterThan(0);
        }).always(function() {
          returned = true;
        });
        waitsFor(ajaxtoreturn, 5000);
      });

      it("calls the root when parentfolderid is not supplied", function() {
        var returned;
        spyOn($, 'ajax').andReturn(new $.Deferred().resolve());
        GGRC.Models.GDriveFolder.findAll();
        expect($.ajax.mostRecentCall.args[0].data.parameters).toMatch(new RegExp(GGRC.config.GDRIVE_ROOT_FOLDER));
      });
    });

    describe("::findChildFolders", function() {
      beforeEach(function() {
        spyOn(GGRC.Models.GDriveFolder, "findAll");
      });
      it("performs a findAll with a supplied string as parentfolderid", function() {
        GGRC.Models.GDriveFolder.findChildFolders("foo");
        expect(GGRC.Models.GDriveFolder.findAll).toHaveBeenCalledWith({ parentfolderid : "foo" });
      });
      it("performs a findAll with a supplied object's id as parentfolderid", function() {
        GGRC.Models.GDriveFolder.findChildFolders({id : "bar"});
        expect(GGRC.Models.GDriveFolder.findAll).toHaveBeenCalledWith({ parentfolderid : "bar" });
      });
    });
  });

});