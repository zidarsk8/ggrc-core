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
      modified_by: "CMS.Models.Person.stub",
      owners : "CMS.Models.Person.stubs",
      context: "CMS.Models.Context.stub"
    },

    tree_view_options: {
      show_view: GGRC.mustache_path + "/workflows/tree.mustache"
    },

    init: function() {
      this._super && this._super.apply(this, arguments);
      this.validatePresenceOf("title");
      this.validatePresenceOf("start_date");
      this.validatePresenceOf("end_date");
    },
  }, {

    form_preload: function(new_object_form) {
      if(new_object_form) {
        this.attr("start_date", new Date())
        .attr("end_date", moment().add(1, "month").subtract(1, "day").toDate());
      }
    },

    // start day of month, affects start_date.
    //  Use when month number doesn't matter or is
    //  selectable.
    start_day_of_month: can.compute(function(val) {
      var newdate;
      if(val) {
        while(val.isComputed) {
          val = val();
        }
        if(val > 31) {
          val = 31;
        }
        newdate = new Date(this.start_date || null);
        while(moment(newdate).daysInMonth() < val) {
          newdate.setMonth((newdate.getMonth() + 1) % 12);
        }
        newdate.setDate(val);
        this.attr("start_date", newdate);
      } else {
        newdate = this.attr("start_date");
        if(newdate) {
          return newdate.getDate();
        } else {
          return null;
        }
      }
    }),

    // end day of month, affects end_date.
    //  Use when month number doesn't matter or is
    //  selectable.
    end_day_of_month: can.compute(function(val) {
      var newdate;
      if(val) {
        while(val.isComputed) {
          val = val();
        }
        if(val > 31) {
          val = 31;
        }
        newdate = new Date(this.end_date || null);
        while(moment(newdate).daysInMonth() < val) {
          newdate.setMonth((newdate.getMonth() + 1) % 12);
        }
        newdate.setDate(val);
        this.attr("end_date", newdate);
      } else {
        newdate = this.attr("end_date");
        if(newdate) {
          return newdate.getDate();
        } else {
          return null;
        }
      }
    }),

    // start month of quarter, affects start_date.
    //  Sets month to be a 31-day month in the chosen quarterly cycle:
    //  1 for Jan-Apr-Jul-Oct, 2 for Feb-May-Aug-Nov, 3 for Mar-Jun-Sep-Dec
    start_month_of_quarter: can.compute(function(val) {
      var newdate;
      var month_lookup = [0, 4, 2]; //31-day months in quarter cycles: January, May, March

      if(val) {
        newdate = new Date(this.start_date || null);
        newdate.setMonth(month_lookup[(val - 1) % 3]);
        this.attr("start_date", newdate);
      } else {
        newdate = this.attr("start_date");
        if(newdate) {
          return newdate.getMonth() % 3 + 1;
        } else {
          return null;
        }
      }
    }),

    // end month of quarter, affects end_date.
    //  Sets month to be a 31-day month in the chosen quarterly cycle:
    //  1 for Jan-Apr-Jul-Oct, 2 for Feb-May-Aug-Nov, 3 for Mar-Jun-Sep-Dec
    end_month_of_quarter: can.compute(function(val) {
      var newdate;
      var month_lookup = [0, 7, 2]; //31-day months in quarter cycles: January, May, March

      if(val) {
        newdate = new Date(this.end_date || null);
        newdate.setMonth(month_lookup[(val - 1) % 3]);
        this.attr("end_date", newdate);
      } else {
        newdate = this.attr("end_date");
        if(newdate) {
          return newdate.getMonth() % 3 + 1;
        } else {
          return null;
        }
      }
    }),

    // start month of yesr, affects start_date.
    //  Sets month to the chosen month, and adjusts
    //  day of month to be within chosen month
    start_month_of_year: can.compute(function(val) {
      var newdate;
      if(val) {
        if(val > 12) {
          val = 12;
        }
        newdate = new Date(this.start_date || null);
        if(moment(newdate).date(1).month(val - 1).daysInMonth() < newdate.getDate()) {
          newdate.setDate(moment(newdate).date(1).month(val - 1).daysInMonth());
        }
        newdate.setMonth(val - 1);
        this.attr("start_date", newdate);
      } else {
        newdate = this.attr("start_date");
        if(newdate) {
          return newdate.getMonth() + 1;
        } else {
          return null;
        }
      }
    }),

    // end month of yesr, affects end_date.
    //  Sets month to the chosen month, and adjusts
    //  day of month to be within chosen month
    end_month_of_year: can.compute(function(val) {
      var newdate;
      if(val) {
        if(val > 12) {
          val = 12;
        }
        newdate = new Date(this.end_date || null);
        if(moment(newdate).date(1).month(val - 1).daysInMonth() < newdate.getDate()) {
          newdate.setDate(moment(newdate).date(1).month(val - 1).daysInMonth());
        }
        newdate.setMonth(val - 1);
        this.attr("end_date", newdate);
      } else {
        newdate = this.attr("end_date");
        if(newdate) {
          return newdate.getMonth() + 1;
        } else {
          return null;
        }
      }
    }),

    // start day of week, affects start_date.
    //  Sets day of month to the first day of the
    //  month that is the selected day of the week
    //  Sunday is 0, Saturday is 6
    start_day_of_week: can.compute(function(val) {
      var newdate;
      if(val) {
        val = +val;
        newdate = new Date(this.start_date || null);
        newdate.setDate((newdate.getDate() + 7 - newdate.getDay() + val - 1) % 7 + 1);
        this.attr("start_date", newdate);
      } else {
        newdate = this.attr("start_date");
        if(newdate) {
          return newdate.getDay();
        } else {
          return null;
        }
      }
    }),

    // end day of week, affects end_date.
    //  Sets day of month to the first day of the
    //  month that is the selected day of the week
    //  Sunday is 0, Saturday is 6
    end_day_of_week: can.compute(function(val) {
      var newdate;
      if(val) {
        val = +val;
        newdate = new Date(this.end_date || null);
        newdate.setDate((newdate.getDate() + 7 - newdate.getDay() + val - 1) % 7 + 1);
        this.attr("end_date", newdate);
      } else {
        newdate = this.attr("end_date");
        if(newdate) {
          return newdate.getDay();
        } else {
          return null;
        }
      }
    })
  });

})(window.can);
