Mustache.registerHelper("if_equals", function(val1, val2, options) {
  var that = this, _val1, _val2;
  function exec() {
    if(_val1 == _val2) return options.fn(options.contexts);
    else return options.inverse(options.contexts);
  }
    if(typeof val1 === "function") {
      if(val1.isComputed) {
        val1.bind("change", function(ev, newVal, oldVal) {
          _val1 = newVal;
          return exec();
        });
      }
      _val1 = val1.call(this);
    } else {
      _val1 = val1;
    }
    if(typeof val2 === "function") {
      if(val2.isComputed) {
        val2.bind("change", function(ev, newVal, oldVal) {
          _val2 = newVal;
          exec();
        });
      }
      _val2 = val2.call(this);
    } else {
      _val2 = val2;
    }

  return exec();
});

var Assessment = can.Model.LocalStorage.extend({
},{
  init: function(){
    this.name = "workflow";
    this.on('change', function(ev, prop){
      if(prop === 'text' || prop === 'complete'){
        ev.target.save();
      }
    });
  },
});

var Workflow = can.Model.LocalStorage.extend({
},{
  init: function(){
    this.name = "assessmentWorkflows-v3";
    this.on('change', function(ev, prop){
      if(prop === 'text' || prop === 'complete'){
        ev.target.save();
      }
    });
  }
});

var Task = can.Model.LocalStorage.extend({
},{
  init: function(){
    this.name = "task";
    this.on('change', function(ev, prop){
      if(prop === 'text' || prop === 'complete'){
        ev.target.save();
      }
    });
  }
});


var ProgramList = [{
  name: 'program',
  title: 'Google Fiber',
  description: '<p><b>ISO/IEC 27001</b>, part of the growing&nbsp;<a href="http://en.wikipedia.org/wiki/ISO/IEC_27000-series">ISO/IEC 27000 family of standards</a>, is an&nbsp;<a href="http://en.wikipedia.org/wiki/Information_security_management_system">information security management system</a>&nbsp;(ISMS) standard published in October 2005 by the&nbsp;<a href="http://en.wikipedia.org/wiki/International_Organization_for_Standardization">International Organization for Standardization</a>&nbsp;(ISO) and the&nbsp;<a href="http://en.wikipedia.org/wiki/International_Electrotechnical_Commission">International Electrotechnical Commission</a>&nbsp;(IEC). Its full name is&nbsp;<i>ISO/IEC 27001:2005 – Information technology – Security techniques – Information security management systems – Requirements</i>.</p><p>ISO/IEC 27001 formally specifies a management system that is intended to bring information security under explicit management control. Being a formal specification means that it mandates specific requirements. Organizations that claim to have adopted ISO/IEC 27001 can therefore be formally audited and certified compliant with the standard (more below).</p>',
  owner: 'liz@reciprocitylbas.com',
  contact: 'ken@reciprocitylbas.com'
}];
var Objects = {
  controls: [
    {type: "control", name: "Secure Backups"},
    {type: "control", name: "Data Storage"},
    {type: "control", name: "Password Security"},
    {type: "control", name: "Access Control"},
    {type: "control", name: "Stability and Perpetuability"}
  ],
  objectives: [
    {type: "objective", name: "Establish a schedule"}
  ],
  standards: [
    {type: "standard", name: "ASHRAE 90.1"}
  ],
  policies: [
    {type: "policy", name: "Probationary Terms"},
    {type: "policy", name: "Medical Leave"}
  ],
  contracts: [
    {type: "contract", name: "Master Service Agreement"},
    {type: "contract", name: "SaaS Vendor Contract"},
    {type: "contract", name: "Company X Contract"}
  ],
  regulations: [
    {type: "regulation", name: "SOX"},
    {type: "regulation", name: "PCI DSS v2.0"}
  ]
}



var taskList = new Task.List({});
var assessmentList = new Assessment.List({});
create_seed();


