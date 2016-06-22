# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

Feature: Basic Audit support

  Background:
    Given service description
    And User "program.owner@example.com" has "ProgramCreator" role
    And the current user
      """
      { "email": "program.owner@example.com" }
      """

  Scenario: Program Creators can create Audits
    Given a new "Program" named "private_program"
    And "private_program" property "private" is literal "True"
    And "private_program" is POSTed to its collection
    When GET of the resource "private_program"
    Given a new "Audit" named "audit"
    And "audit" link property "program" is "private_program"
    And link property "context" of "audit" is link property "context" of "private_program"
    And "audit" is POSTed to its collection
    Then GET of "audit" is allowed
