/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

$(document).ready(function() {

  can.Component.extend({
    tag: "audit-info",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-info").html(can.view("/static/mockups/mustache/audit-revamp/info.mustache",{}));

  can.Component.extend({
    tag: "control",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-control").html(can.view("/static/mockups/mustache/audit-revamp/control.mustache",{}));

  can.Component.extend({
    tag: "ca",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-ca").html(can.view("/static/mockups/mustache/audit-revamp/control-assessments.mustache",{}));

  can.Component.extend({
    tag: "people",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-people").html(can.view("/static/mockups/mustache/audit-revamp/people.mustache",{}));

  can.Component.extend({
    tag: "program",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-program").html(can.view("/static/mockups/mustache/audit-revamp/program.mustache",{}));

  can.Component.extend({
    tag: "requests",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-requests").html(can.view("/static/mockups/mustache/audit-revamp/requests.mustache",{}));

  can.Component.extend({
    tag: "complete",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-complete").html(can.view("/static/mockups/mustache/audit-revamp/complete.mustache",{}));

  can.Component.extend({
    tag: "issues",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-issues").html(can.view("/static/mockups/mustache/audit-revamp/issues.mustache",{}));

  can.Component.extend({
    tag: "issue-info",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-issue-info").html(can.view("/static/mockups/mustache/audit-revamp/issue-info.mustache",{}));

  can.Component.extend({
    tag: "issue-ca",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-issue-ca").html(can.view("/static/mockups/mustache/audit-revamp/issue-ca.mustache",{}));

  can.Component.extend({
    tag: "issue-audit",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-issue-audit").html(can.view("/static/mockups/mustache/audit-revamp/issue-audit.mustache",{}));

  can.Component.extend({
    tag: "issue-controls",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-issue-controls").html(can.view("/static/mockups/mustache/audit-revamp/issue-controls.mustache",{}));

  can.Component.extend({
    tag: "issue-program",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-issue-program").html(can.view("/static/mockups/mustache/audit-revamp/issue-program.mustache",{}));

  can.Component.extend({
    tag: "issue-workflow",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-issue-workflow").html(can.view("/static/mockups/mustache/audit-revamp/issue-workflow.mustache",{}));

  can.Component.extend({
    tag: "issue-workflow-tasks",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-issue-workflow-tasks").html(can.view("/static/mockups/mustache/audit-revamp/issue-workflow-tasks.mustache",{}));

  function innerNavTrigger() {
    var $this = $(this),
        $allList = $this.closest(".nav").children("li"),
        $list = $this.closest("li"),
        aId = $this.attr("href"),
        $element = $("div"+aId);

    $allList.removeClass('active');
    $list.addClass('active');

    $(".object-wrap").hide();
    $(".object-wrap"+aId).show();
  }

  function personRole() {
    $('#PersonRole').modal('hide');
    $('#personAuth').html('Audit member');
    $('#personAuth2').html('Audit member');
  }

  function generateCA() {
    $("#ca .content").find(".tree-structure").find(".tree-item").show();
    $("#CaAdded").hide();
    $("#ca .content").find(".tree-structure").find(".zero-state").hide();
    $("#CACounter").html("4");
  }

  function reviewWorkflow() {
    $("#issueWorkflow").modal("hide");
    $("#workflowWrap").show();
    $(".nav li").removeClass("active");
    $("#workflowTaskWrap").show().addClass("active");
    window.location.href = '#issue-workflow-tasks';
    $(".object-wrap").hide();
    $(".object-wrap-issue-workflow-tasks").show();
  }

  function startTask() {
    $("#startTask").hide();
    $("#finishTask").show();
    $("#undoTask").show();
    $("#taskStatus").removeClass("status-assigned");
    $("#taskStatus").addClass("status-inprogress");
    $("#issueStatus").addClass("status-inprogress");
    $("#taskStatusMessage")
      .removeClass("state-assigned")
      .addClass("state-inprogress")
      .html("In progress");
    $("#issueStatusMessage").html("In progress");
  }

  function finishTask() {
    $("#finishTask").hide();
    $("#approveTask").show();
    $("#declineTask").show();
    $("#taskStatus").removeClass("status-inprogress");
    $("#taskStatus").addClass("status-finished");
    $("#issueStatus").removeClass("status-inprogress");
    $("#issueStatus").addClass("status-finished");
    $("#undoTask").hide();
    $("#taskStatusMessage")
      .removeClass("state-inprogress")
      .addClass("state-finished")
      .html("Finished");
    $("#issueStatusMessage").html("Finished");
    $("#reviewTrigger").hide();
    $("#reviewChoice").show();
  }

  function approveReview() {
    $("#approveTask").hide();
    $("#declineTask").hide();
    $("#taskStatus").removeClass("status-finished");
    $("#taskStatus").addClass("status-verified");
    $("#issueStatus").removeClass("status-finished");
    $("#issueStatus").addClass("status-verified");
    $("#taskStatusMessage")
      .removeClass("state-finished")
      .addClass("state-verified")
      .html("Verified");
    $("#issueStatusMessage")
      .closest("span")
      .removeClass("gray")
      .addClass("task-done")
      .html("<em>Verified</em>");
    $("#taskDone").show();
    $("#reviewChoice").hide();
    $("#issueStatusInfo")
      .removeClass("state-draft")
      .addClass("state-verified")
      .html("Closed");
  }

  function visualSelector() {
    $(this).find("option:selected").each(function() {
      var $respective = $(this).val(),
          $particular = $(".show-in-tree").find("#" + $respective + "").closest(".show-in-tree");

      $particular.children("span").css("display", "none");
      $(".show-in-tree").find("#" + $respective + "").css("display", "block");
    });
  }

  function AddCA() {
    $("#CaModal").modal("hide");
    $("#CaAdded").show();
  }

  function newIssue() {
    $("#issueModal").modal("hide");
    $("#newIssue").show();
    $(".nav li").removeClass("active");
    $("#issuesNavItem").closest("li").addClass("active");
    window.location.href = '#issues';
    $(".object-wrap").hide();
    $(".object-wrap-issues").show();
  }

  function sortableHeader() {
    var $this = $(this),
        $all = $this.closest(".tree-header").find(".widget-col-title");

    if($this.hasClass("asc")) {
      $this.removeClass("asc");
      $this.addClass("desc");
    } else {
      $all.removeClass("asc desc");
      $this.addClass("asc");
      $this.removeClass("desc");
    }
  }

  $(".top-inner-nav a").on("click", innerNavTrigger);

  $("#autoGenerateCA").on("click", generateCA);

  $("#auditRoleSave").on('click', personRole);

  $("#startReviewWorkflow").on("click", reviewWorkflow);

  $("#startTask").on("click", startTask);

  $("#finishTask").on("click", finishTask);

  $("#approveReview, #approveTask").on("click", approveReview);

  $(".visual-selector").on("change", visualSelector);

  $("#CASave").on("click", AddCA);

  $("#issueSave").on("click", newIssue);

  $(".widget-col-title").on("click", sortableHeader);

});
