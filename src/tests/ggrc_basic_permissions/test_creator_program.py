import unittest
from tests.ggrc import TestCase
from ggrc.models import all_models
from tests.ggrc.api_helper import Api
from tests.ggrc.generator import Generator
from tests.ggrc.generator import GgrcGenerator


class TestCreatorProgram(TestCase):

  def setUp(self):
    TestCase.setUp(self)

    self.generator = Generator()
    self.api = Api()
    self.ggrc_generator = GgrcGenerator()
    self.maxDiff = None
    self._generate_users()
    self._init_roles()

  def _init_roles(self):
    response = self.api.get_query(all_models.Role, "")
    self.roles = {}
    for role in response.json.get('roles_collection').get('roles'):
      self.roles[role.get('name')] = role

  def _generate_users(self):
    users = [
        ('creator1', 'Creator'),
        ('creator2', 'Creator'),
        ('reader', 'Reader'),
        ('editor', 'ObjectEditor'),
        ('admin', 'gGRC Admin')]

    for (name, role) in users:
      _, user = self.ggrc_generator.generate_person(
          data={"name": name}, user_role=role)
      setattr(self, name, user)
      setattr(self, name + "_id", user.id)

  def test_creator_can_create_and_map_to_program(self):
    self.api.set_user(self.creator1)
    response = self.api.post(all_models.Program, {
        "program": {"title": "Test Program", "context": None},
    })
    program_id = response.json.get('program').get('id')
    context_id = response.json.get('program').get('context').get('id')
    self.assertEquals(response.status_code, 201)
    response = self.api.post(all_models.System, {
        "system": {"title": "Test System", "context": None},
    })
    system_id = response.json.get('system').get('id')
    self.assertEquals(response.status_code, 201)
    response = self.api.post(all_models.Relationship, {
        "relationship": {"source": {
            "id": program_id,
            "type": "Program"
        }, "destination": {
            "id": system_id,
            "type": "System"
        }, "context": None},
    })
    self.assertEquals(response.status_code, 201)

    # Check if creator2 can access program/mapped object
    self.api.set_user(self.creator2)
    response = self.api.get(all_models.Program, program_id)
    self.assertEquals(response.status_code, 403)
    response = self.api.get(all_models.System, system_id)
    self.assertEquals(response.status_code, 403)

    # Add program read access to Creator2
    self.api.set_user(self.creator1)
    response = self.api.post(all_models.ObjectPerson, {"object_person": {
        "person": {
            "id": self.creator2_id,
            "type": "Person",
            "href": "/api/people/{}".format(self.creator2_id),
        }, "personable": {
            "type": "Program",
            "href": "/api/programs/{}".format(program_id),
            "id": program_id,
        }, "context": {
            "type": "Context",
            "id": context_id,
            "href": "/api/contexts/{}".format(context_id)
        }},
    })
    self.api.set_user(self.creator2)
    response = self.api.get(all_models.Program, program_id)
    self.assertEquals(response.status_code, 403)
    response = self.api.get(all_models.System, system_id)
    self.assertEquals(response.status_code, 403)
    self.api.set_user(self.creator1)
    response = self.api.post(all_models.UserRole, {"user_role": {
        "person": {
            "id": self.creator2_id,
            "type": "Person",
            "href": "/api/people/{}".format(self.creator2_id),
        }, "role": {
            "type": "Role",
            "href": "/api/roles/{}".format(self.roles['ProgramReader']['id']),
            "id": self.roles['ProgramReader']['id'],
        }, "context": {
            "type": "Context",
            "id": context_id,
            "href": "/api/contexts/{}".format(context_id)
        }},
    })
    self.assertEquals(response.status_code, 201)


    # Check if creator2 can access program/mapped object
    self.api.set_user(self.creator2)
    response = self.api.get(all_models.Program, program_id)
    self.assertEquals(response.status_code, 200)
    response = self.api.get(all_models.System, system_id)
    self.assertEquals(response.status_code, 200)

if __name__ == '__main__':
  unittest.main()
