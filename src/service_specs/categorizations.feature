Feature: Many resources can be "categorized". This feature will exercise
  categorizing relations.

  Background:
    Given service description

  Scenario Outline:
    Given a Category resource named "some_category" for scope "<scope>"
    And "some_category" is POSTed to its collection
    And a new "<resource_type>" named "categorized_resource"
    And "some_category" is added to links property "<category_property>" of "categorized_resource"
    And "categorized_resource" is POSTed to its collection
    When GET of the resource "some_category"
    And GET of the resource "some_category"
    Then the "<category_property>" property of the "categorized_resource" is not empty
    And "some_category" is in the links property "<category_property>" of "categorized_resource"
    And the "<categorizable_property>" property of the "some_category" is not empty
    And "categorized_resource" is in the links property "<categorizable_property>" of "some_category"

  Examples:
      | resource_type | category_property | categorizable_property | scope |
      | Control       | categories        | controls               | 100   |
      | Control       | assertions        | controls               | 102   |
      | Risk          | categories        | risks                  | 100   |

  Scenario: Control categories and assertions are independent
    Given a Category resource named "a_control_category" for scope "100"
    And "a_control_category" is POSTed to its collection
    And a Category resource named "a_control_assertion" for scope "102"
    And "a_control_assertion" is POSTed to its collection
    And a new "Control" named "control"
    And "a_control_category" is added to links property "categories" of "control"
    And "a_control_assertion" is added to links property "assertions" of "control"
    And "control" is POSTed to its collection
    When GET of the resource "control"
    Then the "categories" property of the "control" is not empty
    And the "assertions" property of the "control" is not empty
    #And "a_control_category" is in the links property "categories" of "control"
    And "a_control_category" is not in the links property "assertions" of "control"
    #And "a_control_assertion" is not in the links property "categories" of "control"
    And "a_control_assertion" is in the links property "assertions" of "control"