// LHN
can.Component.extend({
  tag: 'lhn-app',
  scope: {
    assessments: assessmentList,
    programs: ProgramList,
    tasks: taskList,
    select: function(object, el, ev){
      ev.preventDefault();
      $("tree-app").trigger("selected", object);
      $("workflow-modal").trigger("selected", object);
      $("workflow").trigger("selected", object);
      $("task").trigger("selected", object);
      resize_areas();
    },
  },
  events: {
    '{Assessment} created' : function(Construct, ev, assessment){
      this.scope.attr('assessments').unshift(assessment);
    },
    '{Task} created' : function(Construct, ev, tasks){
      this.scope.attr('tasks').unshift(tasks);
    }
  }
});

can.Component.extend({
  tag: 'tree-app',
  scope: {
    object: ProgramList[0]//assessmentList[0]
  },
  events: {
    ' selected' : function(el, ev, object){
      this.scope.attr('object', object);
    }
  },
  helpers: {

    "hide_class": function(val, object, options) {
      var name = object().name;
      if(name === val)
        return '';
      else
        return 'hide';
    }
  }
});

// Workflow Tree
can.Component.extend({
  tag: 'workflow',
  init: function(){
    var that = this;
    $(function(){
      that.scope.initAutocomplete();
    })
  },
  scope: {
    assessments : assessmentList,
    assessment: assessmentList[0],
    objects : [],
    filter_list : [{value: assessmentList[0].program_title}],
    set_fields : function(assessment){
      this.attr('filter_list', [{value: assessment.program_title}]);
      this.attr('assessment', assessment);
    },
    initAutocomplete : function(){
      $( ".date" ).datepicker();
      var lists = {
        objects : $.map(this.assessment.objects, function(o){
          return o.name;
        }),
        people : [
          "Vladan Mitevski",
          "Predrag Kanazir",
          "Dan Ring",
          "Silas Barta",
          "Cassius Clay"
        ],
        mapped_people : [
          "Cassius Clay",
          "Dan Ring",
          "Predrag Kanazir",
        ],
        tasks: [
          "Proof Reading",
          "Validate Mappings",
          "Peer Review"
        ]
      }
      $('.autocomplete').each(function(i,el){
        var $el = $(el)
          , autocomplete_type = $el.data('autocomplete-type')
          , type = autocomplete_type || $el.data('type')
        $el.autocomplete({
          source : lists[type],
          close: function( event, ui ) {$el.trigger('change')}
        })
      });
    },
  },
  events: {
    '{Assessment} created' : function(){this.scope.set_fields(arguments[2])},
    '{Assessment} updated' : function(){
      this.scope.initAutocomplete();
    },
    ' selected' : function(){this.scope.set_fields(arguments[2])},
    "a#objectReview click" : function(el, ev){
      var type = $("#objects_type").val().toLowerCase()
        , that = this
        , objects = this.scope.assessment.objects;
      this.scope.attr('objects', $.map(Objects[type], function(o){

        for(var i = 0; i < objects.length; i++){
          if(o.type === objects[i].type && o.name === objects[i].name){
            return;
          }
        }
        return o;
      }));
      $('.results .info').css('display', 'none');
    },
    "a#filterTrigger,a#filterTriggerFooter click" : function(el, ev){
      this.scope.attr('filter', true);
      this.scope.attr('objects', []);
      this.scope.assessment.attr('objects', []);
    },
    "a#addSelected click" : function(el, ev){
      var scope = this.scope
        , assessment = scope.assessment
        , selected = $('.object-check-single').map(function(_, v){return v.checked;})
        , filtered = []
        , i;
      scope.objects.each(function(v,i){
        if(selected[i]) assessment.objects.push(v);
      });

      if(assessment.attr('started')){
        this.scope.initObjects();
      }
      assessment.save();
      scope.attr('objects', []);
      this.scope.set_fields(assessment);
    },
    "#objectAll click": function(el){
      var $el = $(el)
        , $check = $(this.element).find('.object-check-single');
      $check.prop('checked', $el.prop('checked'));
      $check.each(function(i, c){
        if($el.is(':checked')) {
          $(c).closest('.tree-item').removeClass('disabled');
        } else {
          $(c).closest('.tree-item').addClass('disabled');
        }
      })

    },
    "#addFilterRule click": function(){
      this.scope.filter_list.push([{value: ""}]);
    },
    ".addEntry click" : function(el){
      var object_id = el.closest('.object-top').data('index')
        , task_id = el.data('index')
        , textarea = el.parent().find('textarea').first()
        , value = textarea.val()
        , objects = el.data('objects')
        , list = objects === 'tasks' ? 'entries' : 'notes' ;
      el.closest(".add-entry").hide();
      el.parent().next().show();
      this.scope.assessment.objects[object_id][objects][task_id][list].push({content: value});
      this.scope.assessment.save();
      textarea.val('');
    },
    ".startObjectNow click" : function(el){
      var object_id = el.closest('.object-top').data('index')
        , type = el.data('type')
        , id = el.data('id')
        , status = el.data('status')
        , can_finish = true
        , state = type === 'tasks' ? 'task_state' : 'review_state'
        , object = this.scope.assessment.objects[object_id]
        ;
      if(type === 'object')
        object.attr('status', status);
      else{
        object[type][id].attr(state, status);
      }
      // Check if the finish button can be enabled:
      object.tasks.each(function(v){
        if(v.task_state !== 'rq-accepted'){
          can_finish = false;
        }
      });
      object.reviews.each(function(v){
        if(v.review_state !== 'rq-responded'){
          can_finish = false;
        }
      });
      object.attr('can_finish', can_finish)
      this.scope.assessment.save();
    },
    ".remove_filter click" : function(el){
      this.scope.filter_list.splice(el.data('index'), 1);
    },
    ".reset_filter click" : function(){
      this.scope.attr('filter_list', [{value: this.scope.assessment.program_title}]);
    },
    ".show_review click" : function(el){
      $(el).parent().hide();
      $(el).parent().prev().show();
    },

    // Task groups:
    "#addTaskGroup click" : function(){
      var title = $("#new_object_name").val()
        , assignee = $("#new_task_assignee").val()
        , assessment = this.scope.assessment;
      if(!assessment.task_groups){
        assessment.attr('task_groups', []);
      }
      assessment.task_groups.push({
        title: title,
        description: "",
        assignee: assignee,
        objects: [],
        tasks: [],
        end_date: "",
        taskLock: false
      });
      assessment.save();
    },
    ".removeTaskGroup click" : function(el, ev){
      var assessment = this.scope.assessment
        , index = $(el).data('index')
        ;
      assessment.task_groups.splice(index, 1);
      assessment.save();
    },
    ".saveTaskGroupField change" : function(el, ev){
      var assessment = this.scope.assessment
        , $el = $(el)
        , index = $el.data('index')
        , field = $el.data('field')
        ;
      assessment.task_groups[index].attr(field, $el.val());
      assessment.save();
    },
    ".toggleClosest click" : function(el, ev){
      var $el = $(el)
        , hide = $el.parent()
        , show = $el.parent().siblings()
      hide.hide();
      show.show();
    },
    ".addTrigger click" : function(el, ev){
      var $el = $(el)
        , assessment = this.scope.assessment
        , index = $el.data('index')
        , type = $el.data('type')
        ;
      if($el.hasClass('disabled')) return;
      assessment.task_groups[index][type].push({title: ""});
      assessment.save();
    },
    ".deleteTrigger click" : function(el, ev){
      var $el = $(el)
        , assessment = this.scope.assessment
        , index = $el.data('index')
        , workflowIndex = $el.closest('ul').data('index')
        , type = $el.data('type')
        ;
      if($el.hasClass('disabled')) return;
      assessment.task_groups[workflowIndex][type].splice(index, 1);
      assessment.save();
    },
    ".taskLock change" : function(el, ev){
      var $el = $(el)
        , index = $el.data('index')
        , assessment = this.scope.assessment
        , task_group = assessment.task_groups[index]
        ;
      task_group.attr('taskLock', $el.is(':checked'));
      assessment.save();
    },
    ".editTitle change" : function(el, ev){
      var $el = $(el)
        , assessment = this.scope.assessment
        , index = $el.data('index')
        , workflowIndex = $el.closest('ul').data('index')
        , type = $el.data('type')
        ;
      if($el.hasClass('disabled')) return;
      assessment.task_groups[workflowIndex][type][index].attr('title', $el.val());
      assessment.save();
    }
  }
});

