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
      hidable: true
    }),
    end_date: Generator.create({
      hidable: true
    }),
    t_description: Generator.create({
      hidable: true
    }),
    t_type: Generator.create({
      hidable: false,
      sidebar: false,
      size: 5
    }),
    select: {
      "type": Generator.create({
        option_text: "%title",
      }, {
        count: 3
      }),
      "frequency": Generator.create({
        option_text: "%title",
      }, {
        count: 5
      })
    },
    // t_type_data: [{
    //     option_text: "Rich text"
    //   }, {
    //     option_text: "Dropdown"
    //   }, {
    //     option_text: "Checkboxes"
    // }],
    t_group: Generator.create({
      hidable: true
    }),
    w_title: Generator.create({
      hidable: true
    }),
    w_desc: Generator.create({
      hidable: true
    }),
    frequency: Generator.create({
      hidable: false,
      sidebar: true,
      size: 6
    }),
    // frequency_data: [{
    //     option_text: "One time"
    //   }, {
    //     option_text: "Weekly"
    //   }, {
    //     option_text: "Monthly"
    //   }, {
    //     option_text: "Quarterly"
    //   }, {
    //     option_text: "Annually"
    // }]
  };
})(GGRC || {}, GGRC.Mockup.Generator);
