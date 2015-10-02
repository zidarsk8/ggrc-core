# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc.utils import merge_dicts
from ggrc.utils import merge_dict
from ggrc.utils import get_mapping_rules
from tests.ggrc import TestCase


class TestUtilsDictFunctions(TestCase):

  def test_mapping_rules(self):
    """ Test that all mappings go both ways """
    mappings = get_mapping_rules()
    verificationErrors = []

    # Special cases in mappings as defined in utils.py:
    audit_mappings = ["Control", "DataAsset", "Facility", "Market", "OrgGroup",
                      "Process", "Product", "Program", "Project", "System",
                      "Vendor", "AccessGroup"]
    section_mappings = ["Policy", "Regulation", "Standard"]

    for object_name, object_mappings in mappings.items():
      for mapping in object_mappings:
        try:
          if mapping == "Request":
            self.assertNotIn(mapping, mappings)
          elif mapping == "Audit" and object_name in audit_mappings:
            self.assertNotIn(
                object_name, mappings[mapping],
                "{} found in {} mappings".format(object_name, mapping)
            )
          elif mapping == "Section" and object_name in section_mappings:
            self.assertNotIn(
                object_name, mappings[mapping],
                "{} found in {} mappings".format(object_name, mapping)
            )
          else:
            self.assertIn(
                mapping, mappings,
                "- {} is not in the mappings dict".format(mapping)
            )
            self.assertIn(
                object_name, mappings[mapping],
                "{} not found in {} mappings".format(object_name, mapping)
            )
        except AssertionError as e:
          verificationErrors.append(str(e))

    verificationErrors.sort()
    self.assertEqual(verificationErrors, [])

  def test_merge_dict(self):
    dict1 = {
        "a": {
            "b": {
                "c": 1,
                "d": {
                    "e": 2
                }
            }
        }
    }
    dict2 = {
        "a": {
            "b": {
                "c": 1,
                "f": {
                    "e": 2
                }
            },
            "g": 3
        },
        "h": 4
    }

    result = merge_dict(dict1, dict2)

    self.assertEquals(result["h"], 4)
    self.assertEquals(result["a"]["b"]["c"], 1)
    self.assertEquals(result["a"]["b"]["d"]["e"], 2)
    self.assertEquals(result["a"]["b"]["f"]["e"], 2)

  def test_merge_dicts(self):
    dict1 = {
        "a": {
            "b": {
                "c": 1,
                "d": {
                    "e": 2
                }
            }
        }
    }
    dict2 = {
        "a": {
            "b": {
                "c": 1,
                "f": {
                    "e": 2
                }
            },
            "g": 3
        },
        "h": 4
    }
    dict3 = {
        "a": {
            "eeb": {
                "c": 1,
                "f": {
                    "e": 2
                }
            },
            "g": 3
        },
        "h": 4
    }

    result = merge_dicts(dict1, dict2, dict3)

    self.assertIn("a", result)
    self.assertIn("h", result)
    self.assertIn("eeb", result["a"])
    self.assertIn("g", result["a"])
    self.assertIn("b", result["a"])
    self.assertIn("c", result["a"]["b"])
    self.assertIn("d", result["a"]["b"])
    self.assertIn("e", result["a"]["b"]["d"])
    self.assertEquals(result["a"]["b"]["f"]["e"], 2)

  def test_emails_dict(self):

    aggregate_data = {
        "all@emails.me": {
            "cycle_started": {
                "2": {
                    "custom_message": "",
                    "cycle_title": "monthly",
                    "cycle_url": "http://a.com",
                    "manually": False,
                    "my_tasks": {
                        "2": {
                            "cycle_task_url": "http://a.com",
                            "end_date": "05/18/2015",
                            "fuzzy_due_in": "in 5 days",
                            "object_title": "",
                            "title": "all emails task"
                        }
                    },
                    "workflow_owners": {
                        "1": {
                            "email": "user@example.com",
                            "id": 1,
                            "name": "Example User"
                        }
                    }
                }
            },
            "force_notifications": {
                "8": False,
                "9": False,
                "12": False
            },
            "user": {
                "email": "all@emails.me",
                "id": 2,
                "name": "All Emails"
            }
        },
        "default@emails.me": {
            "cycle_started": {
                "2": {
                    "custom_message": "",
                    "cycle_title": "monthly",
                    "cycle_url": "http://a.com",
                    "manually": False,
                    "workflow_owners": {
                        "1": {
                            "email": "user@example.com",
                            "id": 1,
                            "name": "Example User"
                        }
                    }
                }
            },
            "force_notifications": {
                "8": False
            },
            "user": {
                "email": "default@emails.me",
                "id": 4,
                "name": "Defaullt Emails"
            }
        },
        "digest@only.me": {
            "cycle_started": {
                "2": {
                    "custom_message": "",
                    "cycle_title": "monthly",
                    "cycle_url": "http://a.com",
                    "manually": False,
                    "workflow_owners": {
                        "1": {
                            "email": "user@example.com",
                            "id": 1,
                            "name": "Example User"
                        }
                    }
                }
            },
            "force_notifications": {
                "8": False
            },
            "user": {
                "email": "digest@only.me",
                "id": 3,
                "name": "Digest Only"
            }
        },
        "user@example.com": {
            "cycle_started": {
                "1": {
                    "custom_message": "",
                    "cycle_title": "onetime",
                    "cycle_url": "http://a.com",
                    "manually": True,
                    "my_task_groups": {
                        "1": {
                            "1": {
                                "cycle_task_url": "http://a.com",
                                "end_date": "05/29/2015",
                                "fuzzy_due_in": "in 16 days",
                                "object_title": "",
                                "title": "task"
                            }
                        }
                    },
                    "my_tasks": {
                        "1": {
                            "cycle_task_url": "http://a.com",
                            "end_date": "05/29/2015",
                            "fuzzy_due_in": "in 16 days",
                            "object_title": "",
                            "title": "task"
                        }
                    },
                    "workflow_owners": {
                        "1": {
                            "email": "user@example.com",
                            "id": 1,
                            "name": "Example User"
                        }
                    },
                    "workflow_tasks": {
                        "1": {
                            "cycle_task_url": "http://a.com",
                            "end_date": "05/29/2015",
                            "fuzzy_due_in": "in 16 days",
                            "object_title": "",
                            "title": "task"
                        }
                    }
                },
                "2": {
                    "custom_message": "",
                    "cycle_title": "monthly",
                    "cycle_url": "http://a.com",
                    "manually": False,
                    "my_task_groups": {
                        "2": {
                            "2": {
                                "cycle_task_url": "http://a.com",
                                "end_date": "05/18/2015",
                                "fuzzy_due_in": "in 5 days",
                                "object_title": "",
                                "title": "all emails task"
                            }
                        }
                    },
                    "workflow_owners": {
                        "1": {
                            "email": "user@example.com",
                            "id": 1,
                            "name": "Example User"
                        }
                    },
                    "workflow_tasks": {
                        "2": {
                            "cycle_task_url": "http://a.com",
                            "end_date": "05/18/2015",
                            "fuzzy_due_in": "in 5 days",
                            "object_title": "",
                            "title": "all emails task"
                        }
                    }
                }
            },
            "force_notifications": {
                "1": False,
                "2": False,
                "5": False,
                "8": False,
                "9": False,
                "12": False
            },
            "user": {
                "email": "user@example.com",
                "id": 1,
                "name": "Example User"
            }
        }
    }

    user_data = {
        "user@example.com": {
            "cycle_started": {
                "2": {
                    "my_task_groups": {
                        "2": {
                            "3": {
                                "cycle_task_url": "http://a.com",
                                "end_date": "05/18/2015",
                                "fuzzy_due_in": "in 5 days",
                                "object_title": "",
                                "title": "no emails task"
                            }
                        }
                    },
                    "workflow_tasks": {
                        "3": {
                            "cycle_task_url": "http://a.com",
                            "end_date": "05/18/2015",
                            "fuzzy_due_in": "in 5 days",
                            "object_title": "",
                            "title": "no emails task"
                        }
                    }
                }
            },
            "force_notifications": {
                "15": False
            },
            "user": {
                "email": "user@example.com",
                "id": 1,
                "name": "Example User"
            }
        }
    }

    merged_data = merge_dict(aggregate_data, user_data)

    self.assertNotIn(
        "3", merged_data["all@emails.me"]["cycle_started"]["2"]["my_tasks"])
