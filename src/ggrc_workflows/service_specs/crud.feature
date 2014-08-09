# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: brad@reciprocitylabs.com
# Maintained By: brad@reciprocitylabs.com

Feature: Basic RESTful CRUD Support

  Background:
    Given service description
    And Workflow factories registration

  Scenario Outline: HTTP POST and GET
    Given an example "<resource_type>"
    When the example "<resource_type>" is POSTed to its collection
    Then a 201 status code is received
    And the response has a Location header
    And we receive a valid "<resource_type>" in the entity body
    And the received "<resource_type>" matches the one we posted

  Examples: Resources
      | resource_type             |
      | Workflow                  |
      | TaskGroup                 |
      | WorkflowPerson            |
      | TaskGroupObject           |
      | TaskGroupTask             |
      | Cycle                     |
      | CycleTaskGroup            |
      | CycleTaskEntry            |
      | CycleTaskGroupObject      |
      | CycleTaskGroupObjectTask  |


  Scenario: Creation of Workflow Cycle
    Given a new "Workflow" named "workflow"
    And "workflow" property "workflow" is literal "True"
    And "workflow" is POSTed to its collection
