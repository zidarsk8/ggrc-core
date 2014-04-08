# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

Feature: Resource caching
  I would like resources to be cached:
    I would like to have objects cached on repeated loads when using `id__in`
    I would like to have the cache entry invalidated on PUT
    I would like to have the cache entry removed on DELETE

  I would like resources to be expired due to mapping-object changes:
    I would like to have objects cached on repeated loads when using `id__in`
    I would like to have the cache entry invalidated after POST of mapping
    I would like to have the cache entry invalidated after PUT of mapping
    I would like to have the cache entry invalidated after DELETE of mapping

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



  Scenario Outline: Caching misses and hits when many-to-many mappings were affected
    # Set up the endpoint objects
    Given a new "<near_resource_type>" named "example_near_resource"
    And "example_near_resource" is POSTed to its collection
    And a new "<far_resource_type>" named "example_far_resource"
    And "example_far_resource" is POSTed to its collection

    # Confirm the near endpoint are cached
    When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"

    # Confirm the far endpoint is cached
    When GET of "<far_resource_type>" collection using id__in for "example_far_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    When GET of "<far_resource_type>" collection using id__in for "example_far_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"

    # Create the mapping object
    Given a new "<mapping_type>" named "example_mapping"
    And "example_mapping" link property "<mapping_near_key>" is "example_near_resource"
    And "example_mapping" link property "<mapping_far_key>" is "example_far_resource"
    And "example_mapping" is POSTed to its collection

    # Confirm the near endpoint is expired and is correct
    When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    And "example_mapping" is in the links property "<near_resource_key>" of "example_near_resource"
    When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"
    And "example_mapping" is in the links property "<near_resource_key>" of "example_near_resource"

    # Confirm the far endpoint is expired and is correct
    When GET of "<far_resource_type>" collection using id__in for "example_far_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    And "example_mapping" is in the links property "<far_resource_key>" of "example_far_resource"
    When GET of "<far_resource_type>" collection using id__in for "example_far_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"
    And "example_mapping" is in the links property "<far_resource_key>" of "example_far_resource"

    # Confirm the mapping object itself gets cached
    When GET of "<mapping_type>" collection using id__in for "example_mapping"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    When GET of "<mapping_type>" collection using id__in for "example_mapping"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"


  Examples: Cached resources with mappings
      | near_resource_type  | near_resource_key | mapping_near_key | mapping_type   | mapping_far_key | far_resource_key | far_resource_type |
      | Control             | object_documents  | documentable     | ObjectDocument | document        | object_documents | Document          |



  Scenario Outline: Caching misses and hits when many-to-many mappings were affected
    # Set up the endpoint objects
    Given a new "<near_resource_type>" named "example_near_resource"
    And "example_near_resource" is POSTed to its collection

    # Confirm the near endpoint are cached
    When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"

    # Create the mapping object
    Given a new "<mapping_type>" named "example_mapping"
    And "example_mapping" property "<property>" is "Draft"
    And "example_mapping" link property "<mapping_near_key>" is "example_near_resource"
    And "example_mapping" is POSTed to its collection

    # Confirm the near endpoint is expired and is correct
    When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    And "example_mapping" is in the links property "<near_resource_key>" of "example_near_resource"
    When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"
    And "example_mapping" is in the links property "<near_resource_key>" of "example_near_resource"

    # Confirm the mapping object itself gets cached
    When GET of "<mapping_type>" collection using id__in for "example_mapping"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    When GET of "<mapping_type>" collection using id__in for "example_mapping"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"

    ## Confirm the mapping object and endpoints are expired on PUT
    ## Update the mapping object
    #When GET of the resource "example_mapping"
    #And "example_mapping" property "status" is "Final"
    #And PUT "example_mapping"

    ## Confirm the mapping object itself gets expired and re-cached
    #When GET of "<mapping_type>" collection using id__in for "example_mapping"
    #Then the response has a header "X-GGRC-Cache"
    #And the response header "X-GGRC-Cache" is "Miss"
    #When GET of "<mapping_type>" collection using id__in for "example_mapping"
    #Then the response has a header "X-GGRC-Cache"
    #And the response header "X-GGRC-Cache" is "Hit"

    ## Confirm the near endpoint is expired and is correct
    #When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    #Then the response has a header "X-GGRC-Cache"
    #And the response header "X-GGRC-Cache" is "Miss"
    #And "example_mapping" is in the links property "<near_resource_key>" of "example_near_resource"
    #When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    #Then the response has a header "X-GGRC-Cache"
    #And the response header "X-GGRC-Cache" is "Hit"
    #And "example_mapping" is in the links property "<near_resource_key>" of "example_near_resource"

    # Confirm the mapping object and endpoints are expired on DELETE
    # DELETE the mapping object
    When GET of the resource "example_mapping"
    And DELETE "example_mapping"

    # Confirm the near endpoint is expired and is correct
    When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    And "example_mapping" is not in the links property "<near_resource_key>" of "example_near_resource"
    When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"
    And "example_mapping" is not in the links property "<near_resource_key>" of "example_near_resource"

    # Confirm the mapping object itself is expired and deleted
    When GET of "<mapping_type>" collection using id__in for "example_mapping"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    When GET of "<mapping_type>" collection using id__in for "example_mapping"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"


  Examples: Cached resources with mappings
      | near_resource_type        | near_resource_key    | mapping_near_key     | mapping_type              |
      #| Audit                     | requests             | audit                | Request                   |
      | Audit                     | object_people        | personable           | ObjectPerson              |
      | Control                   | control_controls     | control              | ControlControl            |
      | Control                   | implementing_control_controls | implemented_control | ControlControl            |
      | Control                   | program_controls     | control              | ProgramControl            |
      | Control                   | object_owners        | ownable              | ObjectOwner               |
      | Control                   | objective_controls   | control              | ObjectiveControl          |
      | Control                   | directive_controls   | control              | DirectiveControl          |
      | Control                   | object_documents     | documentable         | ObjectDocument            |
      | Control                   | object_controls      | control              | ObjectControl             |
      | Control                   | control_sections     | control              | ControlSection            |
      | Control                   | object_people        | personable           | ObjectPerson              |
      | DataAsset                 | related_sources      | destination          | Relationship              |
      | DataAsset                 | object_owners        | ownable              | ObjectOwner               |
      | DataAsset                 | object_controls      | controllable         | ObjectControl             |
      | DataAsset                 | object_documents     | documentable         | ObjectDocument            |
      | DataAsset                 | object_sections      | sectionable          | ObjectSection             |
      | DataAsset                 | object_people        | personable           | ObjectPerson              |
      | DataAsset                 | object_objectives    | objectiveable        | ObjectObjective           |
      | DataAsset                 | related_destinations | source               | Relationship              |
      | Contract                  | related_sources      | destination          | Relationship              |
      | Contract                  | directive_sections   | directive            | DirectiveSection          |
      | Contract                  | directive_controls   | directive            | DirectiveControl          |
      | Contract                  | program_directives   | directive            | ProgramDirective          |
      | Contract                  | object_owners        | ownable              | ObjectOwner               |
      | Contract                  | object_documents     | documentable         | ObjectDocument            |
      | Contract                  | object_people        | personable           | ObjectPerson              |
      | Contract                  | object_objectives    | objectiveable        | ObjectObjective           |
      | Contract                  | related_destinations | source               | Relationship              |
      | Policy                    | related_sources      | destination          | Relationship              |
      | Policy                    | directive_sections   | directive            | DirectiveSection          |
      | Policy                    | directive_controls   | directive            | DirectiveControl          |
      | Policy                    | program_directives   | directive            | ProgramDirective          |
      | Policy                    | object_owners        | ownable              | ObjectOwner               |
      | Policy                    | object_documents     | documentable         | ObjectDocument            |
      | Policy                    | object_people        | personable           | ObjectPerson              |
      | Policy                    | object_objectives    | objectiveable        | ObjectObjective           |
      | Policy                    | related_destinations | source               | Relationship              |
      | Regulation                | related_sources      | destination          | Relationship              |
      | Regulation                | directive_sections   | directive            | DirectiveSection          |
      | Regulation                | directive_controls   | directive            | DirectiveControl          |
      | Regulation                | program_directives   | directive            | ProgramDirective          |
      | Regulation                | object_owners        | ownable              | ObjectOwner               |
      | Regulation                | object_documents     | documentable         | ObjectDocument            |
      | Regulation                | object_people        | personable           | ObjectPerson              |
      | Regulation                | object_objectives    | objectiveable        | ObjectObjective           |
      | Regulation                | related_destinations | source               | Relationship              |
      | Standard                  | related_sources      | destination          | Relationship              |
      | Standard                  | directive_sections   | directive            | DirectiveSection          |
      | Standard                  | directive_controls   | directive            | DirectiveControl          |
      | Standard                  | program_directives   | directive            | ProgramDirective          |
      | Standard                  | object_owners        | ownable              | ObjectOwner               |
      | Standard                  | object_documents     | documentable         | ObjectDocument            |
      | Standard                  | object_people        | personable           | ObjectPerson              |
      | Standard                  | object_objectives    | objectiveable        | ObjectObjective           |
      | Standard                  | related_destinations | source               | Relationship              |
      | Document                  | object_owners        | ownable              | ObjectOwner               |
      | Facility                  | related_sources      | destination          | Relationship              |
      | Facility                  | object_owners        | ownable              | ObjectOwner               |
      | Facility                  | object_controls      | controllable         | ObjectControl             |
      | Facility                  | object_documents     | documentable         | ObjectDocument            |
      | Facility                  | object_sections      | sectionable          | ObjectSection             |
      | Facility                  | object_people        | personable           | ObjectPerson              |
      | Facility                  | object_objectives    | objectiveable        | ObjectObjective           |
      | Facility                  | related_destinations | source               | Relationship              |
      | Market                    | related_sources      | destination          | Relationship              |
      | Market                    | object_owners        | ownable              | ObjectOwner               |
      | Market                    | object_controls      | controllable         | ObjectControl             |
      | Market                    | object_documents     | documentable         | ObjectDocument            |
      | Market                    | object_sections      | sectionable          | ObjectSection             |
      | Market                    | object_people        | personable           | ObjectPerson              |
      | Market                    | object_objectives    | objectiveable        | ObjectObjective           |
      | Market                    | related_destinations | source               | Relationship              |
      | Meeting                   | object_people        | personable           | ObjectPerson              |
      | Objective                 | objective_objects    | objective            | ObjectObjective           |
      | Objective                 | objective_controls   | objective            | ObjectiveControl          |
      | Objective                 | object_owners        | ownable              | ObjectOwner               |
      | Objective                 | object_documents     | documentable         | ObjectDocument            |
      | Objective                 | object_people        | personable           | ObjectPerson              |
      | Objective                 | object_objectives    | objectiveable        | ObjectObjective           |
      | Objective                 | section_objectives   | objective            | SectionObjective          |
      | OrgGroup                  | related_sources      | destination          | Relationship              |
      | OrgGroup                  | object_owners        | ownable              | ObjectOwner               |
      | OrgGroup                  | object_controls      | controllable         | ObjectControl             |
      | OrgGroup                  | object_documents     | documentable         | ObjectDocument            |
      | OrgGroup                  | object_sections      | sectionable          | ObjectSection             |
      | OrgGroup                  | object_people        | personable           | ObjectPerson              |
      | OrgGroup                  | object_objectives    | objectiveable        | ObjectObjective           |
      | OrgGroup                  | related_destinations | source               | Relationship              |
      | Person                    | object_people        | person               | ObjectPerson              |
      #| Person                    | user_roles           | person               | UserRole                  |
      | Product                   | related_sources      | destination          | Relationship              |
      | Product                   | object_owners        | ownable              | ObjectOwner               |
      | Product                   | object_controls      | controllable         | ObjectControl             |
      | Product                   | object_documents     | documentable         | ObjectDocument            |
      | Product                   | object_sections      | sectionable          | ObjectSection             |
      | Product                   | object_people        | personable           | ObjectPerson              |
      | Product                   | object_objectives    | objectiveable        | ObjectObjective           |
      | Product                   | related_destinations | source               | Relationship              |
      | Program                   | program_controls     | program              | ProgramControl            |
      | Program                   | related_sources      | destination          | Relationship              |
      | Program                   | program_directives   | program              | ProgramDirective          |
      | Program                   | object_owners        | ownable              | ObjectOwner               |
      | Program                   | object_documents     | documentable         | ObjectDocument            |
      | Program                   | object_people        | personable           | ObjectPerson              |
      | Program                   | object_objectives    | objectiveable        | ObjectObjective           |
      | Program                   | related_destinations | source               | Relationship              |
      | Project                   | related_sources      | destination          | Relationship              |
      | Project                   | object_owners        | ownable              | ObjectOwner               |
      | Project                   | object_controls      | controllable         | ObjectControl             |
      | Project                   | object_documents     | documentable         | ObjectDocument            |
      | Project                   | object_sections      | sectionable          | ObjectSection             |
      | Project                   | object_people        | personable           | ObjectPerson              |
      | Project                   | object_objectives    | objectiveable        | ObjectObjective           |
      | Project                   | related_destinations | source               | Relationship              |
      | DocumentationResponse     | object_controls      | controllable         | ObjectControl             |
      | DocumentationResponse     | object_documents     | documentable         | ObjectDocument            |
      | DocumentationResponse     | related_destinations | source               | Relationship              |
      | DocumentationResponse     | object_people        | personable           | ObjectPerson              |
      | DocumentationResponse     | related_sources      | destination          | Relationship              |
      | InterviewResponse         | object_controls      | controllable         | ObjectControl             |
      | InterviewResponse         | object_documents     | documentable         | ObjectDocument            |
      | InterviewResponse         | related_destinations | source               | Relationship              |
      | InterviewResponse         | object_people        | personable           | ObjectPerson              |
      | InterviewResponse         | related_sources      | destination          | Relationship              |
      | PopulationSampleResponse  | object_controls      | controllable         | ObjectControl             |
      | PopulationSampleResponse  | object_documents     | documentable         | ObjectDocument            |
      | PopulationSampleResponse  | related_destinations | source               | Relationship              |
      | PopulationSampleResponse  | object_people        | personable           | ObjectPerson              |
      | PopulationSampleResponse  | related_sources      | destination          | Relationship              |
      | Section                   | directive_sections   | section              | DirectiveSection          |
      | Section                   | control_sections     | section              | ControlSection            |
      | Section                   | object_owners        | ownable              | ObjectOwner               |
      | Section                   | object_documents     | documentable         | ObjectDocument            |
      | Section                   | object_sections      | section              | ObjectSection             |
      | Section                   | object_people        | personable           | ObjectPerson              |
      | Section                   | section_objectives   | section              | SectionObjective          |
      | Clause                    | directive_sections   | section              | DirectiveSection          |
      | Clause                    | control_sections     | section              | ControlSection            |
      | Clause                    | object_owners        | ownable              | ObjectOwner               |
      | Clause                    | object_documents     | documentable         | ObjectDocument            |
      | Clause                    | object_sections      | section              | ObjectSection             |
      | Clause                    | object_people        | personable           | ObjectPerson              |
      | Clause                    | section_objectives   | section              | SectionObjective          |
      | System                    | related_sources      | destination          | Relationship              |
      | System                    | object_owners        | ownable              | ObjectOwner               |
      | System                    | object_controls      | controllable         | ObjectControl             |
      | System                    | object_documents     | documentable         | ObjectDocument            |
      | System                    | object_sections      | sectionable          | ObjectSection             |
      | System                    | object_people        | personable           | ObjectPerson              |
      | System                    | object_objectives    | objectiveable        | ObjectObjective           |
      | System                    | related_destinations | source               | Relationship              |
      | Process                   | related_sources      | destination          | Relationship              |
      | Process                   | object_owners        | ownable              | ObjectOwner               |
      | Process                   | object_controls      | controllable         | ObjectControl             |
      | Process                   | object_documents     | documentable         | ObjectDocument            |
      | Process                   | object_sections      | sectionable          | ObjectSection             |
      | Process                   | object_people        | personable           | ObjectPerson              |
      | Process                   | object_objectives    | objectiveable        | ObjectObjective           |
      | Process                   | related_destinations | source               | Relationship              |
