/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/


(function(can) {

  can.Model.Cacheable("CMS.Models.Workflow", {
    root_object: "workflow",
    root_collection: "workflows",
    category: "workflow",
    mixins: ["ownable"],
    findAll: "GET /api/workflows",
    findOne: "GET /api/workflows/{id}",
    create: "POST /api/workflows",
    update: "PUT /api/workflows/{id}",
    destroy: "DELETE /api/workflows/{id}",
    attributes: {
      objects: "CMS.Models.get_stubs",
      workflow_objects: "CMS.Models.WorkflowObject.stubs",
      people: "CMS.Models.Person.stubs",
      workflow_people: "CMS.Models.WorkflowPerson.stubs",
      tasks: "CMS.Models.Task.stubs",
      workflow_tasks: "CMS.Models.WorkflowTask.stubs",
      task_groups: "CMS.Models.TaskGroup.stubs",
      cycles: "CMS.Models.Cycle.stubs",
      start_date: "date",
      end_date: "date",
      //workflow_task_groups: "CMS.Models.WorkflowTaskGroup.stubs"
      modified_by : "CMS.Models.Person.stub"
    },

    tree_view_options : {
      show_view : GGRC.mustache_path + "/workflows/tree.mustache"
    },

    init: function() {
      this._super && this._super.apply(this, arguments);
      this.validatePresenceOf("title");
    },
  }, {

    start_day_of_month : can.compute(function(val) {
      var newdate;
      if(val) {
        newdate = new Date(this.start_date);
        newdate.setDate(val);
        this.attr("start_date", newdate);
      } else {
        return this.attr("start_date").getDate();
      }
    }),
    end_day_of_month : can.compute(function(val) {
      var newdate;
      if(val) {
        newdate = new Date(this.end_date);
        newdate.setDate(val);
        this.attr("end_date", newdate);
      } else {
        return this.attr("end_date").getDate();
      }
    }),
    start_month_of_quarter : can.compute(function(val) {
      var newdate;
      if(val) {
        newdate = new Date(this.start_date);
        newdate.setMonth((val - 1) % 3);
        this.attr("start_date", newdate);
      } else {
        return this.attr("start_date").getMonth() % 3 + 1;
      }
    }),
    end_month_of_quarter : can.compute(function(val) {
      var newdate;
      if(val) {
        newdate = new Date(this.end_date);
        newdate.setMonth((val - 1) % 3);
        this.attr("end_date", newdate);
      } else {
        return this.attr("end_date").getMonth() % 3 + 1;
      }    }),
    start_month_of_year : can.compute(function(val) {
      var newdate;
      if(val) {
        newdate = new Date(this.start_date);
        newdate.setMonth(val - 1);
        this.attr("start_date", newdate);
      } else {
        return this.attr("start_date").getMonth() + 1;
      }
    }),
    end_month_of_year : can.compute(function(val) {
      var newdate;
      if(val) {
        newdate = new Date(this.end_date);
        newdate.setMonth(val - 1);
        this.attr("end_date", newdate);
      } else {
        return this.attr("end_date").getMonth() + 1;
      }
    }),
    start_day_of_week : can.compute(function(val) {
      var newdate;
      if(val) {
        val = +val;
        newdate = new Date(this.start_date);
        newdate.setDate((newdate.getDate() + 7 - newdate.getDay() + val - 1) % 7 + 1);
        this.attr("start_date", newdate);
      } else {
        return this.attr("start_date").getDay();
      }
    }),
    end_day_of_week : can.compute(function(val) {
      var newdate;
      if(val) {
        val = +val;
        newdate = new Date(this.end_date);
        newdate.setDate((newdate.getDate() + 7 - newdate.getDay() + val - 1) % 7 + 1);
        this.attr("end_date", newdate);
      } else {
        return this.attr("end_date").getDay();
      }
    })
  });

})(window.can);
