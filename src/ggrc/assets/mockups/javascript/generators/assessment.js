/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE- 0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/


(function (GGRC, _, Generator) {
  Generator.assessment = function () {
    return {
      title: Generator.title(),
      info_title: Generator.title(),
      description: Generator.paragraph(7),
      type: "assessment",
      state: {
        title: "In Progress",
        class_name: "inprogress"
      },
      state_color: "inprogress",
      status: "In Progress",
      id: "2",
      comments: Generator.get("comment", 10, {sort: "date", types: ["assignee", "assessor", "verifier"]}),
      urls: Generator.get("url", 3),
      people: {
        "assignee": Generator.get("user", 5),
        "assessor": Generator.get("user"),
        "verifier": Generator.get("user", 3)
      },
      created_on: Generator.get_date({year: 2015}),
      due_on: Generator.get_date({year: 2015}),
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
      past_requests: Generator.get("request", 5)
    };
  };
})(this.GGRC, this._, GGRC.Mockup.Generator);
