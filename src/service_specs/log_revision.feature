# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: brad@reciprocitylabs.com
# Maintained By: brad@reciprocitylabs.com

Feature: Log events and revisions
  In order to be able to detect who changed what and when
  As a system administrator
  I would like to have all changes logged

  Background:
    Given service description

  Scenario: Event and revision on POST
    Given a new "Program" named "example_program"
    When "example_program" is POSTed to its collection
    And GET of "/api/events" as "events"
    Then the value of the "events_collection.events.0.resource_type" property of the "events" is "Program"
    And the value of the "events_collection.events.0.action" property of the "events" is "POST"

  Scenario: Event and revision on DELETE
    Given a new "Program" named "example_program"
    And "example_program" is POSTed to its collection
    And a new "Regulation" named "example_regulation"
    And "example_regulation" is POSTed to its collection
    And a new "ProgramDirective" named "example_program_directive"
    And "example_program_directive" link property "directive" is "example_regulation"
    And "example_program_directive" link property "program" is "example_program"
    And "example_program_directive" is POSTed to its collection
    When GET of the resource "example_program"
    And DELETE "example_program"
    And GET of "/api/events?__include=revisions" as "events"
    Then the revisions for the latest event contains "deleted" and "Program"
    And the revisions for the latest event contains "deleted" and "ProgramDirective"

  Scenario: Event and revision on PUT
    Given a new "Program" named "example_program"
    And "example_program" is POSTed to its collection
    When GET of the resource "example_program"
    And "example_program" property "description" is "Some Description"
    And PUT "example_program"
    And GET of "/api/events" as "events"
    Then the value of the "events_collection.events.0.resource_type" property of the "events" is "Program"
    And the value of the "events_collection.events.0.action" property of the "events" is "PUT"
