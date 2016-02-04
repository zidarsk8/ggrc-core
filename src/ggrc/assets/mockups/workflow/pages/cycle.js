(function (GGRC, Generator) {
  GGRC.Bootstrap.Mockups = GGRC.Bootstrap.Mockups || {};
  GGRC.Bootstrap.Mockups.Workflow = GGRC.Bootstrap.Mockups.Workflow || {};

  GGRC.Bootstrap.Mockups.Workflow.Workflows = {
    title: "Active Cycles",
    icon: "cycle",
    template: "/workflow/cycle.mustache",
    hide_filter: false,
    //children: Generator.get("assessment")
    children: [{
      title: "My workflow",
      info_title: "My workflow",
      description: Generator.paragraph(7),
      notes: Generator.paragraph(9),
      test: Generator.paragraph(11),
      state: {
        title: "In Progress",
        class_name: "inprogress"
      },
      state_color: "inprogress",
      type: "workflow",
      status: "In Progress",
      id: "2",
      comments: Generator.get("comment", 10, {sort: "date"}),
      code: "WORKFLOW-915",
      people: {
        "assignee": Generator.get("user", 5),
        "requester": Generator.get("user"),
        "verifier": Generator.get("user", 3)
      },
      created_on: "12/03/14",
      due_on: "12/31/15",
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
      logs: Generator.create({
        author: "%user",
        timestamp: "%date",
        data: [{
          status: "made changes",
          field: "Comment",
          original: {
            text: "%text"
          },
          changed: {
            text: "%text"
          }
        }, {
          status: "made changes",
          field: "Evidence",
          original: {
            files: []
          },
          changed: {
            files: "%files"
          }
        }, {
          status: "made changes",
          field: "People - Requester",
          original: {
            author: "%user"
          },
          changed: {
            author: "%user"
          }
        }, {
          status: "created request",
          field: ""
        }, {
          status: "made changes",
          field: "Dates - Due on",
          original: {
            text: "%date"
          },
          changed: {
            text: "%date"
          }
        }, {
          status: "made changes",
          field: "Dates - Created on",
          original: {
            text: "%date"
          },
          changed: {
            text: "%date"
          }
        }, {
          status: "made changes",
          field: "Description",
          original: {
            text: "%text"
          },
          changed: {
            text: "%text"
          }
        }]
      }, {
        count: 5,
        randomize: "data"
      }),
      children: [{
        title: "Other title",
        type: "process",
        id: "23"
      }, {
        title: "YOLO",
        type: "issue",
        id: "24"
      }, {
        title: "R U Talking to me",
        type: "system",
        id: "12"
      }]
    }]
  };
})(GGRC || {}, GGRC.Mockup.Generator);
