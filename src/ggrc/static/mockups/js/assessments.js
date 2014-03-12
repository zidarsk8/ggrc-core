var Assessment = can.Model.LocalStorage.extend({
},{
  init: function(){
    this.name = "assessments";
    this.on('change', function(ev, prop){
      if(prop === 'text' || prop === 'complete'){
        ev.target.save();
      }
    });
  }
});

var Workflow = can.Model.LocalStorage.extend({
},{
  init: function(){
    this.name = "assessmentWorkflows";
    this.on('change', function(ev, prop){
      if(prop === 'text' || prop === 'complete'){
        ev.target.save();
      }
    });
  }
});

// Init: 
var assessmentList = new Assessment.List({});
if(assessmentList.length === 0){
  new Assessment({
    title: "2014 Google Fiber Assessment",
    program_title: "Google Fiber",
    lead_email: "Cassius Clay",
    start_date: "03/11/2014",
    end_date: "",
    status: "Pending",
    workflow: 0,
  }).save();
}
var workflowList = new Workflow.List({});
if(workflowList.length === 0){
  new Workflow({
    title : "FIBER - Control Testing",
    tasks : [
      "Proof reading",
      "Validate mappings",
      "Validate supporting documents"
    ],
    reviews : [
      {title: "Peer Review", reviewer: "Jonathan Myers"},
      {title: "3rd party review", reviewer: "Cindy Rella"},
      
    ],
    frequency : {
      type: "Annually",
      repeat_day: 24,
      repeat_month: 4
    }
  }).save();
  new Workflow({
    title : "General Walkthrough",
    tasks : [
      "Proof reading",
    ],
    reviews : [
      {title: "Peer Review", reviewer: "Jonathan Myers"},
    ],
    frequency : {
      type: "Annually",
      repeat_day: 24,
      repeat_month: 4
    }
  }).save();
  new Workflow({
    title : "General Testing",
    tasks : [
    ],
    reviews : [
    ],
    frequency : {
      type: "Annually",
      repeat_day: 24,
      repeat_month: 4
    }
  }).save();
  new Workflow({
    title : "General Walkthrough",
    tasks : [
    ],
    reviews : [
    ],
    frequency : {
      type: "Annually",
      repeat_day: 24,
      repeat_month: 4
    }
  }).save();
  new Workflow({
    title : "FED Contract Validation",
    tasks : [
    ],
    reviews : [
    ],
    frequency : {
      type: "Annually",
      repeat_day: 24,
      repeat_month: 4
    }
  }).save();
}

can.Component.extend({
  tag: 'assessments-app',
  scope: {
    assessments: new Assessment.List({}),
    select: function(assessment, el, ev){
      ev.preventDefault();
      $("assessment-app").trigger("selected", assessment);
      $("workflow-app").trigger("selected", assessment);
    },
    equals : function(v){
      return false;
    }
  },
  events: {
    '{Assessment} created' : function(Construct, ev, assessment){
      this.scope.attr('assessments').unshift(assessment);
    }
  }
});

can.Component.extend({
  tag: 'assessment-app',
  scope: {
    assessments : new Assessment.List({}),
    assessment: new Assessment.List({})[0],
    workflow: null,
  },
  events: {
    '{Assessment} created' : function(Custruct, ev, assessment){
      this.scope.attr('assessment', assessment);
    },
    ' selected' : function(el, ev, assessment){
      this.scope.attr('assessment', assessment);
    },
    ' workflow_selected' : function(el, ev, workflow){
      this.scope.attr('workflow', workflow);
    },
  }
});

can.Component.extend({
  tag: 'workflow-app',
  name: 'workflow-app',
  edited: false,
  scope: {
    assessments : new Assessment.List({}),
    assessment: new Assessment.List({})[0],
    workflows : new Workflow.List({}),
    workflow : null,
    workflow_id : 'workflow' in assessment ? assessment.workflow : 0,
  },
  events: {
    '{Assessment} created' : function(Custruct, ev, assessment){
      this.scope.attr('assessment', assessment);
    },
    ' selected' : function(el, ev, assessment){
      this.scope.attr('assessment', assessment);
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
      $("assessment-app").trigger("workflow_selected", this.scope.workflow);
      if(this.scope.workflow.attr('_new')){
        this.scope.workflow.attr('_new', false);
        this.scope.workflow.save();
        
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
    }
  },
  helpers: {
    
    "if_equals": function(val1, val2, options) {
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
    }
  }
});
$("#addAssessmentCreated").on('click', function(ev){
  var attrs = {}, $modal =  $("#newAssessmentStandAlone");
  
  $modal.find('input').each(function(_, e){
    attrs[e.name] = e.value;
  })
  attrs['status'] = 'Pending';
  attrs['workflow'] = 0;
  $modal.modal('hide')
  
  new Assessment(attrs).save();
});
$("#confirmChangeWorkflow").on('click', function(ev){
  ev.preventDefault();
  var id = $("#assessmentWorkflowChoose").val();
  new Workflow.List({}).each(function(v){
    if(v.id == id){
      workflow = v;
    }
  });
  if(id == "new"){
    workflow = new Workflow({_new: true, title: "", tasks: [], reviews: []});
  }
  workflow.confirmed = true;
  $("workflow-app").trigger("workflow_selected", workflow);
  $('#workflowConfirm').modal('hide');
});
$("#cancelChangeWorkflow").on('click', function(ev){
  $("workflow-app").trigger("select_previous", workflow);
});
$("#assessments-lhn").html(can.view("assessments", {}))
$("#assessment-app").html(can.view("assessment", {}))
$("#workflow-app").html(can.view("workflow", {}))