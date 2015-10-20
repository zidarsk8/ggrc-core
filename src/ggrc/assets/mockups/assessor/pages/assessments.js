(function (GGRC, Generator) {
  GGRC.Bootstrap.Mockups = GGRC.Bootstrap.Mockups || {};
  GGRC.Bootstrap.Mockups.Assessor = GGRC.Bootstrap.Mockups.Assessor || {};

  GGRC.Bootstrap.Mockups.Assessor.Assessments = {
    title: "Assessments",
    icon: "grcicon-assessment-color",
    template: "/assessor/assessments.mustache",
    children: [{
      title: "Very first assessment",
      info_title: "Very first assessment",
      description: Generator.paragraph(7),
      state: "In Progress",
      state_color: "inprogress",
      type: "assessment",
      status: "In Progress",
      id: "2",
      files: Generator.get("file", 8, {sort: "date"}),
      comments: Generator.get("comment", 3, {sort: "date"}),
      urls: Generator.get("url", 3),
      created_on: "12/03/14",
      due_on: "12/31/15",
      people: {
        "assignee": Generator.get("user", 5),
        "assessor": Generator.get("user"),
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
      })
    }]
  };
})(GGRC || {}, GGRC.Mockup.Generator);
