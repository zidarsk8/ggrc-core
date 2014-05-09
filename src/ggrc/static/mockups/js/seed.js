function create_seed(){
  if(assessmentList.length === 0){
    new Assessment({
      title: "2014 Google Fiber Assessment",
      program_title: "Google Fiber",
      description: "Initial control setup confirmation.",
      lead_email: "Cassius Clay",
      end_date: "09/06/2014",
      status: "Future",
      workflow: 0,
      objects: [],
      task_groups: [],
    }).save();
  }
  if(taskList.length === 0){
    new Task({
      title: "Peer Review",
      description: "",
      end_date: "",
    }).save();
    new Task({
      title: "Control Checkup",
      description: "",
      end_date: ""
    }).save();
  }
  var workflowList = new Workflow.List({});
  assessmentList = new Assessment.List({});
  taskList = new Task.List({});

  for(var i = 0; i < assessmentList.length; i++){
    var assessment = assessmentList[i];
    if(!assessment.people) assessment.attr('people', []);
    if(!assessment.tasks) assessment.attr('tasks', []);
    assessment.save();
  }
}
