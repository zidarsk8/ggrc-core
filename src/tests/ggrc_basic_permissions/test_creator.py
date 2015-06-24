import unittest
from tests.ggrc import TestCase
from ggrc.models import get_model
from ggrc.models import all_models
from tests.ggrc.api_helper import Api
from tests.ggrc.generator import Generator
from tests.ggrc.generator import GgrcGenerator


class TestCreator(TestCase):
  def setUp(self):
    TestCase.setUp(self)

    self.generator = Generator()
    self.api = Api()
    self.ggrc_generator = GgrcGenerator()
    self.maxDiff = None
    self._generate_users()

  def _generate_users(self):
    users = [('creator', 'Creator'), ('admin', 'gGRC Admin')]
    for (name, role) in users:
      _, user = self.ggrc_generator.generate_person(
          data={"name": name}, user_role=role)
      setattr(self, name, user)

  def test_creator_can_crud_basic_models(self):
    self.api.set_user(self.creator)
    all_errors = []
    base_models = set([
        'Control', 'ControlAssessment', 'DataAsset', 'Contract',
        'Policy', 'Regulation', 'Standard', 'Document', 'Facility',
        'Market', 'Objective', 'OrgGroup', 'Vendor', 'Product',
        'Clause', 'System', 'Process', 'Issue', 'Project'
    ])
    for model_singular in base_models:
      try:
        model = get_model(model_singular)
        table_singular = model._inflector.table_singular
        table_plural = model._inflector.table_plural
        # Test POST creation
        response = self.api.post(model, {
            table_singular: {
                "title": model_singular,
                "context": None,
                "reference_url": "ref",
                "contact": {
                    "type": "Person",
                    "id": self.creator.id,
                },
            },
        })
        if response.status_code != 201:
          all_errors.append("{} post creation failed {} {}".format(
              model_singular, response.status, response.data))
          continue

        # Test GET when not owner
        obj_id = response.json.get(table_singular).get('id')
        response = self.api.get(model, obj_id)
        if response.status_code != 403:  # we are not onwers yet
          all_errors.append(
              "{} can retrieve object if not owner".format(model_singular))
          continue
        response = self.api.get_collection(model, obj_id)
        collection = response.json.get(
            "{}_collection".format(table_plural)).get(table_plural)
        if len(collection) != 0:
          all_errors.append(
              "{} can retrieve object if not owner (collection)".format(model_singular))
          continue
        # Become an owner
        response = self.api.post(all_models.ObjectOwner, {"object_owner": {
            "person": {
                "id": self.creator.id,
                "type": "Person",
            }, "ownable": {
                "type": model_singular,
                "id": obj_id
            }, "context": None},
        })
        if response.status_code != 201:
          all_errors.append("{} can't create owner {}.".format(
              model_singular, response.status))
          continue

        # Test GET when owner
        response = self.api.get(model, obj_id)
        if response.status_code != 200:
          all_errors.append("{} can't GET object {}".format(
              model_singular, response.status))
          continue

        # Test GET collection when owner
        response = self.api.get_collection(model, obj_id)
        collection = response.json.get(
            "{}_collection".format(table_plural)).get(table_plural)
        if len(collection) == 0:
          all_errors.append(
              "{} cannot retrieve object even if owner (collection)".format(model_singular))
          continue
      except:
          all_errors.append("{} exception thrown".format(model_singular))
          raise
    self.assertEquals(all_errors, [])

  def test_creator_search(self):
    self.api.set_user(self.admin)
    self.api.post(all_models.Regulation, {
        "regulation": {"title": "Admin regulation", "context": None},
    })
    self.api.set_user(self.creator)
    response = self.api.post(all_models.Policy, {
        "policy": {"title": "Creator Policy", "context": None},
    })
    obj_id = response.json.get('policy').get('id')
    self.api.post(all_models.ObjectOwner, {"object_owner": {
        "person": {
            "id": self.creator.id,
            "type": "Person",
        }, "ownable": {
            "type": "Policy",
            "id": obj_id,
        }, "context": None},
    })
    response, _ = self.api.search('Regulation,Policy')
    entries = response.json['results']['entries']
    self.assertEquals(len(entries), 1)
    self.assertEquals(entries[0]['type'], "Policy")
    response, _ = self.api.search('Regulation,Policy', counts=True)
    self.assertEquals(response.json['results']['counts']['Policy'], 1)
    self.assertEquals(
        response.json['results']['counts'].get('Regulation'), None)

  def _get_count(self, obj):
    response, _ = self.api.search(obj, counts=True)
    return response.json['results']['counts'].get(obj)

  def test_creator_should_see_all_users(self):
    self.api.set_user(self.admin)
    admin_count = self._get_count('Person')
    self.api.set_user(self.creator)
    creator_count = self._get_count('Person')
    self.assertEquals(admin_count, creator_count)

  def test_creator_cannot_become_owner(self):
    self.api.set_user(self.admin)
    _, obj = self.generator.generate(all_models.Regulation, "regulation", {
        "regulation": {"title": "Test regulation", "context": None},
    })
    self.api.set_user(self.creator)
    response = self.api.post(all_models.ObjectOwner, {"object_owner": {
        "person": {
            "id": self.creator.id,
            "type": "Person",
        }, "ownable": {
            "type": "Regulation",
            "id": obj.id,
        }, "context": None},
    })
    self.assertEquals(response.status_code, 403)

if __name__ == '__main__':
  unittest.main()
