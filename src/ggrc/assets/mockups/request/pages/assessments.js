(function (GGRC, Generator) {
  GGRC.Bootstrap.Mockups = GGRC.Bootstrap.Mockups || {};
  GGRC.Bootstrap.Mockups.Request = GGRC.Bootstrap.Mockups.Request || {};

  GGRC.Bootstrap.Mockups.Request.Assessments = {
    title: "Assessments",
    icon: "grcicon-assessment-color",
    template: "/request/audit.mustache",
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
      people_assignee: Generator.get("user", 5),
      people_assessor: Generator.get("user"),
      people_verifier: Generator.get("user", 3),
      created_on: "12/03/14",
      due_on: "12/31/15",
      type_a: "assignee",
      type_s: "assessor",
      type_v: "verifier",
      mapped_objects: [{
        icon: "objective",
        title: "090.7068 objective 1",
        state: "Draft",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer bibendum sem id lectus porta, eu rutrum nunc commodo."
      }, {
        icon: "control",
        title: "Access to the Private Network with expired Key v0906984",
        state: "In Progress",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer bibendum sem id lectus porta, eu rutrum nunc commodo."
      }, {
        icon: "regulation",
        title: "a regulation object",
        state: "In Progress",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer bibendum sem id lectus porta, eu rutrum nunc commodo."
      }],
      mapped_objects_requests: [{
        icon: "request",
        title: "My new request",
        state: "In Progress",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer bibendum sem id lectus porta, eu rutrum nunc commodo."
      }, {
        icon: "request",
        title: "Simple Request for Programs",
        state: "Draft",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer bibendum sem id lectus porta, eu rutrum nunc commodo."
      }, {
        icon: "request",
        title: "Request made for Sections inspection",
        state: "Draft",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer bibendum sem id lectus porta, eu rutrum nunc commodo."
      }],
      mapped_objects_issues: [{
        icon: "issue",
        title: "090.7068 issue 1",
        state: "Draft",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer bibendum sem id lectus porta, eu rutrum nunc commodo."
      }, {
        icon: "issue",
        title: "Access to the Private Network with expired Key v0906984",
        state: "In Progress",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer bibendum sem id lectus porta, eu rutrum nunc commodo."
      }, {
        icon: "issue",
        title: "a object under issue",
        state: "In Progress",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer bibendum sem id lectus porta, eu rutrum nunc commodo."
      }],
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
      past_requests: Generator.get("request", 5),
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
    }, {
      title: "Simple Request for Programs",
      type: "issue",
      id: "3",
      status: "Draft",
      children: []
    }, {
      title: "Request made for Sections inspection",
      type: "audit",
      id: "5",
      status: "Draft",
      children: [{
        title: "Other title",
        type: "process",
        id: "63"
      }, {
        title: "YOLO",
        type: "issue",
        id: "344"
      }, {
        title: "R U Talking to me",
        type: "system",
        id: "342"
      }, {
        title: "Other title",
        type: "process",
        id: "33"
      }, {
        title: "YOLO",
        type: "issue",
        id: "54"
      }, {
        title: "R U Talking to me",
        type: "system",
        id: "62"
      }]
    }]
  };
})(GGRC || {}, GGRC.Mockup.Generator);
