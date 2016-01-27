(function (GGRC, Generator) {
  GGRC.Bootstrap.Mockups = GGRC.Bootstrap.Mockups || {};
  GGRC.Bootstrap.Mockups.Workflow = GGRC.Bootstrap.Mockups.Workflow || {};

  GGRC.Bootstrap.Mockups.Workflow.Info = {
    title: "Setup",
    icon: "info-circle",
    template: "/workflow/info.mustache",
    people: {
      "manager": Generator.get("user", 3)
    },
    task_people: {
      "assignee": Generator.get("user", 3),
      "verifier": Generator.get("user", 3)
    },
    mapped: {
      "objects": Generator.create({
        icon: ["objective", "control", "regulation"],
        title: "%title",
        description: "%text",
        state: ["In Progress", "Draft"]
      }, {
        count: 5,
        randomize: ["state", "icon"]
      }),
      "requests": Generator.create({
        icon: "requests",
        title: "%title",
        description: "%text",
        state: ["In Progress", "Draft"]
      }, {
        count: 5,
        randomize: "state"
      }),
      "issues": Generator.create({
        icon: "issue",
        title: "%title",
        description: "%text",
        state: ["In Progress", "Draft"]
      }, {
        count: 5,
        randomize: "state"
      })
    },
  };
})(GGRC || {}, GGRC.Mockup.Generator);
