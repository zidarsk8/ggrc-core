Feature: Full text search

  Background:
    Given service description

  Scenario: Search finds a document with a matching description
    Given a new "Control" named "control"
    And "control" property "description" is "Let's match on foobar!"
    And "control" is POSTed to its collection
    When fulltext search for "foobar" as "results"
    Then "control" is in the search result "results"

  Scenario: Search doesn't find a document without a matching description
    Given a new "Control" named "control"
    And "control" property "description" is "This shouldn't match at all."
    And "control" is POSTed to its collection
    When fulltext search for "bleargh" as "results"
    Then "control" isn't in the search result "results"

  Scenario: Search can group results by type
    Given the following resources are POSTed:
      | type    | name     | description                                   |
      | Control | control1 | A control that should match because fortytwo. |
      | Control | control2 | A control that shouldn't match.               |
      | Cycle   | cycle1   | A cycle that should match because fortytwo.   |
    When fulltext search grouped by type for "fortytwo" as "results"
    Then "control1" is in the "Control" group of "results"
    And "control2" isn't in the "Control" group of "results"
    And "cycle1" is in the "Cycle" group of "results"

  Scenario: Search finds a document with a matching description but only in authorized contexts
    Given current user is "{\"email\": \"bobtester@testertester.com\", \"name\": \"Bob Tester\", \"permissions\": {\"create\": {\"Control\": [1,2]}, \"read\": {\"Control\": [1,2]}, \"update\": {\"Control\": [1,2]}}}"
    And a new "Control" named "control1"
    And a new "Control" named "control2"
    And "control1" property "description" is "Let's match on foobar!"
    And "control2" property "description" is "Let's match on foobar, also!"
    And "control1" property "context_id" is literal "1"
    And "control2" property "context_id" is literal "2"
    And "control1" is POSTed to its collection
    And "control2" is POSTed to its collection
    When fulltext search for "foobar" as "results"
    Then "control1" is in the search result "results"
    Then "control2" is in the search result "results"
    Given current user is "{\"email\": \"tester@testertester.com\", \"name\": \"Jo Tester\", \"permissions\": {\"create\": {\"Control\": [1]}, \"read\": {\"Control\": [1]}, \"update\": {\"Control\": [1]}}}"
    When fulltext search for "foobar" as "results"
    Then "control1" is in the search result "results"
    Then "control2" isn't in the search result "results"

