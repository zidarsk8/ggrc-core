window.GGRC = window.GGRC || {};
GGRC.config = GGRC.config || {};
GGRC.config.GAPI_ADMIN_GROUP = GGRC.config.GAPI_ADMIN_GROUP || "admins@example.com";

describe("GDrive Workflows Controller", function() {
  var ctl;
  beforeEach(function() {
    waitsFor(function() {
      return (ctl = $(document.body).control(GGRC.Controllers.GDriveWorkflow));
    }, 5000);
  });
  describe("#update_permission_for", function() {

    var item, permissionId, role, saved_object;
    beforeEach(function() {
      item = new CMS.Models.GDriveFolder({
        id : "a folder id"
        , userPermission : {
          role : "writer"
        }
      });
      permissionId = "permission id";
      role = "writer";
      saved_object = undefined;

      spyOn(CMS.Models.GDriveFolderPermission.prototype, "save").andCallFake(function() {
        saved_object = this;
        expect(saved_object.folder).toBe(item);
        expect(saved_object.role).toBe(role);
        return $.when();
      });
    });

    it("creates permission object for user by email address", function() {
      var person = "foo@example.com";
      
      spyOn(CMS.Models.GDriveFolder.prototype, "findPermissions").andCallFake(function() { return $.when([]); });

      ctl.update_permission_for(item, person, permissionId, role);
      expect(saved_object).toBeDefined();
      expect(saved_object.email).toBe(person);
      expect(saved_object.permission_type).toBe("user");
    });

    it("creates permission object for user by Person object", function() {
      var person = new CMS.Models.Person({
        id : 1
        , email : "foo@example.com"
      });

      spyOn(CMS.Models.GDriveFolder.prototype, "findPermissions").andCallFake(function() { return $.when([]); });

      ctl.update_permission_for(item, person, permissionId, role);
      expect(saved_object).toBeDefined();
      expect(saved_object.email).toBe(person.email);
      expect(saved_object.permission_type).toBe("user");
    });

    it("creates group permission object when passed Admin group", function() {
      spyOn(CMS.Models.GDriveFolder.prototype, "findPermissions").andCallFake(function() { return $.when([]); });

      ctl.update_permission_for(item, GGRC.config.GAPI_ADMIN_GROUP, permissionId, role);
      expect(saved_object).toBeDefined();
      expect(saved_object.email).toBe(GGRC.config.GAPI_ADMIN_GROUP);
      expect(saved_object.permission_type).toBe("group");
    });

    //This spec is no longer correct, as all of the extant permissions are now divined in resolve_permissions --BM 4/5/2014
    xit("does not create permissions for users who already have an equivalent permission", function() {
      var person = "foo@example.com";
      
      spyOn(CMS.Models.GDriveFolder.prototype, "findPermissions")
      .andCallFake(function() {
        return $.when([{
          "id" : permissionId
          , "email" : person
          , "role" : "writer"
        }]);
      });

      ctl.update_permission_for(item, person, permissionId, role);
      expect(saved_object).not.toBeDefined();
    });

    it("creates writer permission for users who currently have reader", function() {
      var person = "foo@example.com";
      
      spyOn(CMS.Models.GDriveFolder.prototype, "findPermissions")
      .andCallFake(function() {
        return $.when([{
          "id" : permissionId
          , "email" : person
          , "role" : "reader"
        }]);
      });

      ctl.update_permission_for(item, person, permissionId, role);
      expect(saved_object).toBeDefined();
      expect(saved_object.email).toBe(person);
      expect(saved_object.permission_type).toBe("user");
    });

    afterEach(function() {
      delete CMS.Models.GDriveFolder.cache;
      delete CMS.Models.GDriveFolderPermission.cache;
    });
  });

  describe("#create_folder_if_nonexistent", function() {

    describe("given a Program", function() {

      it("calls out to create_program_folder and does nothing else", function() {
        var program = new CMS.Models.Program({
          id : 1
          , title : "a program"
        });
        spyOn(program, "get_mapping").andReturn([]);

        spyOn(ctl, "create_folder_if_nonexistent").andThrow("ERROR: function tried calling itself for parent object");
        spyOn(ctl.request_create_queue, "push").andThrow("ERROR: function pushed Program folder creation onto the Request queue");
        spyOn(ctl, "link_request_to_new_folder_or_audit_folder").andThrow("ERROR: function tried linking a Program to an Audit's folder");

        spyOn(ctl, "create_program_folder");
        //get a little tricky.  We're already spying on the SUT, so go through it
        ctl.create_folder_if_nonexistent.originalValue.call(ctl, program);
        expect(ctl.create_program_folder).toHaveBeenCalledWith(program.constructor, jasmine.any(Object), program);
      });

    });

    describe("given an Audit", function() {
      var audit;
      beforeEach(function() {
        audit = new CMS.Models.Audit({
          id : 1
          , title : "an audit"
          , program : new CMS.Models.Program({ id : 1 })
          , requests : []
        });
        spyOn(can.Model.Cacheable.prototype, "get_mapping").andReturn([]);
        spyOn(ctl, "create_audit_folder").andReturn($.when());
        spyOn(ctl, "create_program_folder").andReturn($.when());
      });

      it("recursively calls for program", function() {
        spyOn(ctl, "create_folder_if_nonexistent").andReturn($.when());
        ctl.create_folder_if_nonexistent.originalValue.call(ctl, audit);
        expect(ctl.create_folder_if_nonexistent).toHaveBeenCalledWith(jasmine.any(CMS.Models.Program));
      });

      it("calls out to create_audit_folder", function() {

        spyOn(ctl.request_create_queue, "push").andThrow("ERROR: function pushed audit folder creation onto the Request queue");
        spyOn(ctl, "link_request_to_new_folder_or_audit_folder").andThrow("ERROR: function tried linking a audit to another Audit's folder");
        //get a little tricky.  We're already spying on the SUT, so go through it
        ctl.create_folder_if_nonexistent(audit);
        expect(ctl.create_audit_folder).toHaveBeenCalledWith(audit.constructor, jasmine.any(Object), audit);
      });

      it("links in Requests that have no objectives", function() {
        var request = new CMS.Models.Request({
          id : 1
          , audit : audit
        });
        var sanity = false;
        audit.requests.push(request);
        spyOn(CMS.Models.ObjectFolder.prototype, "save").andCallFake(function() {
          sanity = true;
          expect(this instanceof CMS.Models.ObjectFolder).toBe(true);
          expect(this.folderable.reify()).toBe(request);
        });
        spyOn(RefreshQueue.prototype, "trigger").andReturn($.when([request]));
        ctl.create_folder_if_nonexistent(audit);
        expect(sanity).toBe(true);
      });


    });

    describe("given a Request", function() {

      var request;
      beforeEach(function() {
        request = new CMS.Models.Request({
          id : 1
          , audit : new CMS.Models.Audit({
            id : 1
            , program : new CMS.Models.Program({ id : 1 }) })
        });
        request.audit.reify().attr("requests", [request]);
        spyOn(can.Model.Cacheable.prototype, "get_mapping").andReturn([]);
        spyOn(can.Model.Cacheable.prototype, "get_binding").andReturn({ refresh_instances : function() { return $.when(); }});
        spyOn(ctl, "link_request_to_new_folder_or_audit_folder");
        spyOn(ctl.request_create_queue, "push");

        spyOn(ctl, "create_audit_folder").andReturn($.when());
        spyOn(ctl, "create_program_folder").andReturn($.when());
        spyOn(RefreshQueue.prototype, "trigger").andReturn($.when());
      });

      it("recursively creates an audit folder", function() {
        ctl.create_folder_if_nonexistent(request);
        expect(ctl.create_audit_folder).toHaveBeenCalledWith(request.audit.reify().constructor, jasmine.any(Object), request.audit.reify());
      });

      it("calls out to create_request_folder if audit is created", function() {
        ctl.request_create_queue.push.andThrow("ERROR: queued request when audit create was not in progress");
        can.Model.Cacheable.prototype.get_mapping.andCallFake(function() {
          if(this instanceof CMS.Models.Audit) {
            return [{}];
          } else {
            return [];
          }
        });
        ctl.create_folder_if_nonexistent(request);
        expect(ctl.link_request_to_new_folder_or_audit_folder).toHaveBeenCalledWith(request.constructor, jasmine.any(Object), request);
      });

      it("queues Request if Audit create is in progress", function() {
        try {
          ctl._audit_create_in_progress = true;
          ctl.link_request_to_new_folder_or_audit_folder.andThrow("ERROR: created request folder while audit create is in progress");
          ctl.create_folder_if_nonexistent(request);
          expect(ctl.request_create_queue.push).toHaveBeenCalledWith(request);
        } finally {
          delete ctl._audit_create_in_progress;
        }
      });

    });


  });

  describe("UserRole created event", function() {

    it("calls update_permissions only for program with matching context", function() {
      spyOn(ctl, "update_permissions").andReturn(new $.Deferred().resolve({}));

      var p1 = new CMS.Models.Program({id : 1, context : { id : 1 }});
      var p2 = new CMS.Models.Program({id : 2, context : { id : 2 }});

      var role = new CMS.Models.Role({ id : 1, name : "ProgramOwner"});

      var userrole = new CMS.Models.UserRole({
        role : role.stub()
        , context : { id : 1 }
      });

      ctl["{CMS.Models.UserRole} created"](CMS.Models.UserRole, {}, userrole);

      waitsFor(function() {
        return ctl.update_permissions.callCount;
      }, "waiting on delayed update_permissions");
      runs(function() {
        expect(ctl.update_permissions).toHaveBeenCalledWith(CMS.Models.Program, jasmine.any(Object), p1);
        expect(ctl.update_permissions).not.toHaveBeenCalledWith(CMS.Models.Program, jasmine.any(Object), p2);
      });
    });

  });

  afterEach(function() {
    delete CMS.Models.Program.cache;
    delete CMS.Models.Audit.cache;
    delete CMS.Models.Request.cache;
    delete CMS.Models.ObjectFolder.cache;
    delete CMS.Models.UserRole.cache;
    delete CMS.Models.Role.cache;
  });

});
