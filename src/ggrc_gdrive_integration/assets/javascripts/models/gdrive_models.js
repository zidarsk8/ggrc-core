/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: Bradley Momberger
 * Maintained By: Bradley Momberger
 */

(function(can) {

$.ajaxPrefilter(function(opts, orig_opts, jqXHR) {

  if(/^https:\/\/script.google.com/.test(opts.url)) {
    opts.data = opts.type.toUpperCase() === "DELETE" ? "" : JSON.stringify(orig_opts.data);
  }

});

can.Model.Cacheable("GGRC.Models.GDriveFolder", {

  findAll : {
    url : "https://script.google.com/macros/s/" + GGRC.config.GDRIVE_SCRIPT_ID + "/exec"
    , type : "post"
    , dataType : "json"
    , data : { command : 'listfolders', id : GGRC.config.GDRIVE_ROOT_FOLDER }
    , beforeSend : function(xhr, s) {
      var data = JSON.parse(s.data);
      if(data.parentfolderid) {
        data.id = data.parentfolderid;
        delete data.parentfolderid;
      }
      s.data = JSON.stringify(data);
    }
    , success : function(objs) {
      can.each(objs, function(obj) {
        obj.selfLink = "#";
      });
    }
  }
  , create : function(params) {
      params.id = params.parentfolderid;
      delete params.parentfolderid;
      return $.ajax({
      url : "https://script.google.com/macros/s/" + GGRC.config.GDRIVE_SCRIPT_ID + "/exec"
      , type : "post"
      , dataType : "json"
      , data : { command : "addfolders", params : [params] }
    });
  }
  , removeFromParent : function(object, parent_id) {
    if(typeof object !== "object") {
      object = this.store[object];
    }
    return $.ajax({
      type : "POST"
      , url : "https://script.google.com/macros/s/" + GGRC.config.GDRIVE_SCRIPT_ID + "/exec?"
      , dataType : "json"
      , data : {
        command : "deletefolders"
        , folderid : object.id
        , parentfolderid : parent_id
      }
    }).done(function(parents) {
      object.attr("parents", parents);
    });
  }
  , destroy : function() {
    throw "Destroy not supported for GDrive Folders. Use removeFromParent";
  }
  , findChildFolders : function(params) {
    if(typeof params !== "string") {
      params = params.id;
    }
    return this.findAll({ parentfolderid : params });
  }
  , addChildFolder : function(parent, params) {
    return this.create($.extend({ parentfolderid : parent.id }, params));
  }
  , from_id : function(id) {
    return new this({ id : id });
  }
  , model : function(params) {
    if(params.url) {
      params.selfLink = "#";
    }
    return this._super.apply(this, arguments);
  }
}, {

  findChildFolders : function() {
    return this.constructor.findChildFolders(this);
  }

  //No longer a destroy per se, but rather unlinking from all parent folders.
  , destroy : function() {
    var that = this;
    if(this.isNew())
      return;
    can.each(this.parents, function(parent) {
      that.constructor.removeFromParent(that, parent.parentId);
    });
  }

});

can.Model.Cacheable("GGRC.Models.GDriveFile", {

  findAll : {
    url : "https://script.google.com/macros/s/" + GGRC.config.GDRIVE_SCRIPT_ID + "/exec"
    , type : "post"
    , dataType : "json"
    , data : { command : 'listfiles', parentfolderid : GGRC.config.GDRIVE_ROOT_FOLDER }
  }

  , destroy : function() {
    throw "Destroy is not supported for GDrive Files. Use removeFromParent";
  }

  , from_id : function(id) {
    return new this({ id : id });
  }

}, {});

can.Model.Cacheable("GGRC.Models.GDriveFolderPermission", {

  findAll : {
    url : "https://script.google.com/macros/s/" + GGRC.config.GDRIVE_SCRIPT_ID + "/exec"
    , type : "post"
    , dataType : "json"
    , data : { command : 'getFolderPermissions', id : GGRC.config.GDRIVE_ROOT_FOLDER }
  }

}, {});


can.Model.Join("CMS.Models.ObjectFolder", {
  root_object : "object_folder"
  , root_collection : "object_folders"
  , findAll: "GET /api/object_folders?__include=folder"
  , create : "POST /api/object_folders"
  , update : "PUT /api/object_folders/{id}"
  , destroy : "DELETE /api/object_folders/{id}"
  , join_keys : {
    folderable : can.Model.Cacheable
    , folder : GGRC.Models.GDriveFolder
  }
  , attributes : {
      modified_by : "CMS.Models.Person.stub"
    , folder : "GGRC.Models.GDriveFolder.stub"
    , folderable : "CMS.Models.get_stub"
  }

  , model : function(params) {
    if(typeof params === "object") {
      params.folder = {
        id : params.folder_id
        , parentfolderid : params.parent_folder_id
      };
    }
    return this._super(params);
  }
}, {});

can.Model.Join("CMS.Models.ObjectFile", {
  root_object : "object_file"
  , root_collection : "object_files"
  , findAll: "GET /api/object_people?__include=person"
  , create : "POST /api/object_people"
  , update : "PUT /api/object_people/{id}"
  , destroy : "DELETE /api/object_people/{id}"
  , join_keys : {
    fileable : can.Model.Cacheable
    , file : GGRC.Models.GDriveFile
  }
  , attributes : {
      modified_by : "CMS.Models.Person.stub"
    , file : "GGRC.Models.GDriveFile.stub"
    , fileable : "CMS.Models.get_stub"
  }

  , model : function(params) {
    if(typeof params === "object") {
      params.folder = {
        id : params.file_id
        , parentfolderid : params.folder_id
      };
    }
    return this._super(params);
  }
}, {});

})(window.can);