can.Component.extend({
  tag: 'task',
  scope: {
    task: taskList[0],
  },
  events: {
    '{Task} created' : function(){
      this.scope.attr('task', arguments[2]);
    },
    '{Task} updated' : function(){
    },
    ' selected' : function(){
      this.scope.attr('task', arguments[2]);
    },
  }
})

can.Component.extend({
  tag: 'workflow-modal',
  scope: {
    assessment: assessmentList[0],
    new_form: false,
    currentUser : 'user@example.com',
    set_fields : function(assessment){
      this.attr('filter_list', [{value: assessment.program_title}]);
      this.attr('assessment', assessment);
      this.validateForm();
    },
    "new" : function(val, val_old){
      this.validateForm();
      if(this.attr('new_form')) return arguments.length === 3 ? val_old() : '';
      return val();
    },
    validateForm : function(){
      var $modal = $("#editAssessmentStandAlone")
        , required_fields = $modal.find('input.required')
        , $save_button = $("#saveAssessment")
        , empty_fields = $.map(required_fields, function(f){
            if($(f).val()){
              return f;
            }
          })
      if(required_fields.length === empty_fields.length){
        $save_button.removeClass('disabled');
      }
      else{
        $save_button.addClass('disabled');
      }
    }
  },
  events:{
    '{window} click' : function(el, ev){
      if(!$(ev.target).hasClass('show-workflow-modal')) return;
      this.scope.attr('new_form', $(ev.target).data('new'));
    },
    'a#saveAssessment click' : function(el, ev){
      var $modal = $('#editAssessmentStandAlone')
        , assessment = this.scope.attr('new_form') ? new Assessment({}) : this.scope.attr('assessment');

      if($(el).hasClass('disabled'))return;
      $modal.find('input').each(function(_, e){
        assessment.attr(e.name, e.value);
      });
      $modal.find('textarea').each(function(_, e){
        assessment.attr(e.name, $(e).val());
      });
      $modal.modal('hide');
      if(typeof assessment.objects === 'undefined'){
        assessment.attr('objects', []);
      }
      if(typeof assessment.task_groups === 'undefined'){
        assessment.attr('task_groups', []);
      }
      assessment.save();
      $("tree-app").trigger("selected", this.scope.assessment);

    },
    '{Assessment} created' : function(){
      this.scope.attr('assessment', arguments[2]);
    },
    ' selected' : function(){
      this.scope.attr('assessment', arguments[2]);
    },
    'input,textarea change' : function(){
      this.scope.validateForm();
    },
    'input,textarea keyup' : function(){
      this.scope.validateForm();
    }
  }
});

