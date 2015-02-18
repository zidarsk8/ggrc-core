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
        //show_audit: false;
        error_msg : '',
        error : true
      });
    can.view(this.get_widget_view(this.element), this.options.context, function(frag) {
      that.element.html(frag);
    });

    // If dashboard then load workflow, tasks and audit-count,
    // audits will be loaded when audit tab is clicked
    if (/dashboard/.test(window.location)){
      this.options.initial_wf_size = 5;

      // this.load_my_workflows();
      // this.initialize_task_filter();
      // this.load_my_tasks();
      // this.options.show_audit = false;
      // this.load_audit_count();
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

  , display_tasks: function(loader) {
    var self = this,
        my_view = this.options.context.task_view,
        task_data = {},
        component_class = 'ul.task-tree',
        prepend = true;

      loader.refresh_instances().then(function(tasks) {
        self.options.context.attr('task_count', tasks.length);
        task_data.list = tasks;
        task_data.filtered_list = tasks;
        self.options.task_data = task_data;
        self.options.context.attr('task_data', task_data);
        self.element.find(component_class).empty();
        self.insert_options(task_data, my_view, component_class, prepend);
        self.options.context.attr('tasks_loaded', true);
      })
      return 0;
  }

  , load_my_tasks: function(){
    //To get the tasks only for the current person/current cycle
    var loader = GGRC.page_instance().get_binding("assigned_tasks");
    if(loader) {
      this.display_tasks(loader);
    }
    return 0;
  }

  , load_task_with_history: function() {
    //load assigned tasks and history
    var loader = GGRC.page_instance().get_binding("assigned_tasks_with_history");
    if(loader) {
      this.display_tasks(loader);
    }
    return 0;
  }

  , load_audit_count:function() {
    var self = this;

    if (!GGRC.current_user) {
      return 0;
    }

    GGRC.page_instance().get_binding("open_audit_requests").refresh_count()
      .then(function(result) {
        self.options.context.attr('audit_count', result());
    });
    return 0;
  }

  , load_my_audits: function() {
    var self = this,
        my_view = this.options.context.audit_view,
        audit_data = {},
        component_class = 'ul.audit-tree',
        prepend = true,
        loader;

    //Get the audits only for the current person
    loader = GGRC.page_instance().get_binding("open_audit_requests");
    if (loader) {
      loader.refresh_instances().then(function(audits) {
        self.options.context.attr('audit_count', audits.length);
        audit_data.list = audits;
        //task_data.filtered_list = tasks;
        self.options.audit_data = audit_data;
        self.options.context.attr('audit_data', audit_data);
        self.element.find(component_class).empty();
        self.insert_options(audit_data, my_view, component_class, prepend);
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
    if (task.instance.status === "Finished" || task.instance.status === "Verified")
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
        if (list[i].instance.status === "Verified")
          list1.push(list[i]);
    } else if (filter.status === "Finished"){
      status_flag = true;
      for (i = 0; i < list.length; i++)
        if (list[i].instance.status === "Finished")
          list1.push(list[i]);
    } else if (filter.status === "InProgress"){
      status_flag = true;
      for (i = 0; i < list.length; i++)
        if (list[i].instance.status === "InProgress")
          list1.push(list[i]);
    } else if (filter.status === "Assigned"){
      status_flag = true;
      for (i = 0; i < list.length; i++)
        if (list[i].instance.status === "Assigned")
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
        cycle = my_list[i].instance.cycle.reify();
        obj = my_list[i].instance.cycle_task_group_object;
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
    var filter_task_data = {};
    filter_task_data.list = [];
    var filters = {};
    //find all the filters, filter the existing task_data, don't need to go to the server
    //show the data
    var obj = this.element.find('input[name="object"]').val();
    var wf = this.element.find('input[name="workflow"]').val();
    var status = this.element.find('select[name="status"]').val();
    var overdue = this.element.find('input[type=checkbox].filter-overdue:checked').length;

    //set up task filter
    this.options.task_filter.status = status;
    this.options.task_filter.object = obj;
    this.options.task_filter.workflow = wf;
    this.options.task_filter.overdue = overdue;

    //filter task_data
    this.filter_task_data();

    this.options.context.attr('task_count', this.options.task_data.filtered_list.length);
    this.element.find('ul.task-tree').empty();
    this.insert_options(this.options.task_data, this.options.context.task_view, 'ul.task-tree', true);

    ev.stopPropagation();
  }

  , "input[type=checkbox].show-history change" : function(el, ev) {
    if (this.element.find('input[type=checkbox].show-history:checked').length === 1) {
      this.load_task_with_history();
    } else {
      this.load_my_tasks();
    }
    ev.stopPropagation();
  }

  //Show audits
  , "li.audit-tab click" : function(el, ev) {
    this.element.find('li.task-tab').removeClass('active');
    this.element.find('ul.inline-task-filter').hide();
    this.element.find('ul.task-tree').hide();

    el.addClass('active');

    if (!this.options.show_audit) {
      this.options.show_audit = true;
      this.load_my_audits();
    } else {
      this.element.find('ul.audit-tree').show();
    }
    ev.stopPropagation();
  }

  // Show tasks
  , "li.task-tab click" : function(el, ev) {
    this.element.find('li.audit-tab').removeClass('active');
    this.element.find('ul.audit-tree').hide();

    el.addClass('active');
    this.element.find('ul.inline-task-filter').show();
    this.element.find('ul.task-tree').show();
    ev.stopPropagation();
  }

});

})(this.can, this.can.$);
