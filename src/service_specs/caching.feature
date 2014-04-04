# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

Feature: Caching
  I would like to have objects cached on repeated loads when using `id__in`
  I would like to have the cache entry invalidated on PUT
  I would like to have the cache entry removed on DELETE

  Background:
    Given service description

  Scenario Outline: Caching Misses and Hits
    Given a new "<resource_type>" named "example_resource"
    And "example_resource" property "<property>" is "<value1>"
    And "example_resource" is POSTed to its collection

    When GET of "<resource_type>" collection using id__in for "example_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    When GET of "<resource_type>" collection using id__in for "example_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"

    When GET of the resource "example_resource"
    And "example_resource" property "<property>" is "<value2>"
    And PUT "example_resource"
    When GET of "<resource_type>" collection using id__in for "example_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    And the value of the "<table_plural>_collection.<table_plural>.0.<property>" property of the "collectionresource" is "<value2>"
    When GET of "<resource_type>" collection using id__in for "example_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"
    And the value of the "<table_plural>_collection.<table_plural>.0.<property>" property of the "collectionresource" is "<value2>"

    When GET of the resource "example_resource"
    And DELETE "example_resource"
    When GET of "<resource_type>" collection using id__in for "example_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    And the "<table_plural>_collection.<table_plural>" property of the "collectionresource" is empty
    When GET of "<resource_type>" collection using id__in for "example_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    And the "<table_plural>_collection.<table_plural>" property of the "collectionresource" is empty

  Examples: Cached Resources
      | resource_type      | table_plural         | property    | value1   | value2   |
      | ControlAssertion   | control_assertions   | name        | name1    | name2    |
      | ControlCategory    | control_categories   | name        | name1    | name2    |
      | Control            | controls             | description | desc1    | desc2    |
      | DataAsset          | data_assets          | description | desc1    | desc2    |
      #| Directive          | directives           | description | desc1    | desc2    |
      | DirectiveControl   | directive_controls   | status      | Draft    | Final    |
      | DirectiveSection   | directive_sections   | status      | Draft    | Final    |
      | Contract           | contracts            | description | desc1    | desc2    |
      | Policy             | policies             | description | desc1    | desc2    |
      | Regulation         | regulations          | description | desc1    | desc2    |
      | Standard           | standards            | description | desc1    | desc2    |
      | Document           | documents            | description | desc1    | desc2    |
      | Facility           | facilities           | description | desc1    | desc2    |
      | Help               | helps                | content     | content1 | content2 |
      | Market             | markets              | description | desc1    | desc2    |
      #| Meeting            | meetings             |
      | ObjectControl      | object_controls      | status      | Draft    | Final    |
      | ObjectDocument     | object_documents     | status      | Draft    | Final    |
      | ObjectObjective    | object_objectives    | status      | Draft    | Final    |
      | ObjectPerson       | object_people        | status      | Draft    | Final    |
      | Objective          | objectives           | description | desc1    | desc2    |
      | ObjectiveControl   | objective_controls   | status      | Draft    | Final    |
      | Option             | options              | title       | title1   | title2   |
      | OrgGroup           | org_groups           | description | desc1    | desc2    |
      | Person             | people               | name        | name1    | name2    |
      | Product            | products             | description | desc1    | desc2    |
      | Project            | projects             | description | desc1    | desc2    |
      | Program            | programs             | description | desc1    | desc2    |
      | ProgramDirective   | program_directives   | status      | Draft    | Final    |
      | Relationship       | relationships        | status      | Draft    | Final    |
      #| SectionBase        | section_bases        | description | desc1    | desc2    |
      | Section            | sections             | description | desc1    | desc2    |
      | Clause             | clauses              | description | desc1    | desc2    |
      | SectionObjective   | section_objectives   | status      | Draft    | Final    |
      #| SystemOrProcess    | systems_or_processes | description | desc1    | desc2    |
      | System             | systems              | description | desc1    | desc2    |
      | Process            | processes            | description | desc1    | desc2    |
