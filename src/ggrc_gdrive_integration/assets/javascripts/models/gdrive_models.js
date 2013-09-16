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

can.Model("GGRC.Models.GDriveFolder", {

  findAll : {
    url : "https://script.google.com/macros/s/" + GGRC.config.GDRIVE_SCRIPT_ID + "/exec"
    , type : "post"
    , dataType : "json"
    , data : { command : 'listfolders', parentfolderid : GGRC.config.GDRIVE_ROOT_FOLDER }
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
    if(typeof object === "object") {
      object = this.store[object];
    }
    return $.ajax({
      type : "POST"
      , url : "https://script.google.com/macros/s/" + GGRC.config.GDRIVE_SCRIPT_ID + "/exec?"
      , dataType : "json"
      , data : JSON.stringify({
        command : "deletefolder"
        , folderid : id
        , parentfolderid : parent_id
      })
    }).done(function(parents) {
      obj.attr("parents", parents);
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

can.Model("GGRC.Models.GDriveFile", {

  findAll : {
    url : "https://script.google.com/macros/s/" + GGRC.config.GDRIVE_SCRIPT_ID + "/exec"
    , type : "post"
    , dataType : "json"
    , data : { command : 'listfiles', id : GGRC.config.GDRIVE_ROOT_FOLDER }
  }

  , destroy : function() {
    throw "Destroy is not supported for GDrive Files. Use removeFromParent";
  }

}, {});

can.Model("GGRC.Models.GDriveFolderPermission", {

  findAll : {
    url : "https://script.google.com/macros/s/" + GGRC.config.GDRIVE_SCRIPT_ID + "/exec"
    , type : "post"
    , dataType : "json"
    , data : { command : 'getFolderPermissions', id : GGRC.config.GDRIVE_ROOT_FOLDER }
  }

}, {});

})(window.can);