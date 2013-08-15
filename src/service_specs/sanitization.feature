# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

Feature: String and Text column HTML sanitization

  Background:
    Given service description

  Scenario Outline: All String and Text attributes are HTML sanitized
    Given "<resource_type>" named "resource" with sanitized properties "<properties>"
    And "resource" is POSTed to its collection
    When GET of the resource "resource"
    Then "resource" has sanitized properties "<properties>"

  Examples:
      | resource_type     | properties |
      | Category          | name |
      | Context           | description, name |
      | Control           | description, title, documentation_description, version, notes |
      | ControlAssessment | control_version, notes |
      | Cycle             | description, title, audit_firm, audit_lead, status, notes |
      | DataAsset         | title, description |
      | Contract          | title, version, scope, description, organization |
      | Policy            | title, version, scope, description, organization |
      | Regulation        | title, version, scope, description, organization |
      | Document          | title, description |
      | Facility          | title, description |
      | Help              | title, content |
      | Market            | title, description |
      | Objective         | title, description, notes |
      | Option            | title, description |
      | OrgGroup          | title, description |
      | Person            | company, name |
      | Product           | title, version, description |
      | Program           | title, description |
      | Project           | title, description |
      | Request           | pbc_control_desc, company_responsible, auditor_responsible, test, status, notes, request, pbc_control_code |
      | Response          | status |
      | Risk              | residual_risk, description, impact, title, trigger, preconditions, risk_mitigation, likelihood, kind, threat_vector, inherent_risk |
      | RiskyAttribute    | title, type_string, description |
      | Section           | title, description, notes |
      | System            | title, version, description, notes |
      | Process           | title, version, description, notes |
