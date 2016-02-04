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
    t_title: Generator.create({
      hidable: false
    }),
    start_date: Generator.create({
      hidable: false
    }),
    end_date: Generator.create({
      hidable: false
    }),
    t_description: Generator.create({
      hidable: true
    }),
    task: Generator.create({
      object_type: "task"
    }),
    t_type: Generator.create({
      hidable: true,
      sidebar: false,
      size: 5
    }),
    frequency_select: Generator.create({
      data: [{
        option_text: "One time",
        value: "one_time"
      }, {
        option_text: "Weekly",
        value: "weekly"
      }, {
        option_text: "Monthly",
        value: "monthly"
      }, {
        option_text: "Quarterly",
        value: "quarterly"
      }, {
        option_text: "Annually",
        value: "annually"
      }]
    }),
    type_select: Generator.create({
      data: [{
        option_text: "Rich text",
        value: "text"
      }, {
        option_text: "Dropdown",
        value: "menu"
      }, {
        option_text: "Checkboxes",
        value: "checkbox"
      }]
    }),
    t_group: Generator.create({
      hidable: true
    }),
    w_title: Generator.create({
      hidable: false
    }),
    w_desc: Generator.create({
      hidable: true
    }),
    frequency: Generator.create({
      hidable: false,
      sidebar: true,
      size: 6
    }),
    button_draft: "Save draft",
    button_active: "Activate"
  };
})(GGRC || {}, GGRC.Mockup.Generator);
