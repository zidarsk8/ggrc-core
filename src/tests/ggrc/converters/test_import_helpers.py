# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from os.path import abspath, dirname, join

from ggrc import models
from ggrc.converters.import_helper import get_object_column_definitions
from ggrc.models import CustomAttributeDefinition
from tests.ggrc import TestCase
from tests.ggrc.api_helper import Api

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'example_csvs/')


def generate_custom_attr(definition_type, title, attribute_type="Text",
                         mandatory=False, helptext="", multi_choice=""):
  api = Api()
  custom_attr = {
      "custom_attribute_definition": {
          "title": title,
          "custom_attribute_definitions": [],
          "custom_attributes": {},
          "definition_type": definition_type,
          "modal_title": title,
          "attribute_type": attribute_type,
          "mandatory": mandatory,
          "helptext": helptext,
          "placeholder": "",
          "context": {"id": None},
          "multi_choice_options": multi_choice
      }
  }
  api.post(CustomAttributeDefinition, custom_attr)


class TestCustomAttributesDefinitions(TestCase):

  def test_policy_definitions(self):
    generate_custom_attr("policy", "My Attribute")
    generate_custom_attr("policy", "Mandatory Attribute", mandatory=True)
    definitions = get_object_column_definitions(models.Policy)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Code",
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Policy URL",
        "Reference URL",
        "Kind/Type",
        "Effective Date",
        "Stop Date",
        "State",
        "My Attribute",
        "Mandatory Attribute",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])
    self.assertTrue(mandatory["Mandatory Attribute"])

  def test_program_definitions(self):
    """ test custom attribute headers for Program """
    generate_custom_attr("program", "My Attribute")
    generate_custom_attr("program", "Mandatory Attribute", mandatory=True)
    generate_custom_attr(
        "program", "Choose",
        mandatory=True,
        attribute_type="Dropdown",
        multi_choice="hello,world,what's,up"
    )
    definitions = get_object_column_definitions(models.Program)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Privacy",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Program URL",
        "Reference URL",
        "Kind/Type",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
        "My Attribute",
        "Mandatory Attribute",
        "Choose",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])
    self.assertTrue(mandatory["Mandatory Attribute"])
    self.assertTrue(mandatory["Choose"])


class TestGetObjectColumnDefinitions(TestCase):

  """
  Test default column difinitions for all objcts

  order of these test functions is the same as the objects in LHN
  """

  def test_program_definitions(self):
    """ test default headers for Program """
    definitions = get_object_column_definitions(models.Program)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Privacy",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Program URL",
        "Reference URL",
        "Kind/Type",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_audit_definitions(self):
    """ test default headers for Audit """
    definitions = get_object_column_definitions(models.Audit)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Program",
        "Title",
        "Description",
        "Internal Audit Lead",
        "Status",
        "Planned Start Date",
        "Planned End Date",
        "Planned Report Period from",
        "Planned Report Period to",
        "Auditors",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])
    self.assertTrue(mandatory["Internal Audit Lead"])

  def test_control_assessment_definitions(self):
    """ test default headers for Control Assessment """
    definitions = get_object_column_definitions(models.ControlAssessment)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Test Plan",
        "Control",
        "Audit",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Assessment URL",
        "Reference URL",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
        "Conclusion: Design",
        "Conclusion: Operation",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])
    self.assertTrue(mandatory["Control"])
    self.assertTrue(mandatory["Audit"])

  def test_issue_definitions(self):
    """ test default headers for Issue """
    definitions = get_object_column_definitions(models.Issue)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Test Plan",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Issue URL",
        "Reference URL",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_regulation_definitions(self):
    """ test default headers for Regulation """
    definitions = get_object_column_definitions(models.Regulation)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Regulation URL",
        "Reference URL",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_policy_definitions(self):
    """ test default headers for Policy """
    definitions = get_object_column_definitions(models.Policy)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Policy URL",
        "Reference URL",
        "Kind/Type",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_standard_definitions(self):
    """ test default headers for Standard """
    definitions = get_object_column_definitions(models.Standard)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Standard URL",
        "Reference URL",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_contract_definitions(self):
    """ test default headers for Contract """
    definitions = get_object_column_definitions(models.Contract)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Contract URL",
        "Reference URL",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_clause_definitions(self):
    """ test default headers for Clause """
    definitions = get_object_column_definitions(models.Clause)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Clause URL",
        "Reference URL",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_section_definitions(self):
    """ test default headers for Section """
    definitions = get_object_column_definitions(models.Section)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Text of Section",
        "Notes",
        "Policy / Regulation / Standard",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Section URL",
        "Reference URL",
        "Code",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_control_definitions(self):
    """ test default headers for Control """
    definitions = get_object_column_definitions(models.Control)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Test Plan",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Control URL",
        "Reference URL",
        "Code",
        "Kind/Nature",
        "Fraud Related",
        "Significance",
        "Type/Means",
        "Effective Date",
        "Stop Date",
        "Frequency",
        "Assertions",
        "Categories",
        "Principal Assessor",
        "Secondary Assessor",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_objective_definitions(self):
    """ test default headers for Objective """
    definitions = get_object_column_definitions(models.Objective)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Objective URL",
        "Reference URL",
        "Code",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_person_definitions(self):
    """ test default headers for Person """
    definitions = get_object_column_definitions(models.Person)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Name",
        "Email",
        "Company",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Email"])

  def test_org_group_definitions(self):
    """ test default headers for OrgGroup """
    definitions = get_object_column_definitions(models.OrgGroup)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Org Group URL",
        "Reference URL",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_vendor_definitions(self):
    """ test default headers for Vendor """
    definitions = get_object_column_definitions(models.Vendor)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Vendor URL",
        "Reference URL",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_system_definitions(self):
    """ test default headers for System """
    definitions = get_object_column_definitions(models.System)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "System URL",
        "Reference URL",
        "Code",
        "Network Zone",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_process_definitions(self):
    """ test default headers for Process """
    definitions = get_object_column_definitions(models.Process)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Process URL",
        "Reference URL",
        "Code",
        "Network Zone",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_data_asset_definitions(self):
    """ test default headers for DataAsset """
    definitions = get_object_column_definitions(models.DataAsset)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Data Asset URL",
        "Reference URL",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_product_definitions(self):
    """ test default headers for Product """
    definitions = get_object_column_definitions(models.Product)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Product URL",
        "Reference URL",
        "Code",
        "Kind/Type",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_project_definitions(self):
    """ test default headers for Project """
    definitions = get_object_column_definitions(models.Project)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Project URL",
        "Reference URL",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_facility_definitions(self):
    """ test default headers for Facility """
    definitions = get_object_column_definitions(models.Facility)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Facility URL",
        "Reference URL",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])

  def test_market_definitions(self):
    """ test default headers for Market """
    definitions = get_object_column_definitions(models.Market)
    display_names = set([val["display_name"] for val in definitions.values()])
    expected_names = set([
        "Title",
        "Description",
        "Notes",
        "Owner",
        "Primary Contact",
        "Secondary Contact",
        "Market URL",
        "Reference URL",
        "Code",
        "Effective Date",
        "Stop Date",
        "State",
    ])
    self.assertEquals(expected_names, display_names)
    mandatory = {val["display_name"]: val["mandatory"]
                 for val in definitions.values()}
    self.assertTrue(mandatory["Title"])
