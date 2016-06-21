# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

Feature: Basic RESTful CRUD Support

  Background:
    Given service description

  Scenario Outline: HTTP POST and GET
    Given an example "<resource_type>"
    When the example "<resource_type>" is POSTed to its collection
    Then a 201 status code is received
    And the response has a Location header
    And we receive a valid "<resource_type>" in the entity body
    And the received "<resource_type>" matches the one we posted

  Examples: Resources
      | resource_type      |
      | ControlAssertion   |
      | ControlCategory    |
      | Control            |
      | DataAsset          |
      | Contract           |
      | Policy             |
      | Regulation         |
      | Standard           |
      | Document           |
      | Facility           |
      | Help               |
      | Market             |
      #| Meeting            |
      #| ObjectDocument     |
      #| ObjectPerson       |
      | Objective          |
      | Option             |
      | OrgGroup           |
      | Person             |
      | Product            |
      | Project            |
      #| Program            |
      | ProgramDirective   |
      #| Relationship       |
      | Section            |
      | Clause             |
      #| SystemOrProcess    |
      | System             |
      | Process            |
