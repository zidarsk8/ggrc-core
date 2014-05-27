/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/

//= require can.jquery-all
//= require controllers/tree_view_controller
//= require controls/control
//= require controls/category

/*  RefreshQueue
 *
 *  enqueue(obj, force=false) -> queue or null
 *  trigger() -> Deferred
 */

can.Construct("ModelRefreshQueue", {
}, {
    init: function(model) {
      this.model = model;
      this.ids = [];
      this.deferred = new $.Deferred();
      this.triggered = false;
      this.completed = false;
      this.updated_at = Date.now();
    }

  , enqueue: function(id) {
      if (this.triggered)
        return null;
      else {
        if (this.ids.indexOf(id) === -1) {
          this.ids.push(id);
          this.updated_at = Date.now();
        }
        return this;
      }
    }

  , trigger: function() {
      var self = this;
      if (!this.triggered) {
        this.triggered = true;
        if (this.ids.length > 0)
          this.model.findAll({ id__in: this.ids.join(",") }).then(function() {
            self.completed = true;
            self.deferred.resolve();
          }, function() {
            self.deferred.reject.apply(self.deferred, arguments);
          });
        else {
          this.completed = true;
          this.deferred.resolve();
        }
      }
      return this.deferred;
    }

  , trigger_with_debounce: function(delay, manager) {
      var ms_to_wait = (delay || 0) + this.updated_at - Date.now();

      if (!this.triggered) {
        if (ms_to_wait < 0 && (!manager || manager.triggered_queues().length < 6))
          this.trigger();
        else
          setTimeout(this.proxy("trigger_with_debounce", delay, manager), ms_to_wait);
      }

      return this.deferred;
    }
});

can.Construct("RefreshQueueManager", {
    model_bases: {
      // This won't work until Relatable/Documentable/etc mixins can handle
      // queries with multiple `type` values.
      //  Regulation: 'Directive'
      //, Contract: 'Directive'
      //, Policy: 'Directive'
      //, Standard: 'Directive'
      //, System: 'SystemOrProcess'
      //, Process: 'SystemOrProcess'
    }
}, {
    init: function() {
      this.null_queue = new ModelRefreshQueue(null);
      this.queues = [];
    }

  , triggered_queues: function() {
      return can.map(this.queues, function(queue) {
        if (queue.triggered)
          return queue;
      });
    }

  , enqueue: function(obj, force) {
      var self = this
        , model = obj.constructor
        , model_name = model.shortName
        , found_queue = null
        , id = obj.id
        ;

      if (!obj.selfLink) {
        if (obj instanceof can.Model) {
          model_name = obj.constructor.shortName;
        } else if (obj.type) {
          // FIXME: obj.kind is to catch invalid stubs coming from Directives
          model_name = obj.type || obj.kind;
        }
      }
      model = CMS.Models[model_name];

      if (this.constructor.model_bases[model_name]) {
        model_name = this.constructor.model_bases[model_name];
        model = CMS.Models[model_name];
      }

      if (!force)
        // Check if the ID is already contained in another queue
        can.each(this.queues, function(queue) {
          if (!found_queue
              && queue.model === model && queue.ids.indexOf(id) > -1)
            found_queue = queue;
        });

      if (!found_queue) {
        can.each(this.queues, function(queue) {
          if (!found_queue && queue.model === model
              && !queue.triggered && queue.ids.length < 50) {
            found_queue = queue.enqueue(id);
            return false;
          }
        });
        if (!found_queue) {
          found_queue = new ModelRefreshQueue(model);
          this.queues.push(found_queue)
          found_queue.enqueue(id);
          found_queue.deferred.done(function() {
            var index = self.queues.indexOf(found_queue);
            if (index > -1)
              self.queues.splice(index, 1);
          });
        }
      }

      return found_queue;
    }
});

can.Construct("RefreshQueue", {
    refresh_queue_manager: new RefreshQueueManager()
}, {
    init: function() {
      this.objects = [];
      this.queues = [];
      this.deferred = new $.Deferred();
      this.triggered = false;
      this.completed = false;
    }

  , enqueue: function(obj, force) {
      var that = this;
      if (!obj)
        return;
      if (this.triggered)
        return null;
      if (obj.push) {
        can.each(obj, function(o) {
          that.enqueue(o, force);
        });
        return this;
      }

      this.objects.push(obj);
      if (force || !obj.selfLink) {
        queue = this.constructor.refresh_queue_manager.enqueue(obj, force);
        if (this.queues.indexOf(queue) === -1)
          this.queues.push(queue);
      }
      return this;
    }

  , trigger: function(delay) {
      var self = this
        , deferreds = []
        ;

      if (!delay)
        delay = 50;

      this.triggered = true;
      can.each(this.queues, function(queue) {
        deferreds.push(queue.trigger_with_debounce(
            50, self.constructor.refresh_queue_manager));
      });

      if (deferreds.length > 0)
        $.when.apply($, deferreds).then(function() {
          self.deferred.resolve(can.map(self.objects, function(obj) {
            return obj.reify();
          }));
        }, function() {
          self.deferred.reject.apply(self.deferred, arguments);
        });
      else
        return this.deferred.resolve(this.objects);

      return this.deferred;
    }
});


(function(can, $) {

if(!/^\/programs\/\d+/.test(window.location.pathname))
 return;

$(function() {
  var program_widget_descriptors = {
      person: {
          widget_id: "person"
        , widget_name: "People"
        , widget_icon: "person"
        , content_controller: GGRC.Controllers.TreeView
        , content_controller_options: {
              show_view: GGRC.mustache_path + "/ggrc_basic_permissions/people_roles/authorizations_by_person_tree.mustache"
            , footer_view: GGRC.mustache_path + "/ggrc_basic_permissions/people_roles/authorizations_by_person_tree_footer.mustache"
            , parent_instance: GGRC.page_instance()
            , allow_reading: true
            , allow_mapping: true
            , allow_creating: true
            , model: CMS.Models.Person
            , mapping: "mapped_and_or_authorized_people"
            }
        }
  };

  if (/programs\/\d+/.test(window.location)) {
    if (!GGRC.widget_descriptors)
      GGRC.widget_descriptors = {};
    $.extend(GGRC.widget_descriptors, program_widget_descriptors);
  }

});

})(window.can, window.can.$);
