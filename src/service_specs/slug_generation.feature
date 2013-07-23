Feature: Slugs should be generated when not provided

  Background:
    Given service description

  Scenario Outline: A Slugged resource is POSTed without a slug and a slug is generated.
    Given a new "<resource_type>" named "slugged_resource"
    And "slugged_resource" property "slug" is literal "None"
    And "slugged_resource" is POSTED to its collection
    When GET of the resource "slugged_resource"
    Then evaluate "context.slugged_resource.get('slug') is not None"
    And evaluate "context.slugged_resource.get('slug').startswith('<resource_type>')"

  Examples:
      | resource_type  |
      | Control        |
      | DataAsset      |
      | Directive      |
      | Facility       |
      | Help           |
      | Market         |
      | Objective      |
      | OrgGroup       |
      | Product        |
      | Program        |
      | Project        |
      | Risk           |
      | RiskyAttribute |
      | Section        |
      | System         |

  Scenario Outline: A Slugged resource is POSTed with a slug and that slug is preserved.
    Given a new "<resource_type>" named "slugged_resource"
    And "slugged_resource" property "slug" is "What a slug!"
    And "slugged_resource" is POSTed to its collection
    When GET of the resource "slugged_resource"
    Then evaluate "context.slugged_resource.get('slug') == 'What a slug!'"

  Examples:
      | resource_type  |
      | Control        |
      | DataAsset      |
      | Directive      |
      | Facility       |
      | Help           |
      | Market         |
      | Objective      |
      | OrgGroup       |
      | Product        |
      | Program        |
      | Project        |
      | Risk           |
      | RiskyAttribute |
      | Section        |
      | System         |


