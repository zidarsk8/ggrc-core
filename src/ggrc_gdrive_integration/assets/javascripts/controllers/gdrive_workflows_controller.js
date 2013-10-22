(function(can, $) {
var create_folder = function(cls, title_generator, parent_attr, model, ev, instance) {
  var that = this
  , dfd
  , owner = cls === CMS.Models.Request ? "assignee" : "owner";

  if(instance instanceof cls) {
    if(parent_attr) {
      dfd = instance[parent_attr].reify().get_binding("folders").refresh_instances();
    } else {
      dfd = $.when([{}]); //make parent_folder instance be undefined; 
                          // GDriveFolder.create will translate that into 'root'
    }
    return dfd.then(function(parent_folders) {
      return new CMS.Models.GDriveFolder({
        title : title_generator(instance)
        , parents : parent_folders[0].instance
      }).save();
    }).then(function(folder) {
      var refresh_queue;

      new CMS.Models.ObjectFolder({
        folder : folder
        , folderable : instance
        , context : instance.context || { id : null }
      }).save();

      if(instance[owner] && instance[owner].id !== GGRC.current_user.id) {
        refresh_queue = new RefreshQueue().enqueue(instance[owner].reify());
        refresh_queue.trigger().done(function() {
          new CMS.Models.GDriveFolderPermission({
            folder : folder
            , person : instance[owner]
            , role : "writer"
          }).save();
        });
      }
    });
  }
  else {
    dfd = new $.Deferred();
    return dfd.reject("Type mismatch");
  }
};

function partial_proxy(fn) {
  var args = can.makeArray(arguments).slice(1);
  return function() {
    return fn.apply(this, args.concat(can.makeArray(arguments)));
  };
}

can.Control("GGRC.Controllers.GDriveWorkflow", {

}, {
  request_create_queue : []

  , "{CMS.Models.Program} created" : partial_proxy(create_folder, CMS.Models.Program, function(inst) { return inst.title + " Audits"; }, null)

  , create_audit_folder : partial_proxy(create_folder, CMS.Models.Audit, function(inst) { return inst.title; }, "program")
  , "{CMS.Models.Audit} created" : function(model, ev, instance) {
    if(instance instanceof CMS.Models.Audit) {
      this._audit_create_in_progress = true;
      this.create_audit_folder(model, ev, instance)
      delete this._audit_create_in_progress;
    }
  }

  // if we had to wait for an Audit to get its own folder link on creation, we can now do the delayed creation
  //  of folder links for the audit's requests, which were created first in the PBC workflow
  , "{CMS.Models.ObjectFolder} created" : function(model, ev, instance) {
    var i, that = this;
    if(instance instanceof CMS.Models.ObjectFolder && instance.folderable.reify() instanceof CMS.Models.Audit) {
      instance.folderable.reify().refresh().then(function() {
        for(i = that.request_create_queue.length; i--;) {
          if(that.request_create_queue[i].audit.reify() === instance.folderable.reify()) {
            that.create_request_folder(CMS.Models.Request, ev, that.request_create_queue[i]);
            that.request_create_queue.splice(i, 1);
          }
        }
      });
    }
  }

  // When creating requests as part of audit workflow, wait for audit to have a folder link before
  // trying to create subfolders for request.  If the audit and its folder link are already created
  //  we can do the request folder immediately.
  , create_request_folder : partial_proxy(create_folder, CMS.Models.Request, function(inst) { return inst.objective.reify().title; }, "audit")
  , "{CMS.Models.Request} created" : function(model, ev, instance) {
    if(instance instanceof CMS.Models.Request) {
      if(this._audit_create_in_progress || instance.audit.reify().object_folders.length < 1) {
        this.request_create_queue.push(instance);
      } else {
        this.create_request_folder(model, ev, instance);
      }
    }
  }

  , update_owner_permission : function(model, ev, instance) {
    var owner = instance instanceof CMS.Models.Request ? "assignee" : "owner";
    var person;
    if(~can.inArray(instance.constructor.shortName, ["Program", "Audit", "Request"]) && instance[owner]) {
      person = instance[owner].reify();
      instance.get_binding("folders").refresh_instances().then(function(list) {
        can.each(list, function(binding) {
          binding.instance.findPermissions().then(function(permissions) {
            var matching = can.map(permissions, function(permission) {
              if(permission.type === "user"
                && permission.emailAddress === person.email
                && (permission.role === "owner" || permission.role === "writer")
              ) {
                return permission;
              }
            });
            if(matching.length < 1) {
              new CMS.Models.GDriveFolderPermission({
                folder : binding.instance
                , person : person
                , role : "writer"
              }).save();
            }
          });
        });
      });
    }


  }
  , "{CMS.Models.Program} updated" : "update_owner_permission"
  , "{CMS.Models.Audit} updated" : "update_owner_permission"
  , "{CMS.Models.Request} updated" : "update_owner_permission"
});

$(function() {
  $(document.body).ggrc_controllers_g_drive_workflow();
});

})(this.can, this.can.$);
