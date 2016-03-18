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
    tasks: Generator.create({
      type: "task",
      title: {
        value: "Simple task",
        hidable: false
      },
      description: {
        value: "Governanceit way sustained for organization. Interests all. Perspective tribe goals. Where policies successful. With regulated coherent. Governance governanceinformation authority body perspective. Respect processes governance regulation eells proposes.",
        hidable: true
      },
      task_type: {
        option: "Rich text",
        value: "Articulated are being already banks deals at differences internet control articulated. As where. Respect on governance. Decision-making term issues. Established found governance. Goal regulators include. Way becht authority interaction postulated in.",
        hidable: true,
        size: 5
      },
      group: {
        value: "Group 007",
        hidable: true
      },
      start_date: {
        value: "22/03/16",
        hidable: false
      },
      end_date: {
        value: "22/03/18",
        hidable: false
      },
      mappedd: {
        objects: Generator.create({
          icon: ['objective', 'control', 'regulation'],
          title: '%title',
          description: '%text',
          state: ['In Progress', 'Draft']
        }, {
          count: 5,
          randomize: ['state', 'icon']
        })
      }
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
    frequency: Generator.create({
      hidable: false,
      size: 6
    }),
    button_draft: "Save draft",
    button_reset: "Don’t save",
    button_active: "Activate"
  };
})(GGRC || {}, GGRC.Mockup.Generator);
