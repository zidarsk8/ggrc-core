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
        task_view : GGRC.mustache_path + "/dashboard/info/my_tasks.mustache",
        error_msg : 'This is global messaging letting you know that something is over due!',
        error : true
      });
    can.view(this.get_widget_view(this.element), this.options.context, function(frag) {
      that.element.html(frag);
    });

    var test_a = this.options.context;
    //Fixme if dashboard then do these 2 lines below
    this.load_my_workflows();
    this.load_my_tasks();
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
        context = {},
        dfd = $.Deferred();

        //console.log("insert_options");
        context.options = options;

        can.view(my_view, new can.Map(context), function(frag) {
          if (self.element) {
            if (prepend)
              self.element.find(component_class).prepend(frag);//self.element.find('ul.workflow-tree').prepend(frag);
            else
              self.element.find(component_class).append(frag);
          }
          dfd.resolve();
        });
        return dfd;
  }

  , update_tasks_for_workflow: function(workflow){
    var dfd = $.Deferred(),
        task_count = 0,
        finished = 0,
        in_progress = 0,
        assigned = 0,
        over_due = 0,
        task_data = {};
      workflow.get_binding('current_all_tasks').refresh_instances().then(function(d){
        task_count = d.length;
        for(var i = 0; i < task_count; i++){
          if (d[i].status === "Finished")
            finished++;
          else if (d[i].status === "InProgress")
            in_progress++;
          else {
            var end_date = new Date(d[i].end_date || null);
            var today = new Date();
            if (end_date.getTime() < today.getTime())
              over_due++;
            else
              assigned++;
          }
        }
        //Calculate %

        task_data.finished = (finished * 100) / task_count;
        task_data.in_progress = (in_progress * 100) / task_count;
        task_data.over_due = (over_due * 100) / task_count;
        task_data.assigned = (assigned * 100) / task_count;
        workflow.task_data = task_data
        dfd.resolve();
      });

      return dfd;
  }

  , load_my_workflows: function(){
    var my_workflows,
        self = this,
        my_view = this.options.context.workflow_view,
        component_class = 'ul.workflow-tree',
        prepend = true;

    GGRC.Models.Search.search_for_types('', ['Workflow'], {contact_id: GGRC.current_user.id})
      .then(function(result_set){
          var wf_data = result_set.getResultsForType('Workflow');
          //FIX ME Load data 10 each time
          var refresh_queue = new RefreshQueue();
          refresh_queue.enqueue(wf_data);
          refresh_queue.trigger().then(function(options){
            var wf, i, tasklist;
            for (i = 0; i < options.length; i++){
              wf=options[i];
              console.log(wf);
              wf.get_binding('current_all_tasks').refresh_instances().then(function(d){
                //console.log(d.length);
              });

              //self.update_tasks_for_workflow(wf);
              console.log(wf);
            }
            //Create a view and update here
            if(options.length > 0)
              self.insert_options(options, my_view, component_class, prepend);
          });
      });
    return 0;
  }

  , load_my_tasks: function(){
    var my_tasks,
        self = this,
        my_view = this.options.context.task_view,
        component_class = 'ul.task-tree',
        prepend = true;
    //The below search loads all tasks so far, so history is also loaded
    /*GGRC.Models.Search.search_for_types('', ['CycleTaskGroupObjectTask'], {contact_id: GGRC.current_user.id})
      .then(function(result_set){
          var task_data = result_set.getResultsForType('CycleTaskGroupObjectTask');
          var refresh_queue = new RefreshQueue();
          //FIX ME Load data 10 each time
          refresh_queue.enqueue(task_data);
          refresh_queue.trigger().then(function(options){
            //Create a view and update here
            self.insert_options(options, my_view, component_class, prepend);
          });
        });
    */
    //To get the tasks only for the current person/current cycle
    var loader = GGRC.page_instance().get_binding("assigned_tasks");
    if(loader) {
      loader.refresh_instances().then(function(tasks) {
        self.insert_options(tasks, my_view, component_class, prepend);
      })
    }
    /*GGRC.page_instance().get_binding("assigned_tasks").refresh_instances()
      .then(function(tasks) {
        //var mytasks=tasks; console.log(tasks)
        if(tasks.length > 0)
          self.insert_options(tasks, my_view, component_class, prepend);
      })*/
    return 0;
  }

});

})(this.can, this.can.$);
