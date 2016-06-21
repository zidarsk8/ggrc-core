# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

Feature: Some resources can be related to Document resources

  Background:
    Given service description

  Scenario Outline:
    Given a new "Document" named "document"
    And "document" is POSTed to its collection
    And a new "<documentable_type>" named "documentable"
    And "documentable" is POSTed to its collection
    And a new "ObjectDocument" named "object_document"
    And "object_document" link property "document" is "document"
    And "object_document" polymorphic link property "documentable" is "documentable"
    And "object_document" is POSTed to its collection
    When GET of the resource "documentable"
    Then "document" is in the links property "documents" of "documentable"

  Examples:
      | documentable_type |
      | Control           |
      | DataAsset         |
      #| Directive         |
      | Contract          |
      | Policy            |
      | Regulation        |
      | Standard          |
      | Facility          |
      | Market            |
      | Objective         |
      | OrgGroup          |
      | Product           |
      | Program           |
      | Project           |
      | System            |
      | Process           |
