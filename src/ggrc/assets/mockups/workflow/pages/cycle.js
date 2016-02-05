(function (GGRC, Generator) {
  GGRC.Bootstrap.Mockups = GGRC.Bootstrap.Mockups || {};
  GGRC.Bootstrap.Mockups.Workflow = GGRC.Bootstrap.Mockups.Workflow || {};

  GGRC.Bootstrap.Mockups.Workflow.Workflows = {
    title: "Active Cycles",
    icon: "cycle",
    template: "/workflow/cycle.mustache",
    hide_filter: false,
    children: Generator.get("task")
    // children: [{
    //   title: "My workflow",
    //   type: "workflow",
    //   id: "2",
    //   children: [{
    //     title: "Task Group",
    //     type: "task_group",
    //     icon: "task_group",
    //     id: "23",
    //     children: Generator.get("task")
    //   }]
    // }]
  };
})(GGRC || {}, GGRC.Mockup.Generator);
