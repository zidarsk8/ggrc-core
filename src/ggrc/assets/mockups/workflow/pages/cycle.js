(function (GGRC, Generator) {
  GGRC.Bootstrap.Mockups = GGRC.Bootstrap.Mockups || {};
  GGRC.Bootstrap.Mockups.Workflow = GGRC.Bootstrap.Mockups.Workflow || {};

  GGRC.Bootstrap.Mockups.Workflow.Workflows = {
    title: "Active Cycles",
    icon: "cycle",
    template: "/workflow/cycle.mustache",
    hide_filter: false,
    children: Generator.create({
      title: "%title",
      type: "workflow",
      due_on: '12/31/2017',
      id: "%id",
      children: Generator.create({
        title: "Task Group",
        type: "task_group",
        icon: "task_group",
        id: "%id",
        children: Generator.get("task")
      })
    })
  };
})(GGRC || {}, GGRC.Mockup.Generator);
