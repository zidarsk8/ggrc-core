/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/

(function(can, $) {

can.Control("GGRC.Controllers.InfoWidget", {
  defaults : {
    model : null
    , instance : null
    , widget_view : GGRC.mustache_path + "/base_objects/info.mustache"
  }
  , init : function() {
    var that = this;
    $(function() {
      if (GGRC.page_object) {
        $.extend(that.defaults, {
          model : GGRC.infer_object_type(GGRC.page_object)
          , instance : GGRC.page_instance()
        });
      }
    });
  }
}, {
  init : function() {
    var that = this;
    this.init_menu();

    if (this.element.data('widget-view')) {
      this.options.widget_view = GGRC.mustache_path + this.element.data('widget-view');
    }

    this.options.context = new can.Observe({
        model : this.options.model,
        instance : this.options.instance,
        start_menu : this.options.start_menu,
        object_menu : this.options.object_menu,
        workflow_view : GGRC.mustache_path + "/dashboard/info/workflow_progress.mustache",
        workflow_data: {},
        task_view : GGRC.mustache_path + "/dashboard/info/my_tasks.mustache",
        task_data: {},
        //audit_view : GGRC.mustache_path + "/dashboard/info/my_audits.mustache",
        //audit_data:{},
        task_count : 0,
        error_msg : '',
        error : true
      });
    can.view(this.get_widget_view(this.element), this.options.context, function(frag) {
      that.element.html(frag);
    });

    var test_a = this.options.context;
    //If dashboard then do these 2 lines below
    if (/dashboard/.test(window.location)){
      this.load_my_workflows();
      this.initialize_task_filter();
      this.load_my_tasks();
      //this.load_my_audits();
    }
  }

  , get_widget_view: function(el) {
      var widget_view = $(el)
            .closest('[data-widget-view]').attr('data-widget-view');
      if (widget_view && widget_view.length > 0)
        return GGRC.mustache_path + widget_view;
      else
        return this.options.widget_view;
    }

  , init_menu: function(){
    var start_menu,
        object_menu;

    if(!this.options.start_menu) {
      start_menu = [
        { model_name: 'Program', model_lowercase: 'program', model_plural: 'programs', display_name: 'Start new Program'},
        { model_name: 'Audit', model_lowercase: 'audit', model_plural: 'audits', display_name: 'Start new Audit'},
        { model_name: 'Workflow', model_lowercase: 'workflow', model_plural: 'workflows', display_name: 'Start new Workflow'}
      ];
      this.options.start_menu = start_menu;
    }
    if(!this.options.object_menu) {
      object_menu = [
        { model_name: 'Regulation', model_lowercase: 'regulation', model_plural: 'regulations', display_name: 'Regulations'},
        { model_name: 'Policy', model_lowercase: 'policy', model_plural: 'policies', display_name: 'Policies'},
        { model_name: 'Standard', model_lowercase: 'standard', model_plural: 'standards', display_name: 'Standards'},
        { model_name: 'Contract', model_lowercase: 'contract', model_plural: 'contracts', display_name: 'Contracts'},
        { model_name: 'Clause', model_lowercase: 'clause', model_plural: 'clauses', display_name: 'Clauses'},
        { model_name: 'Section', model_lowercase: 'section', model_plural: 'sections', display_name: 'Sections'},
        { model_name: 'Objective', model_lowercase: 'objective', model_plural: 'objectives', display_name: 'Objectives'},
        { model_name: 'Control', model_lowercase: 'control', model_plural: 'controls', display_name: 'Controls'},
        { model_name: 'Person', model_lowercase: 'person', model_plural: 'people', display_name: 'People'},
        { model_name: 'OrgGroup', model_lowercase: 'org_group', model_plural: 'org_groups', display_name: 'Org Groups'},
        { model_name: 'Vendor', model_lowercase: 'vendor', model_plural: 'vendors', display_name: 'Vendors'},
        { model_name: 'System', model_lowercase: 'system', model_plural: 'systems', display_name: 'Systems'},
        { model_name: 'Process', model_lowercase: 'process', model_plural: 'processs', display_name: 'Processes'},
        { model_name: 'DataAsset', model_lowercase: 'data_asset', model_plural: 'data_assets', display_name: 'Data Assets'},
        { model_name: 'Product', model_lowercase: 'product', model_plural: 'products', display_name: 'Products'},
        { model_name: 'Project', model_lowercase: 'project', model_plural: 'projects', display_name: 'Projects'},
        { model_name: 'Facility', model_lowercase: 'facility', model_plural: 'facilities', display_name: 'Facilities'},
        { model_name: 'Market', model_lowercase: 'market', model_plural: 'markets', display_name: 'Markets'}
      ];
      this.options.object_menu = object_menu;
    }
  }

  , insert_options: function(options, my_view, component_class, prepend){
    var self = this,
        dfd = $.Deferred();

        can.view(my_view, new can.Map(options), function(frag) {
          if (self.element) {
            if (prepend)
              self.element.find(component_class).prepend(frag);
            else
              self.element.find(component_class).append(frag);
          }
          dfd.resolve();
        });
        return dfd;
  }

  , update_tasks_for_workflow: function(workflow){
    var self = this,
        dfd = $.Deferred(),
        task_count = 0,
        finished = 0,
        in_progress = 0,
        declined = 0,
        verified = 0, 
        assigned = 0,
        over_due = 0,
        today = new Date(),
        first_end_date,
        task_data = {};

      workflow.get_binding('current_all_tasks').refresh_instances().then(function(d){
        var mydata = d;
        task_count = mydata.length;
        for(var i = 0; i < task_count; i++){
          var data = mydata[i].instance,
              end_date = new Date(data.end_date || null);

          //Calculate first_end_date for the workflow / earliest end for all the tasks in a workflow
          if (i === 0)
            first_end_date = end_date;
          else if (end_date.getTime() < first_end_date.getTime())
            first_end_date = end_date;

          //Any task not finished or verified is subject to overdue
          if (data.status === 'Finished')
            finished++;
          else if (data.status === 'Verified')
            verified++;
          else {
            if (end_date.getTime() < today.getTime()) {
              over_due++;
              self.options.context.attr('error_msg', 'Some tasks are over due!')
            }
            else if (data.status === 'InProgress')
              in_progress++;
            else if (data.status === 'Declined')
              declined++;
            else
              assigned++;
          }
        }
        //Calculate %
        if (task_count > 0) {
          task_data.task_count = task_count;
          task_data.finished = finished;
          task_data.finished_percentage = Math.floor((finished * 100) / task_count); //ignore the decimal part
          task_data.in_progress = in_progress;
          task_data.in_progress_percentage = Math.floor((in_progress * 100) / task_count);
          task_data.verified = verified;
          task_data.verified_percentage = Math.floor((verified * 100) / task_count);
          task_data.declined = declined;
          task_data.declined_percentage = Math.floor((declined * 100) / task_count);
          task_data.over_due = over_due;
          task_data.over_due_percentage = Math.floor((over_due * 100) / task_count);
          task_data.assigned = assigned;
          task_data.assigned_percentage = Math.floor((assigned * 100) / task_count);
          task_data.first_end_date = first_end_date.toLocaleDateString();
          //calculate days left for first_end_date
          if(today.getTime() >= first_end_date.getTime())
            task_data.days_left_for_first_task = 0;
          else {
            var time_interval = first_end_date.getTime() - today.getTime();
            var day_in_milli_secs = 24 * 60 * 60 * 1000;
            task_data.days_left_for_first_task = Math.floor(time_interval/day_in_milli_secs);
          }

          //set overdue flag
          task_data.over_due_flag = over_due ? true : false;
        }

        workflow.attr('task_data', new can.Map(task_data));
        dfd.resolve();
      });

      return dfd;
  }

  , load_my_workflows: function(){
    var self = this,
        my_view = this.options.context.workflow_view,
        component_class = 'ul.workflow-tree',
        prepend = true,
        workflow_data = {},
        wfs;

      GGRC.Models.Search.search_for_types('', ['Workflow'], {contact_id: GGRC.current_user.id})
      .then(function(result_set){
          var wf_data = result_set.getResultsForType('Workflow');
          var refresh_queue = new RefreshQueue();
          refresh_queue.enqueue(wf_data);
          return refresh_queue.trigger();
      }).then(function(options){
          wfs = options;

          return $.when.apply($, can.map(options, function(wf){
            return self.update_tasks_for_workflow(wf);
          }));
      }).then(function(){
        if(wfs.length > 0){
          //TBD sort workflows for the first 5 workflow-end-dates
          workflow_data.list = wfs;
          self.options.context.attr('workflow_data', workflow_data);
          self.insert_options(workflow_data, my_view, component_class, prepend);
        }
      });

    return 0;
  }

  , initialize_task_filter: function(){
    var filter = {
      status: '',     //initialy any task should be displayed
      object: '',     // not filtered by any object, object = empty string
      workflow: '',   // not filtered by workflow, workflow = empty string
      overdue: 0      // not filtered by overdue status
    };
    if (!this.options.task_filter) {
      this.options.task_filter = filter;
      //this.options.context.attr('task_filters', task_filters);
    }
  }

  , load_my_tasks: function(){
    var self = this,
        my_view = this.options.context.task_view,
        task_data = {},
        component_class = 'ul.task-tree',
        prepend = true;

    //To get the tasks only for the current person/current cycle
    var loader = GGRC.page_instance().get_binding("assigned_tasks");
    if(loader) {
      loader.refresh_instances().then(function(tasks) {
        self.options.context.attr('task_count', tasks.length);
        task_data.list = tasks;
        task_data.filtered_list = tasks;
        if (!self.options.task_data)
          self.options.task_data = task_data;
        self.options.context.attr('task_data', task_data);
        //Here the data is not filtered
        self.insert_options(task_data, my_view, component_class, prepend);
      })
    }
    return 0;
  }

  ////button actions  
  , "input[data-lookup] focus" : function(el, ev) {
    this.autocomplete(el);
  }

  , autocomplete : function(el) {
    $.cms_autocomplete.call(this, el);
  }

  , autocomplete_select : function(el, ev, ui) {
      setTimeout(function(){
        if (ui.item.title) {
          el.val(ui.item.title, ui.item);
        } else {
          el.val(ui.item.name ? ui.item.name : ui.item.email, ui.item);
        }
        el.trigger('change');
      }, 0);
  }

  , is_overdue_task : function (task) {
    var end_date = new Date(task.instance.end_date || null),
        today = new Date();

    //Any task that is not finished or verified are subject to overdue
    if (task.status === "Finished" || task.status === "Verified")
      return false;
    else if (end_date.getTime() < today.getTime())
      return true;
  }

  , filter_task_data : function() {
    var list = this.options.context.task_data.list, //original list of data
        i,
        task_data = {},
        list1 = [], //list filtered by status
        my_list = [],
        list2 = [], //list filtered by object or workflow
        filtered_list = [], //final filtered list
        filter = this.options.task_filter,
        status_flag = false,
        cycle,
        obj,
        obj_flag = false;

    //Filter by status first
    if (filter.overdue === 1) {
      status_flag = true;
      for (i = 0; i < list.length; i++) {
        if (this.is_overdue_task(list[i]))
          list1.push(list[i]);
      }
    } else if (filter.status === "Verified"){
      status_flag = true;
      for (i = 0; i < list.length; i++)
        if (list[i].status === "Verified")
          list1.push(list[i]);
    } else if (filter.status === "Finished"){
      status_flag = true;
      for (i = 0; i < list.length; i++)
        if (list[i].status === "Finished")
          list1.push(list[i]);
    } else if (filter.status === "InProgress"){
      status_flag = true;
      for (i = 0; i < list.length; i++)
        if (list[i].status === "InProgress")
          list1.push(list[i]);
    } else if (filter.status === "Assigned"){
      status_flag = true;
      for (i = 0; i < list.length; i++)
        if (list[i].status === "Assigned")
          list1.push(list[i]);
    }

    //Now filter by object and workflow
    if (status_flag){
        my_list = list1;
    } else {
        my_list = list;
    }

    if (filter.workflow !== '' && filter.object !== '') {
      obj_flag = true;
      for (i = 0; i < my_list.length; i++) {
        cycle = my_list[i].cycle.reify();
        obj = my_list[i].cycle_task_group_object;
        if (filter.workflow === cycle.workflow.title && filter.object === obj.object.title)
          list2.push(my_list[i]);
      }

    } else if (filter.workflow !== '') {
      obj_flag = true;
      for (i = 0; i < my_list.length; i++) {
        cycle = my_list[i].instance.cycle.reify();
        if (filter.workflow === cycle.title)
          list2.push(my_list[i]);
      }
    } else if (filter.object !== '') {
      obj_flag = true;
      for (i = 0; i < my_list.length; i++) {
        if (my_list[i].instance.cycle_task_group_object) {
          obj = my_list[i].instance.cycle_task_group_object.reify();
          if (filter.object === obj.title)
            list2.push(my_list[i]);
        }
      }
    }

    if (obj_flag) {
      filtered_list = list2;
    } else if (status_flag) {
      filtered_list = list1;
    } else {
      filtered_list = list;
    }

    task_data.list = list;
    task_data.filtered_list = filtered_list;
    this.options.task_data = task_data;
    this.options.context.attr('task_data', task_data);
  }

  , "input[type=text], input[type=checkbox].filter-overdue, select change" : function(el, ev) {
    //console.log("selection changed-------");
    var filter_task_data = {};
    filter_task_data.list = [];
    var filters = {};
    //find all the filters, filter the existing task_data, don't need to go to the server
    //show the data
    var obj = this.element.find('input[name="object"]').val();
    var wf = this.element.find('input[name="workflow"]').val();
    var status = this.element.find('select[name="status"]').val();
    var overdue = this.element.find('input[type=checkbox].filter-overdue:checked').length;
    console.log(obj + " : " + wf + " : " + status + " : " + overdue);

    //set up task filter
    this.options.task_filter.status = status;
    this.options.task_filter.object = obj;
    this.options.task_filter.workflow = wf;
    this.options.task_filter.overdue = overdue;

    //filter task_data
    this.filter_task_data();

    this.element.find('ul.task-tree').empty();
    this.insert_options(this.options.task_data, this.options.context.task_view, 'ul.task-tree', true);

    ev.stopPropagation();
  }

});

})(this.can, this.can.$);
