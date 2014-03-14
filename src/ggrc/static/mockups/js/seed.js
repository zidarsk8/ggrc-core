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