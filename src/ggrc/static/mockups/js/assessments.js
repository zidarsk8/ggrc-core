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
      console.log(v)
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
  },
  events: {
    '{Assessment} created' : function(Custruct, ev, assessment){
      this.scope.attr('assessment', assessment);
    },
    ' selected' : function(el, ev, assessment){
      this.scope.attr('assessment', assessment);
    }
  }
});

can.Component.extend({
  tag: 'workflow-app',
  name: 'workflow-app',
  scope: {
    assessments : new Assessment.List({}),
    assessment: new Assessment.List({})[0],
    workflows : new Workflow.List({}),
    workflow : null,
    workflow_id : 'workflow' in assessment ? assessment.workflow : 0
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
      this.scope.attr('workflow', workflow);
    },
    '#addTask click' : function(){
      this.scope.attr('workflow').tasks.push('');
    },
    '#addReview click' : function(){
      var review = this.scope.attr('workflow');
      review.reviews.push({title: "", reviewer: ""});
      review.save();
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
$("#assessments-lhn").html(can.view("assessments", {}))
$("#assessment-app").html(can.view("assessment", {}))
$("#workflow-app").html(can.view("workflow", {}))