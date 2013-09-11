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

      it("fails when parentfolderid is not supplied", function() {
        var returned;
        function ajaxtoreturn() { return returned; }
        expect(GGRC.Models.GDriveFolder.findAll).toThrow("ERROR: parentfolderid is required for GDriveFolder.findAll");
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