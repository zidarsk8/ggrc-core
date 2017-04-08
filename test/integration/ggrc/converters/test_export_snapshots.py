# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for snapshot export."""


from ggrc import models
from integration.ggrc import TestCase
from integration.ggrc.models import factories


class TestExportSnapshots(TestCase):
  """Tests basic snapshot export."""

  def setUp(self):
    super(TestExportSnapshots, self).setUp()
    self.client.get("/login")
    self.headers = {
        "Content-Type": "application/json",
        "X-Requested-By": "GGRC",
        "X-export-view": "blocks",
    }

  def test_simple_export(self):
    """Test simple empty snapshot export."""
    search_request = [{
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": "child_type",
                "op": {"name": "="},
                "right": "Control",
            },
        },
    }]
    parsed_data = self.export_parsed_csv(search_request)["Snapshot"]
    self.assertEqual(parsed_data, [])

  @staticmethod
  def _get_cav(control, cad_name):
    """Get proper CA value for a given CAD name."""
    for cav in control.custom_attribute_values:
      if cav.custom_attribute.title == cad_name:
        if cav.custom_attribute.attribute_type == "Checkbox":
          return u"yes" if int(cav.attribute_value) else u"no"
        elif cav.custom_attribute.attribute_type == "Map:Person":
          return cav.attribute_object.email if cav.attribute_object else u""
        elif cav.custom_attribute.attribute_type == "Date":
          parts = cav.attribute_value.split("-")
          return u"{}/{}/{}".format(parts[1], parts[2], parts[0])
        else:
          return cav.attribute_value
    return u""

  def test_full_export(self):
    """Test exporting of a single full control snapshot."""
    cad = factories.CustomAttributeDefinitionFactory
    cad(title="date", definition_type="control", attribute_type="Date")
    cad(title="checkbox", definition_type="control", attribute_type="Checkbox")
    cad(title="person", definition_type="control", attribute_type="Map:Person")
    cad(title="RT", definition_type="control", attribute_type="Rich Text")
    cad(title="dropdown", definition_type="control", attribute_type="Dropdown",
        multi_choice_options="one,two,three,four,five")
    self.import_file("control_snapshot_data_single.csv")
    # Duplicate import because we have a bug in logging revisions and this
    # makes sure that the fixture created properly.
    self.import_file("control_snapshot_data_single.csv")

    controls = models.Control.query.all()
    audit = factories.AuditFactory()
    snapshots = self._create_snapshots(audit, controls)

    control_dicts = {
        control.slug: {
            # normal fields
            "Admin": "\n".join(owner.email for owner in control.owners),
            "Code": "*" + control.slug,
            "Revision Date": unicode(snapshot.revision.created_at),
            "Control URL": control.url,
            "Description": control.description,
            "Effective Date": control.start_date.strftime("%m/%d/%Y"),
            "Fraud Related": u"yes" if control.fraud_related else u"no",
            "Frequency": control.verify_frequency.display_name,
            "Kind/Nature": control.kind.display_name,
            "Notes": control.notes,
            "Primary Contact": control.contact.email,
            "Principal Assignee": control.principal_assessor.email,
            "Reference URL": control.reference_url,
            "Review State": control.os_state,
            "Secondary Assignee": control.secondary_assessor.email,
            "Secondary Contact": control.secondary_contact.email,
            "Significance": u"key" if control.key_control else u"non-key",
            "State": control.status,
            "Stop Date": control.end_date.strftime("%m/%d/%Y"),
            "Test Plan": control.test_plan,
            "Title": control.title,
            "Type/Means": control.means.display_name,
            # Custom attributes
            "RT": self._get_cav(control, "RT"),
            "checkbox": self._get_cav(control, "checkbox"),
            "date": self._get_cav(control, "date"),
            "dropdown": self._get_cav(control, "dropdown"),
            "person": self._get_cav(control, "person"),
            # Special snapshot export fields
            "Audit": audit.slug,

            # Fields that are not included in snapshots - Known bugs.
            "Assertions": u"",  # "\n".join(c.name for c in control.assertions)
            "Categories": u"",  # "\n".join(c.name for c in control.categories)
        }
        for snapshot, control in zip(snapshots, controls)
    }

    search_request = [{
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": "child_type",
                "op": {"name": "="},
                "right": "Control",
            },
        },
    }]
    parsed_data = self.export_parsed_csv(search_request)["Control Snapshot"]
    parsed_dict = {line["Code"]: line for line in parsed_data}

    self.assertEqual(
        parsed_dict["*Control 1"],
        control_dicts["Control 1"],
    )
