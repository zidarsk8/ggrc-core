(function (GGRC, Generator) {
  GGRC.Bootstrap.Mockups = GGRC.Bootstrap.Mockups || {};
  GGRC.Bootstrap.Mockups.Assessor = GGRC.Bootstrap.Mockups.Assessor || {};

  GGRC.Bootstrap.Mockups.Assessor.Assessments = {
    title: "Assessments",
    icon: "grcicon-assessment-color",
    template: "/assessor/audit.mustache",
    infopane_template: "/static/mockups/base_templates/info_panel_assessments.mustache",
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
      logs: [{
        type: "requester",
        author: "Jost Novljan",
        log_status: "made changes",
        date: "09/19/2015 03:23:55pm PDT",
        field: "Comment",
        original_value: [{
          text: ""
        }],
        new_value: [{
          text: "See usecase here: https://docs.google.com/document/d/1kU6DgyJBOxbPX5eDhphq97dcMhg-b-LpzTJT27XlHYk/edit#heading=h.9wrhlxa3ye2d."
        }]
      }, {
        type: "verifier",
        author: "Prasanna V.",
        log_status: "made changes",
        date: "09/19/2015 05:31:02am PDT",
        field: "Comment",
        original_value: [{
          text: ""
        }],
        new_value: [{
          text: "Curabitur nisl diam, blandit in luctus ac, eleifend quis libero. Morbi in lobortis risus. Vestibulum congue dictum finibus."
        }]
      }, {
        type: "assignee",
        author: "Albert Chan",
        log_status: "made changes",
        date: "09/18/2015 05:31:02am PDT",
        field: "People - Requester",
        original_value: [{
          text: "Ella Cinder"
        }],
        new_value: [{
          text: "Josh Smith"
        }]
      }, {
        type: "assignee",
        author: "Albert Chan",
        log_status: "made changes",
        date: "09/14/2015 05:31:02am PDT",
        field: "Dates - Due on",
        original_value: [{
          text: "12/31/14"
        }],
        new_value: [{
          text: "12/31/15"
        }]
      }, {
        type: "assignee",
        author: "Albert Chan",
        log_status: "made changes",
        date: "09/12/2015 05:31:02am PDT",
        field: "Dates - Created on",
        original_value: [{
          text: "12/03/13"
        }],
        new_value: [{
          text: "12/03/14"
        }]
      }, {
        type: "assignee",
        author: "Albert Chan",
        log_status: "made changes",
        date: "09/08/2015 05:31:02am PDT",
        field: "Evidence",
        original_value: [{
          text: "",
          file_list: Generator.get("file", "random")
        }],
        new_value: [{
          text: "",
          file_list: Generator.get("file", "random")
        }]
      }, {
        type: "assignee",
        author: "Albert Chan",
        log_status: "made changes",
        date: "09/04/2015 3:30:00pm PDT",
        field: "Description",
        original_value: [{
          text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vitae ante dapibus lacus dictum vestibulum. Nullam finibus semper convallis. Ut libero mauris, viverra nec augue eget, congue viverra felis. Aenean ut arcu vel tortor rhoncus dictum id vel urna."
        }],
        new_value: [{
          text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vitae ante dapibus lacus dictum vestibulum. Nullam finibus semper convallis. Ut libero mauris, viverra nec augue eget, congue viverra felis. Aenean ut arcu vel tortor rhoncus dictum id vel urna. Sed a enim laoreet diam lacinia euismod."
        }]
      }, {
        type: "assignee",
        author: "Albert Chan",
        log_status: "made changes",
        date: "09/03/2015 07:15:23am PDT",
        field: "Description",
        original_value: [{
          text: "Cras vitae ante dapibus lacus dictum vestibulum. Nullam finibus semper convallis. Ut libero mauris, viverra nec augue eget, congue viverra felis. Aenean ut arcu vel tortor rhoncus dictum id vel urna."
        }],
        new_value: [{
          text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vitae ante dapibus lacus dictum vestibulum. Nullam finibus semper convallis. Ut libero mauris, viverra nec augue eget, congue viverra felis. Aenean ut arcu vel tortor rhoncus dictum id vel urna."
        }]
      }, {
        type: "assignee",
        author: "Albert Chan",
        log_status: "made changes",
        date: "09/03/2015 05:31:02am PDT",
        field: "Description",
        original_value: [{
          text: ""
        }],
        new_value: [{
          text: "Cras vitae ante dapibus lacus dictum vestibulum. Nullam finibus semper convallis. Ut libero mauris, viverra nec augue eget, congue viverra felis. Aenean ut arcu vel tortor rhoncus dictum id vel urna."
        }]
      }, {
        type: "assignee",
        author: "Albert Chan",
        log_status: "made changes",
        date: "09/02/2015 09:00:12am PDT",
        field: "State",
        original_value: [{
          text: "Draft"
        }],
        new_value: [{
          text: "In progress"
        }]
      }, {
        type: "assignee",
        author: "Albert Chan",
        log_status: "created request",
        date: "09/01/2015 11:07:35am PDT",
        field: "",
        original_value: [{
          text: ""
        }],
        new_value: [{
          text: ""
        }]
      }],
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
