Feature: Role CRUD

  Background:
    Given service description

  Scenario: Basic Role and UserRole CRUD using settings configured admin user
    Given current user is "{\"email\": \"example.admin@example.com\", \"name\": \"Jo Admin\"}"
    And a new Role named "role" is created from json
      """
      {
        "name": "Program Editor",
        "description": "simple program editor role.",
        "permissions": {
          "create": ["Program","Control"],
          "read":   ["Program","Control"],
          "update": ["Program","Control"],
          "delete": ["Control"]
          },
        "context_id": 0
      }
      """
    Then POST of "role" to its collection is allowed
    And GET of "role" is allowed

  #Scenario: A non-adminstrative user cannot access role information

  #Scenario: Use settings configured admin user to add other admin users

  #Scenario: Ensure permissions enforement on role and user role CRUD

