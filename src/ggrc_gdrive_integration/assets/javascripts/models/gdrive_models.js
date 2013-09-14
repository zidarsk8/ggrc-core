/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: Bradley Momberger
 * Maintained By: Bradley Momberger
 */

(function(can) {

can.Model("GGRC.Models.GDriveFolder", {

  findAll : function(params) {
    if(!params || !params.parentfolderid) {
      params = { parentfolderid : GGRC.config.GDRIVE_ROOT_FOLDER };
    }
    return $.ajax({
      url : "https://script.google.com/macros/s/" + GGRC.config.GDRIVE_SCRIPT_ID + "/exec?command=listfolders"
      , type : "get"
      , dataType : "json"
      , data : { parameters : JSON.stringify(params) }
    });
  }
  , create : "GET " + /* "https://script.google.com/" + */ "/macros/s/AKfycbxb-W3rUBTKFF6Ua_eJ5PH9RAvGVL7W3aDqtmnbnUc7PD0FY3zo/exec?command=addfolder"
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

});

})(window.can);