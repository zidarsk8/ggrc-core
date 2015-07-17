/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

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


  var task_group, object, task;
  for(var i = 0; i < assessmentList.length; i++){
    var assessment = assessmentList[i];
    if(!assessment.people) assessment.attr('people', []);
    if(!assessment.tasks) assessment.attr('tasks', []);
    for(var tg = 0; tg < assessment.task_groups.length; tg++){
      task_group = assessment.task_groups[tg];
      for(var o = 0; o < task_group.objects.length; o++){
        object = task_group.objects[o];
        for(var t = 0; t < object.obj_tasks.length; t++){
          task = object.obj_tasks[t];
          task.attr('actions', new can.List());
        }
      }
    }
    if(!assessment.cycles){
      assessment.attr('cycles', new can.List());
    }
    assessment.save();
  }
}
