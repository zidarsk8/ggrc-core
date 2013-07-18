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
    Given existing Role named "ProgramReader"
    And a new "ggrc_basic_permissions.models.UserRole" named "role_assignment" is created from json
    """
    {
      "role": {
        "id": {{context.ProgramReader.value['role']['id']}},
        "type": "Role"
        },
      "user_email": "example.user1@example.com",
      "context": {
        "id": {{context.private_program.value['program']['context']['id']}},
        "type": "Context"
        }
    }
    """
    Given "role_assignment" is POSTed to its collection
    Given the current user
      """
      { "email": "example.user1@example.com", "name": "Example User1" }
      """
    Then GET of "private_program" is allowed
    Then PUT of "private_program" is forbidden
    Then DELETE of "private_program" is forbidden
    
