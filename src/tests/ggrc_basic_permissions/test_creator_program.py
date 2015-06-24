import unittest
from tests.ggrc import TestCase
from ggrc.models import all_models
from tests.ggrc.api_helper import Api
from tests.ggrc.generator import Generator
from tests.ggrc.generator import GgrcGenerator
from ggrc import db


class TestCreatorProgram(TestCase):

  def setUp(self):
    TestCase.setUp(self)
    self.generator = Generator()
    self.api = Api()
    self.ggrc_generator = GgrcGenerator()
    self.maxDiff = None
    self._generate_users()
    self._init_roles()
    self.init_test_cases()
    self.objects = {}

  def delete(self, obj):
    return self.api.delete(obj, obj.id).status_code

  def get(self, obj):
    return self.api.get(obj.__class__, obj.id).status_code

  def put(self, obj):
    response = self.api.get(obj.__class__, obj.id)
    if response.status_code == 200:
      return self.api.put(obj, response.json).status_code
    else:
      return response.status_code

  def _init_roles(self):
    response = self.api.get_query(all_models.Role, "")
    self.roles = {}
    for role in response.json.get("roles_collection").get("roles"):
      self.roles[role.get("name")] = role

  def _generate_users(self):
    users = [
        ("creator", "Creator"),
        ("notmapped", "Creator"),
        ("mapped", "Creator"),
        ("ProgramReader", "Creator"),
        ("ProgramEditor", "Creator"),
        ("ProgramOwner", "Creator")]
    self.people = {}
    for (name, role) in users:
      _, user = self.ggrc_generator.generate_person(
          data={"name": name}, user_role=role)
      self.people[name] = user

  def _init_objects_for_test_case(self, test_case_name):
    # Create a program
    test_case = self.test_cases[test_case_name]
    creator = self.people.get('creator')
    self.api.set_user(creator)
    random_title = self.ggrc_generator.random_str()
    response = self.api.post(all_models.Program, {
        "program": {"title": random_title, "context": None},
    })
    self.assertEquals(response.status_code, 201)
    context_id = response.json.get("program").get("context").get("id")
    program_id = response.json.get("program").get("id")
    self.objects["program"] = all_models.Program.query.get(program_id)
    # Create an object:
    response = self.api.post(all_models.System, {
        "system": {"title": random_title, "context": None},
    })
    self.assertEquals(response.status_code, 201)
    system_id = response.json.get("system").get("id")
    self.objects["mapped_object"] = all_models.System.query.get(system_id)
    # Map Object to Program
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

    # Map people to Program:
    if test_case_name != "notmapped":
      person = self.people.get(test_case_name)
      response = self.api.post(all_models.ObjectPerson, {"object_person": {
          "person": {
              "id": person.id,
              "type": "Person",
              "href": "/api/people/{}".format(person.id),
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

    # Add roles to mapped users:
    if "program_role" in test_case:
      person = self.people.get(test_case_name)
      role = self.roles[test_case["program_role"]]
      response = self.api.post(all_models.UserRole, {"user_role": {
          "person": {
              "id": person.id,
              "type": "Person",
              "href": "/api/people/{}".format(person.id),
          }, "role": {
              "type": "Role",
              "href": "/api/roles/{}".format(role["id"]),
              "id": role["id"],
          }, "context": {
              "type": "Context",
              "id": context_id,
              "href": "/api/contexts/{}".format(context_id)
          }},
      })
      self.assertEquals(response.status_code, 201)

  def test_creator_program_roles(self):
    # Check permissions based on test_cases:
    self.errors = []
    for test_case in self.test_cases:
      self._init_objects_for_test_case(test_case)
      person = self.people.get(test_case)
      objects = self.test_cases.get(test_case).get('objects')
      self.api.set_user(person)
      for obj in ("mapped_object", "program"):
        actions = objects[obj]
        for action in ("get", "put", "delete"):
          # reset sesion:
          db.session.commit()
          func = getattr(self, action)
          if test_case == 'ProgramEditor' and action == "delete":
            res = func(self.objects[obj])
          else:
            res = func(self.objects[obj])
          if res != actions[action]:
            self.errors.append(
                "{}: Tried {} on {}, but received {} instead of {}".format(
                    test_case, action, obj, res, actions[action]))
    self.assertEquals(self.errors, [])

  def init_test_cases(self):
    self.test_cases = {
        "notmapped": {
            "objects": {
                "program": {
                    "get": 403,
                    "put": 403,
                    "delete": 403
                },
                "mapped_object": {
                    "get": 403,
                    "put": 403,
                    "delete": 403
                }
            }
        },
        "mapped": {
            "objects": {
                "program": {
                    "get": 403,
                    "put": 403,
                    "delete": 403
                },
                "mapped_object": {
                    "get": 403,
                    "put": 403,
                    "delete": 403
                }
            }
        },
        "ProgramReader": {
            "program_role": "ProgramReader",
            "objects": {
                "program": {
                    "get": 200,
                    "put": 403,
                    "delete": 403
                },
                "mapped_object": {
                    "get": 200,
                    "put": 403,
                    "delete": 403
                }
            }
        },
        "ProgramOwner": {
            "program_role": "ProgramOwner",
            "objects": {
                "program": {
                    "get": 200,
                    "put": 200,
                    "delete": 200
                },
                "mapped_object": {
                    "get": 200,
                    "put": 200,
                    "delete": 200,
                }
            }
        },
        "ProgramEditor": {
            "program_role": "ProgramEditor",
            "objects": {
                "program": {
                    "get": 200,
                    "put": 200,
                    "delete": 200
                },
                "mapped_object": {
                    "get": 200,
                    "put": 200,
                    "delete": 200
                }
            }
        },
    }

if __name__ == "__main__":
  unittest.main()
