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
    Then the value of the "events_collection.events.0.resource_type" property of the "events" is Program
    And the value of the "events_collection.events.0.http_method" property of the "events" is POST

  Scenario: Event and revision on DELETE
    Given a new "Program" named "example_program"
    And "example_program" is POSTed to its collection
    When GET of the resource "example_program"
    And DELETE "example_program"
    And GET of "/api/events" as "events"
    Then the value of the "events_collection.events.0.resource_type" property of the "events" is Program
    And the value of the "events_collection.events.0.http_method" property of the "events" is DELETE  

  Scenario: Event and revision on PUT
    Given a new "Program" named "example_program"
    And "example_program" is POSTed to its collection
    When GET of the resource "example_program"
    And PUT "example_program"
    And GET of "/api/events" as "events"
    Then the value of the "events_collection.events.0.resource_type" property of the "events" is Program
    And the value of the "events_collection.events.0.http_method" property of the "events" is PUT