var modal = can.Component.extend({
  tag: 'task-modal',
  scope: {
    task: taskList[0],
    new_form: false,
    currentUser : 'user@example.com',
    "new" : function(val, val_old){
      if(this.attr('new_form')) return arguments.length === 3 ? val_old() : '';
      return val();
      this.validateForm();
    },
    validateForm : function(){
      var $modal = $("#newTask")
        , required_fields = $modal.find('input.required')
        , $save_button = $("#addTask")
        , empty_fields = $.map(required_fields, function(f){
            if($(f).val()){
              return f;
            }
          })
      if(required_fields.length === empty_fields.length){
        $save_button.removeClass('disabled');
      }
      else{
        $save_button.addClass('disabled');
      }
    }
  },
  events:{
    '{window} click' : function(el, ev){
      this.scope.validateForm();
      if(!$(ev.target).hasClass('show-task-modal')) return;
      this.scope.attr('new_form', $(ev.target).data('new'));
    },
    'a#addTask click' : function(el, ev){
      var $modal = $('#newTask')
        , task = this.scope.attr('new_form') ? new Task({}) : this.scope.attr('task');

      if($(el).hasClass('disabled'))return;
      $modal.find('input').each(function(_, e){
        task.attr(e.name, e.value);
      });
      $modal.find('textarea').each(function(_, e){
        task.attr(e.name, $(e).val());
      });
      $modal.modal('hide');
      task.save();
      $("tree-app").trigger("selected", this.scope.task);

    },
    '{Task} created' : function(){
      this.scope.attr('task', arguments[2]);
    },
    ' selected' : function(){
      this.scope.attr('task', arguments[2]);
      this.scope.validateForm();
    },
    'input,textarea change' : function(){
      this.scope.validateForm();
    },
    'input,textarea keyup' : function(){
      this.scope.validateForm();
    }
  }
});

