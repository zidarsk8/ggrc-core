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

  Examples: Resources to cache from Core
      | resource_type      | table_plural         | property    | value1   | value2   |
      | ControlAssertion   | control_assertions   | name        | name1    | name2    |
      | ControlCategory    | control_categories   | name        | name1    | name2    |
      | Control            | controls             | description | desc1    | desc2    |
      | DataAsset          | data_assets          | description | desc1    | desc2    |
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
      | ObjectPerson       | object_people        | status      | Draft    | Final    |
      | Objective          | objectives           | description | desc1    | desc2    |
      | Option             | options              | title       | title1   | title2   |
      | OrgGroup           | org_groups           | description | desc1    | desc2    |
      | Person             | people               | name        | name1    | name2    |
      | Product            | products             | description | desc1    | desc2    |
      | Project            | projects             | description | desc1    | desc2    |
      | Program            | programs             | description | desc1    | desc2    |
      | ProgramDirective   | program_directives   | status      | Draft    | Final    |
      | Relationship       | relationships        | status      | Draft    | Final    |
      | Section            | sections             | description | desc1    | desc2    |
      | Clause             | clauses              | description | desc1    | desc2    |
      #| SystemOrProcess    | systems_or_processes | description | desc1    | desc2    |
      | System             | systems              | description | desc1    | desc2    |
      | Process            | processes            | description | desc1    | desc2    |

  Examples: Resources to cache from `ggrc_gdrive_integration`
      | resource_type      | table_plural         | property    | value1   | value2   |
      | ObjectFile         | object_files         | file_id     | 1        | 2        |
      | ObjectFolder       | object_folders       | folder_id   | 1        | 2        |
      | ObjectEvent        | object_events        | event_id    | 1        | 2        |

  Examples: Resources to cache from `ggrc_basic_permissions`
      | resource_type      | table_plural         | property    | value1   | value2   |
      | Role               | roles                | name        | name1    | name2    |
      # UserRole has no extraneous attributes (like status) to change to force
      #   expiry, so will be harder to test.
      #| UserRole           | user_roles           |


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
    And "example_mapping" property "<property>" is "<value1>"
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

    # Confirm the mapping object and endpoints are expired on PUT
    # Update the mapping object
    When GET of the resource "example_mapping"
    And "example_mapping" property "<property>" is "<value2>"
    And PUT "example_mapping"

    # Confirm the mapping object itself gets expired and re-cached
    When GET of "<mapping_type>" collection using id__in for "example_mapping"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    When GET of "<mapping_type>" collection using id__in for "example_mapping"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"

    # Confirm the near endpoint is expired and is correct
    When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Miss"
    And "example_mapping" is in the links property "<near_resource_key>" of "example_near_resource"
    When GET of "<near_resource_type>" collection using id__in for "example_near_resource"
    Then the response has a header "X-GGRC-Cache"
    And the response header "X-GGRC-Cache" is "Hit"
    And "example_mapping" is in the links property "<near_resource_key>" of "example_near_resource"

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


  Examples: Cached resources with mappings from Core
      | near_resource_type        | near_resource_key    | mapping_near_key     | mapping_type              | property | value1 | value2 |
      | Audit                     | requests             | audit                | Request                   | status   | Requested | Responded |
      | Audit                     | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Control                   | program_controls     | control              | ProgramControl            | status   | Draft  | Final  |
      | Control                   | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Control                   | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Control                   | object_controls      | control              | ObjectControl             | status   | Draft  | Final  |
      | Control                   | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | DataAsset                 | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | DataAsset                 | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | DataAsset                 | object_controls      | controllable         | ObjectControl             | status   | Draft  | Final  |
      | DataAsset                 | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | DataAsset                 | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | DataAsset                 | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | Contract                  | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | Contract                  | program_directives   | directive            | ProgramDirective          | status   | Draft  | Final  |
      | Contract                  | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Contract                  | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Contract                  | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Contract                  | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | Policy                    | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | Policy                    | program_directives   | directive            | ProgramDirective          | status   | Draft  | Final  |
      | Policy                    | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Policy                    | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Policy                    | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Policy                    | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | Policy                     | sections             | directive            | Section                   | title    | title1 | title2 |
      | Regulation                | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | Regulation                | program_directives   | directive            | ProgramDirective          | status   | Draft  | Final  |
      | Regulation                | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Regulation                | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Regulation                | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Regulation                | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | Regulation                 | sections             | directive            | Section                   | title    | title1 | title2 |
      | Standard                  | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | Standard                  | program_directives   | directive            | ProgramDirective          | status   | Draft  | Final  |
      | Standard                  | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Standard                  | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Standard                  | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Standard                  | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | Standard                   | sections             | directive            | Section                   | title    | title1 | title2 |
      | Document                  | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Facility                  | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | Facility                  | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Facility                  | object_controls      | controllable         | ObjectControl             | status   | Draft  | Final  |
      | Facility                  | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Facility                  | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Facility                  | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | Market                    | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | Market                    | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Market                    | object_controls      | controllable         | ObjectControl             | status   | Draft  | Final  |
      | Market                    | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Market                    | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Market                    | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | Meeting                   | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Objective                 | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Objective                 | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Objective                 | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | OrgGroup                  | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | OrgGroup                  | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | OrgGroup                  | object_controls      | controllable         | ObjectControl             | status   | Draft  | Final  |
      | OrgGroup                  | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | OrgGroup                  | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | OrgGroup                  | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | Person                    | object_people        | person               | ObjectPerson              | status   | Draft  | Final  |
      | Product                   | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | Product                   | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Product                   | object_controls      | controllable         | ObjectControl             | status   | Draft  | Final  |
      | Product                   | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Product                   | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Product                   | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | Program                   | program_controls     | program              | ProgramControl            | status   | Draft  | Final  |
      | Program                   | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | Program                   | program_directives   | program              | ProgramDirective          | status   | Draft  | Final  |
      | Program                   | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Program                   | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Program                   | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Program                   | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | Project                   | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | Project                   | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Project                   | object_controls      | controllable         | ObjectControl             | status   | Draft  | Final  |
      | Project                   | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Project                   | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Project                   | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | DocumentationResponse     | object_controls      | controllable         | ObjectControl             | status   | Draft  | Final  |
      | DocumentationResponse     | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | DocumentationResponse     | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | DocumentationResponse     | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | DocumentationResponse     | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | InterviewResponse         | object_controls      | controllable         | ObjectControl             | status   | Draft  | Final  |
      | InterviewResponse         | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | InterviewResponse         | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | InterviewResponse         | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | InterviewResponse         | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | PopulationSampleResponse  | object_controls      | controllable         | ObjectControl             | status   | Draft  | Final  |
      | PopulationSampleResponse  | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | PopulationSampleResponse  | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | PopulationSampleResponse  | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | PopulationSampleResponse  | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | Section                   | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Section                   | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Section                   | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Clause                    | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Clause                    | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Clause                    | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | System                    | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | System                    | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | System                    | object_controls      | controllable         | ObjectControl             | status   | Draft  | Final  |
      | System                    | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | System                    | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | System                    | related_destinations | source               | Relationship              | status   | Draft  | Final  |
      | Process                   | related_sources      | destination          | Relationship              | status   | Draft  | Final  |
      | Process                   | object_owners        | ownable              | ObjectOwner               | status   | Draft  | Final  |
      | Process                   | object_controls      | controllable         | ObjectControl             | status   | Draft  | Final  |
      | Process                   | object_documents     | documentable         | ObjectDocument            | status   | Draft  | Final  |
      | Process                   | object_people        | personable           | ObjectPerson              | status   | Draft  | Final  |
      | Process                   | related_destinations | source               | Relationship              | status   | Draft  | Final  |

  Examples: Cached resources with mappings from `ggrc_gdrive_integration`
      | near_resource_type        | near_resource_key    | mapping_near_key     | mapping_type              | property  | value1 | value2 |
      | Request                   | object_folders       | folderable           | ObjectFolder              | folder_id | 1      | 2      |
      | Program                   | object_folders       | folderable           | ObjectFolder              | folder_id | 1      | 2      |
      | Audit                     | object_folders       | folderable           | ObjectFolder              | folder_id | 1      | 2      |
      | DocumentationResponse     | object_files         | fileable             | ObjectFile                | file_id   | 1      | 2      |
      | PopulationSampleResponse  | object_files         | fileable             | ObjectFile                | file_id   | 1      | 2      |
      | Document                  | object_files         | fileable             | ObjectFile                | file_id   | 1      | 2      |
      | Meeting                   | object_events        | eventable            | ObjectEvent               | event_id | 1      | 2      |

  Examples: Cached resources with mappings from `ggrc_basic_permissions`
      | near_resource_type        | near_resource_key    | mapping_near_key     | mapping_type              | property  | value1 | value2 |
      # UserRole has no extraneous attributes (like status) to change to force
      #   expiry, so will be harder to test.
      #| Person                    | user_roles           | person               | UserRole                  | status   | Draft  | Final  |
