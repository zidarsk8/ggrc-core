/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: anze@reciprocitylabs.com
    Maintained By: anze@reciprocitylabs.com
*/

//= require can.jquery-all
//= require models/cacheable

(function(can) {

  can.Model.Cacheable("CMS.Models.NotificationConfig", {
    root_object: "notification_config",
    root_collection: "notification_configs",
    category: "person",
    findAll: "GET /api/notification_config",
    findOne: "GET /api/notification_config/{id}",
    create: "POST /api/notification_config",
    update: "PUT /api/notification_config/{id}",
    destroy: "DELETE /api/notification_config/{id}",
    active: "POST /api/set_active_notifications",
    
    findActive: function(){
      if(GGRC.current_user === null){
        return $.when([]);
      }
      return this.findAll({person_id: GGRC.current_user.id});
    },
    setActive: function(active){
      
      return $.ajax({
        type: 'POST',
        url: this.active.split(' ')[1],
        data: {'active': active},
        contentType: 'application/json;charset=UTF-8',
      });
    }
  }, {});

})(window.can);
