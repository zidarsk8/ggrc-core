(function (GGRC, Generator) {
  GGRC.Bootstrap.Mockups = GGRC.Bootstrap.Mockups || {};
  GGRC.Bootstrap.Mockups.Request = GGRC.Bootstrap.Mockups.Request || {};

  GGRC.Bootstrap.Mockups.Request.Info = {
    title: "Info",
    icon: "grcicon-info",
    template: "/request/info.mustache",
    info_title: "My new request",
    description: Generator.paragraph(7),
    state: "In Progress",
    people_assignee: Generator.users(5),
    people_requester: Generator.users(),
    people_verifier: Generator.users(3),
    created_on: "12/03/14",
    due_on: "12/31/15",
    type_a: "assignee",
    type_r: "requester",
    type_v: "verifier",
    files: Generator.files(8, {sort: "date"}),
    comments: Generator.comments(3, {sort: "date"}),
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
        file_list: Generator.files(2)
      }],
      new_value: [{
        text: "",
        file_list: Generator.files(5)
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
    past_requests: Generator.requests(5)
  };
})(GGRC || {}, GGRC.Mockup.Generator);
