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
  }

  , get_widget_view: function(el) {
      var widget_view = $(el)
            .closest('[data-widget-view]').attr('data-widget-view');
      if (widget_view && widget_view.length > 0)
        return GGRC.mustache_path + widget_view;
      else
        return this.options.widget_view;
    }

  , init_menu: function() {
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
        { model_name: 'Process', model_lowercase: 'process', model_plural: 'processes', display_name: 'Processes'},
        { model_name: 'DataAsset', model_lowercase: 'data_asset', model_plural: 'data_assets', display_name: 'Data Assets'},
        { model_name: 'Product', model_lowercase: 'product', model_plural: 'products', display_name: 'Products'},
        { model_name: 'Project', model_lowercase: 'project', model_plural: 'projects', display_name: 'Projects'},
        { model_name: 'Facility', model_lowercase: 'facility', model_plural: 'facilities', display_name: 'Facilities'},
        { model_name: 'Market', model_lowercase: 'market', model_plural: 'markets', display_name: 'Markets'},
        { model_name: 'Issue', model_lowercase: 'issue', model_plural: 'issues', display_name: 'issues'},
        { model_name: 'ControlAssessment', model_lowercase: 'control_assessment',
            model_plural: 'control_assessments', display_name: 'Control Assessments'}
      ];
      this.options.object_menu = object_menu;
    }
  }
});

})(this.can, this.can.$);
