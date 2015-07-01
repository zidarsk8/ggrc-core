# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: brad@reciprocitylabs.com
# Maintained By: brad@reciprocitylabs.com

Feature: Private Program Audits and Role Implication

  Background:
    Given service description
    And User "program.owner@example.com" has "ProgramCreator" role
    And User "program.owner@example.com" has "Editor" role
    And User "program.editor@example.com" has "Editor" role
    And User "program.reader@example.com" has "Editor" role
    And a user with email "auditor@example.com" as "auditor"
    And a user with email "assignee@example.com" as "assignee"
    And the current user
      """
      { "email": "program.owner@example.com" }
      """
    Given a new "Program" named "private_program"
    And "private_program" property "private" is literal "True"
    And "private_program" is POSTed to its collection
    When GET of the resource "private_program"
    Given a new "Audit" named "audit"
    And "audit" link property "program" is "private_program"
    And link property "context" of "audit" is link property "context" of "private_program"
    And "audit" is POSTed to its collection
    Then GET of "audit" is allowed
    Given a user with email "program.editor@example.com" as "person"
    Given existing Role named "ProgramEditor"
    And a new "ggrc_basic_permissions.models.UserRole" named "role_assignment" is created from json
    """
    {
      "role": {
        "id": {{context.ProgramEditor.value['role']['id']}},
        "type": "Role"
        },
      "person": {
        "id": {{context.person['id']}},
        "type": "Person"
      },
      "context": {
        "id": {{context.private_program.value['program']['context']['id']}},
        "type": "Context"
        }
    }
    """
    And "role_assignment" is POSTed to its collection
    Given a user with email "program.reader@example.com" as "person"
    Given existing Role named "ProgramReader"
    And a new "ggrc_basic_permissions.models.UserRole" named "role_assignment" is created from json
    """
    {
      "role": {
        "id": {{context.ProgramReader.value['role']['id']}},
        "type": "Role"
        },
      "person": {
        "id": {{context.person['id']}},
        "type": "Person"
      },
      "context": {
        "id": {{context.private_program.value['program']['context']['id']}},
        "type": "Context"
        }
    }
    """
    And "role_assignment" is POSTed to its collection
    Given a user with email "auditor@example.com" as "person"
    Given existing Role named "Auditor"
    And a new "ggrc_basic_permissions.models.UserRole" named "role_assignment" is created from json
    """
    {
      "role": {
        "id": {{context.Auditor.value['role']['id']}},
        "type": "Role"
        },
      "person": {
        "id": {{context.person['id']}},
        "type": "Person"
      },
      "context": {
        "id": {{context.audit.value['audit']['context']['id']}},
        "type": "Context"
        }
    }
    """
    And "role_assignment" is POSTed to its collection

  Scenario: ProgramOwner has ProgramAuditOwner permissions
    Given the current user
      """
      { "email": "program.owner@example.com" }
      """
    Then GET of "audit" is allowed
    Then PUT of "audit" is allowed
    Then GET of "audit" is allowed
    Then DELETE of "audit" is forbidden
    Given a new "Objective" named "objective"
    And "objective" is POSTed to its collection
    And a new "Request" named "request"
    And link property "context" of "request" is link property "context" of "audit"
    And "request" link property "audit" is "audit"
    And "request" link property "objective" is "objective"
    And "request" link property "assignee" is "assignee"
    And "request" link property "requestor" is "auditor"
    Then POST of "request" to its collection is allowed
    Then GET of "request" is allowed
    Then PUT of "request" is allowed
    Then GET of "request" is allowed
    Then DELETE of "request" is forbidden
    Given a new "DocumentationResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Then POST of "response" to its collection is allowed
    Then GET of "response" is allowed
    Then PUT of "response" is allowed
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden
    Given a new "InterviewResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Then POST of "response" to its collection is allowed
    Then GET of "response" is allowed
    Then PUT of "response" is allowed
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden
    Given a new "Document" named "population_worksheet"
    And "population_worksheet" is POSTed to its collection
    Given a new "Document" named "sample_worksheet"
    And "sample_worksheet" is POSTed to its collection
    Given a new "Document" named "sample_evidence"
    And "sample_evidence" is POSTed to its collection
    Given a new "PopulationSampleResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "population_worksheet" is "population_worksheet"
    And "response" link property "sample_worksheet" is "sample_worksheet"
    And "response" link property "sample_evidence" is "sample_evidence"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Then POST of "response" to its collection is allowed
    Then GET of "response" is allowed
    Then PUT of "response" is allowed
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden

  Scenario: ProgramEditor has ProgramAuditEditor permissions
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then GET of "audit" is allowed
    Then PUT of "audit" is allowed
    Then GET of "audit" is allowed
    Then DELETE of "audit" is forbidden
    Given a new "Objective" named "objective"
    And "objective" is POSTed to its collection
    And a new "Request" named "request"
    And link property "context" of "request" is link property "context" of "audit"
    And "request" link property "audit" is "audit"
    And "request" link property "objective" is "objective"
    And "request" link property "assignee" is "assignee"
    And "request" link property "requestor" is "auditor"
    Then POST of "request" to its collection is allowed
    Then GET of "request" is allowed
    Then PUT of "request" is allowed
    Then GET of "request" is allowed
    Then DELETE of "request" is forbidden
    Given a new "DocumentationResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Then POST of "response" to its collection is allowed
    Then GET of "response" is allowed
    Then PUT of "response" is allowed
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden
    Given a new "InterviewResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Then POST of "response" to its collection is allowed
    Then GET of "response" is allowed
    Then PUT of "response" is allowed
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden
    Given a new "Document" named "population_worksheet"
    And "population_worksheet" is POSTed to its collection
    Given a new "Document" named "sample_worksheet"
    And "sample_worksheet" is POSTed to its collection
    Given a new "Document" named "sample_evidence"
    And "sample_evidence" is POSTed to its collection
    Given a new "PopulationSampleResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "population_worksheet" is "population_worksheet"
    And "response" link property "sample_worksheet" is "sample_worksheet"
    And "response" link property "sample_evidence" is "sample_evidence"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Then POST of "response" to its collection is allowed
    Then GET of "response" is allowed
    Then PUT of "response" is allowed
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden

  Scenario: ProgramReader has ProgramAuditReader permissions
    Given the current user
      """
      { "email": "program.reader@example.com" }
      """
    Then GET of "audit" is allowed
    Then PUT of "audit" is forbidden
    Then GET of "audit" is allowed
    Then DELETE of "audit" is forbidden
    Given a new "Objective" named "objective"
    And "objective" is POSTed to its collection
    And a new "Request" named "request"
    And link property "context" of "request" is link property "context" of "audit"
    And "request" link property "audit" is "audit"
    And "request" link property "objective" is "objective"
    And "request" link property "assignee" is "assignee"
    And "request" link property "requestor" is "auditor"
    Then POST of "request" to its collection is forbidden
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then POST of "request" to its collection is allowed
    Then GET of "request" is allowed
    Given the current user
      """
      { "email": "program.reader@example.com" }
      """
    Then GET of "request" is allowed
    Then PUT of "request" is forbidden
    Then GET of "request" is allowed
    Then DELETE of "request" is forbidden
    Given a new "DocumentationResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Then POST of "response" to its collection is forbidden
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then POST of "response" to its collection is allowed
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "program.reader@example.com" }
      """
    Then GET of "response" is allowed
    Then PUT of "response" is forbidden
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden
    Given a new "InterviewResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Then POST of "response" to its collection is forbidden
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then POST of "response" to its collection is allowed
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "program.reader@example.com" }
      """
    Then GET of "response" is allowed
    Then PUT of "response" is forbidden
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Given a new "Document" named "population_worksheet"
    And "population_worksheet" is POSTed to its collection
    Given a new "Document" named "sample_worksheet"
    And "sample_worksheet" is POSTed to its collection
    Given a new "Document" named "sample_evidence"
    And "sample_evidence" is POSTed to its collection
    Given a new "PopulationSampleResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "population_worksheet" is "population_worksheet"
    And "response" link property "sample_worksheet" is "sample_worksheet"
    And "response" link property "sample_evidence" is "sample_evidence"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Given the current user
      """
      { "email": "program.reader@example.com" }
      """
    Then POST of "response" to its collection is forbidden
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then POST of "response" to its collection is allowed
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "program.reader@example.com" }
      """
    Then GET of "response" is allowed
    Then PUT of "response" is forbidden
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden

  Scenario: Auditors can create, read, and update requests but cannot create responses
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "audit" is allowed
    Then PUT of "audit" is forbidden
    Then GET of "audit" is allowed
    Then DELETE of "audit" is forbidden
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Given a new "Objective" named "objective"
    And "objective" is POSTed to its collection
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    And a new "Request" named "request"
    And link property "context" of "request" is link property "context" of "audit"
    And "request" link property "audit" is "audit"
    And "request" link property "objective" is "objective"
    And "request" link property "assignee" is "assignee"
    And "request" link property "requestor" is "auditor"
    Then POST of "request" to its collection is allowed
    Then GET of "request" is allowed
    Then PUT of "request" is allowed
    Then GET of "request" is allowed
    Then DELETE of "request" is allowed
    # Now create one that will be responded to
    Given a new "Request" named "request"
    And link property "context" of "request" is link property "context" of "audit"
    And "request" link property "audit" is "audit"
    And "request" link property "objective" is "objective"
    And "request" link property "assignee" is "assignee"
    And "request" link property "requestor" is "auditor"
    Then POST of "request" to its collection is allowed
    Then GET of "request" is allowed

    Given a new "DocumentationResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Then POST of "response" to its collection is forbidden
    Given a new "InterviewResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Then POST of "response" to its collection is forbidden
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Given a new "Document" named "population_worksheet"
    And "population_worksheet" is POSTed to its collection
    Given a new "Document" named "sample_worksheet"
    And "sample_worksheet" is POSTed to its collection
    Given a new "Document" named "sample_evidence"
    And "sample_evidence" is POSTed to its collection
    Given a new "PopulationSampleResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "population_worksheet" is "population_worksheet"
    And "response" link property "sample_worksheet" is "sample_worksheet"
    And "response" link property "sample_evidence" is "sample_evidence"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then POST of "response" to its collection is forbidden

  Scenario: Auditors can read responses that are in a valid state
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Given a new "Objective" named "objective"
    And "objective" is POSTed to its collection
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    And a new "Request" named "request"
    And link property "context" of "request" is link property "context" of "audit"
    And "request" link property "audit" is "audit"
    And "request" link property "objective" is "objective"
    And "request" link property "assignee" is "assignee"
    And "request" link property "requestor" is "auditor"
    Then POST of "request" to its collection is allowed
    Given a new "DocumentationResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then POST of "response" to its collection is allowed
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "response" is forbidden
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then GET of "response" is allowed
    When "response" property "status" is "Accepted"
    Then PUT of "response" is allowed
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then GET of "response" is allowed
    When "response" property "status" is "Rejected"
    Then PUT of "response" is allowed
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden
    Given a new "InterviewResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then POST of "response" to its collection is allowed
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "response" is forbidden
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then GET of "response" is allowed
    When "response" property "status" is "Accepted"
    Then PUT of "response" is allowed
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then GET of "response" is allowed
    When "response" property "status" is "Rejected"
    Then PUT of "response" is allowed
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Given a new "Document" named "population_worksheet"
    And "population_worksheet" is POSTed to its collection
    Given a new "Document" named "sample_worksheet"
    And "sample_worksheet" is POSTed to its collection
    Given a new "Document" named "sample_evidence"
    And "sample_evidence" is POSTed to its collection
    Given a new "PopulationSampleResponse" named "response"
    And link property "context" of "response" is link property "context" of "audit"
    And "response" link property "population_worksheet" is "population_worksheet"
    And "response" link property "sample_worksheet" is "sample_worksheet"
    And "response" link property "sample_evidence" is "sample_evidence"
    And "response" link property "request" is "request"
    And "response" property "status" is "Assigned"
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then POST of "response" to its collection is forbidden
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then POST of "response" to its collection is allowed
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "response" is forbidden
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then GET of "response" is allowed
    When "response" property "status" is "Accepted"
    Then PUT of "response" is allowed
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "program.editor@example.com" }
      """
    Then GET of "response" is allowed
    When "response" property "status" is "Rejected"
    Then PUT of "response" is allowed
    Then GET of "response" is allowed
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "response" is allowed
    Then DELETE of "response" is forbidden

  #Scenario: Auditors can update responses in a limited, validated, way

  #Scenario: Auditors can read business and governance objects (eventually, scoped... but that's tough)

  Scenario: Auditors have AuditorProgramReader permissions in the audited program
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "private_program" is allowed
    Then PUT of "private_program" is forbidden
    Then GET of "private_program" is allowed
    Then DELETE of "private_program" is forbidden

  Scenario: Auditors cannot access object view pages
    Given the current user
      """
      { "email": "program.owner@example.com" }
      """
    Then GET of "audit" is allowed
    Then PUT of "audit" is allowed
    Then GET of "audit" is allowed
    Then DELETE of "audit" is forbidden
    Given a new "Objective" named "objective"
    And "objective" is POSTed to its collection
    Then GET of "objective" object page is allowed
    Given the current user
      """
      { "email": "auditor@example.com" }
      """
    Then GET of "objective" object page is forbidden