can.Component.extend({
  init: function() {
    $("#addTask").on('click', function(){
      new Task({
        title: $("#task-title").val(),
        description: "",
        end_date: ""
      }).save();
      $("#newTask").modal('hide');
    });
  },
  tag: 'workflow-app',
  name: 'workflow-app',
  edited: false,
  scope: {
    assessments : assessmentList,
    assessment: assessmentList[0],
    workflows : new Workflow.List({}),
    workflow : null,
    objectsFilter : false,
    //workflow_id : 'workflow' in assessment ? assessment.workflow : 0,
  },
  events: {
    '{Assessment} created' : function(Custruct, ev, assessment){
      this.scope.attr('assessment', assessment);
    },
    ' selected' : function(el, ev, assessment){
      this.scope.attr('assessment', assessment);
      this.scope.attr('objectsFilter', false);
      this.scope.attr('workflow_id', 'workflow' in assessment ? assessment.workflow : 0)
    },
    ' workflow_selected' : function(el, ev, workflow){
      var show_modal = this.edited;
      this.edited = false;
      if(show_modal && !workflow.confirmed){
        $('#workflowConfirm').modal('show');
        return;
      }
      this.scope.attr('workflow_id', typeof workflow !== "undefined" ? workflow.id : 0);
      this.scope.attr('workflow', workflow);
    },
    ' select_previous' : function(){
      this.edited = true;
      $("#assessmentWorkflowChoose > option[value='"+this.scope.workflow_id+"']").attr('selected', 'selected');
    },
    'input change' : function(el){
      this.edited = true;
    },
    '.add click' : function(el){
      var type = el.data('type')
        , workflow = this.scope.attr('workflow');
      workflow[type].push(type == "tasks" ? "" : {title: "", reviewer: ""});
      this.edited = true;
      //workflow.save();
    },
    '.delete click' : function(el, ev){
      ev.preventDefault();
      var type = el.data('type')
        , index = el.data('index')
        , workflow = this.scope.attr('workflow');

      workflow[type].splice(index, 1);
      this.edited = true;
      //workflow.save()
    },
    "a#addWorkflowNow click" : function(el, ev){
      var workflow = this.scope.workflow;
      $("tree-app").trigger("workflow_selected", this.scope.workflow);
      if(typeof workflow !== 'undefined' && workflow.attr('_new')){
        workflow.attr('_new', false);
        workflow.save();
      }

      $("#setupWorkflow").modal('hide');
    },
    '.update change' : function(el, ev){
      var model = el.data('model')
        , type = el.data('type')
        , index = el.data('index')
        , workflow = this.scope.attr('workflow');
      if(model === "tasks"){
        workflow[model][index] = el.val();
      }
      else if(model === "title"){

        workflow.attr(model, el.val());
      }
      else{
        workflow[model][index].attr(type, el.val());
      }
    },
  }
});
$("#cancelChangeWorkflow").on('click', function(ev){
  $("workflow-app").trigger("select_previous", workflow);
});
$("#lhn-automation").html(can.view("/static/mockups/mustache/v1.1/lhn.mustache", {}))
$("#tree-app").html(can.view("/static/mockups/mustache/v1.1/tree.mustache", {}))
$("#workflow-app").html(can.view("/static/mockups/mustache/workflow.mustache", {}))
$("#workflow").html(can.view("/static/mockups/mustache/v1.1/assessment.mustache", {}));
$("#task").html(can.view("/static/mockups/mustache/v1.1/task.mustache", {}));
$("#workflow-modal").html(can.view("/static/mockups/mustache/v1.1/workflow-modal.mustache", {}));
$("#task-modal").html(can.view("/static/mockups/mustache/v1.1/task-modal.mustache", {}));
