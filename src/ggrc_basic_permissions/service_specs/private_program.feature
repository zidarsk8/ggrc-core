Feature: Private Programs

  Background:
    Given service description

  Scenario: A logged in user can create a private program that another logged in user cannot see or otherwise access.
    Given the current user
      """
      { "email": "secretive.user@example.com", "name": "Secretive User" }
      """
    Given a new "Program" named "private_program"
    And "private_program" property "private" is literal "True"
    And "private_program" is POSTed to its collection
    Then GET of "private_program" is allowed
    Then PUT of "private_program" is allowed
    Then GET of "private_program" is allowed
    Given the current user
      """
      { "email": "example.user1@example.com", "name": "Example User1" }
      """
    Then GET of "private_program" is forbidden
    Then PUT of "private_program" is forbidden
    Then DELETE of "private_program" is forbidden
    Given the current user
      """
      { "email": "secretive.user@example.com", "name": "Secretive User" }
      """
    Then GET of "private_program" is allowed
    Then DELETE of "private_program" is allowed

  Scenario: A user can create a private program and assign another user the ProgramReader role in that program's context granting them the ability to GET the program.
    Given the current user
      """
      { "email": "secretive.user@example.com", "name": "Secretive User" }
      """
    Given a new "Program" named "private_program"
    And "private_program" property "private" is literal "True"
    And "private_program" is POSTed to its collection
    Then GET of "private_program" is allowed
    Given a user with email "example.user2@example.com" as "person"
    Given existing Role named "ProgramReader"
    And a new "ggrc_basic_permissions.models.UserRole" named "role_assignment" is created from json
    """
    {
      "role": {
        "id": {{context.ProgramReader.value['role']['id']}},
        "type": "Role"
        },
      "person": {
        "id": {{context.person['id']}},
        "type": "Person"
      },
      "context": {
        "id": {{context.private_program.value['program']['context']['id']}},
        "type": "Context"
        }
    }
    """
    And "role_assignment" is POSTed to its collection
    And the current user
      """
      { "email": "example.user2@example.com", "name": "Example User1" }
      """
    Then GET of "private_program" is allowed
    Then PUT of "private_program" is forbidden
    Then DELETE of "private_program" is forbidden

  Scenario: Admin users can see the private programs created by other, non-admin, users.
    Given the current user
      """
      { "email": "secretive.user@example.com", "name": "Secretive User" }
      """
    Given a new "Program" named "private_program"
    And "private_program" property "private" is literal "True"
    And "private_program" is POSTed to its collection
    When GET of the resource "private_program"
    Given the current user
      """
      { "email": "example.admin@example.com", "name": "Jo Admin",
        "permissions": {
          "__GGRC_ADMIN__": { "__GGRC_ALL__": [0] }
        }
      }
      """
    When Get of "Program" collection
    Then "private_program" is in collection
