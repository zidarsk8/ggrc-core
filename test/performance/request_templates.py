# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module with actual request payload from the front-end used for testing."""

# pylint: disable=too-many-lines,invalid-name

query_cycle_task_count_and_overdue = [
    {
        "object_name": "CycleTaskGroupObjectTask",
        "type": "count",
                "filters": {
                    "expression": {
                        "object_name": "Person",
                        "op": {"name": "owned"},
                        "ids": ["1"]
                    },
                    "keys":[],
                    "order_by":{"keys": [], "order":"", "compare":None}
                }
    }, {
        "object_name": "CycleTaskGroupObjectTask",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Person",
                    "op": {"name": "owned"},
                    "ids": ["1"]
                },
                "op":{"name": "AND"},
                "right": {
                    "op": {"name": "<"},
                    "left": "task due date",
                            "right": "2017-06-26"
                }
            },
            "keys": [None]
        },
        "type":"count"
    }
]

query_all_original_related_ids = [
    {
        "object_name": "Control",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Product",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "OrgGroup",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Vendor",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Risk",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Facility",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Process",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Clause",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Section",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "DataAsset",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "AccessGroup",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "System",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Contract",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Standard",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Objective",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Regulation",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Threat",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Policy",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    },
    {
        "object_name": "Market",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "type":"ids"
    }
]


query_assessment_relevant_count = [
    {
        "object_name": "Assessment",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {"name": "relevant"},
                "ids": ["5"]
            },
            "keys":[],
            "order_by":{"keys": [], "order":"", "compare":None
                        }
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{"name": "AND"},
                "right": {
                    "left": "child_type",
                            "op": {"name": "="},
                            "right": "AccessGroup"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Audit",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {"name": "relevant"},
                "ids": ["5"]
            },
            "keys":[],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Clause"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Contract"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Control"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "DataAsset"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Facility"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Market"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Objective"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "OrgGroup"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Policy"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Process"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Product"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Regulation"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Risk"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Section"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Standard"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "System"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Threat"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": ["5"]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                            "op": {
                                "name": "="
                            },
                    "right": "Vendor"
                }
            },
            "keys": [
                "child_type"
            ],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "Workflow",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {"name": "relevant"},
                "ids": ["5"]
            },
            "keys":[],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }, {
        "object_name": "CycleTaskGroupObjectTask",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {"name": "relevant"},
                "ids": ["5"]
            },
            "keys":[],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }
]

query_aud_snap_comment_document = [
    {
        "object_name": "Audit",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "limit":[
            0,
            1
        ],
        "fields":[
            "id",
            "type",
            "title",
            "context"
        ]
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "fields":[

        ]
    },
    {
        "object_name": "Comment",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {
                    "name": "relevant"
                },
                "ids": [
                    "5"
                ]
            },
            "keys":[

            ],
            "order_by":{
                "keys": [

                ],
                "order":"",
                "compare":None
            }
        },
        "order_by":[
            {
                "name": "created_at",
                "desc": True
            }
        ],
        "fields": [

        ]
    },
    {
        "object_name": "Document",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": [
                        "5"
                    ]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "document_type",
                    "op": {
                        "name": "="
                    },
                    "right": "EVIDENCE"
                }
            },
            "keys": [
                None
            ]
        },
        "order_by":[
            {
                "name": "created_at",
                "desc": True
            }
        ],
        "fields": [

        ]
    },
    {
        "object_name": "Document",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": [
                        "5"
                    ]
                },
                "op":{
                    "name": "AND"
                },
                "right": {
                    "left": "document_type",
                    "op": {
                        "name": "="
                    },
                    "right": "URL"
                }
            },
            "keys": [
                None
            ]
        },
        "order_by":[
            {
                "name": "created_at",
                "desc": True
            }
        ],
        "fields": [

        ]
    }
]

query_assessment_relevant_to_person = [
    {
        "object_name": "Assessment",
        "filters": {
            "expression": {
                "object_name": "Person",
                "op": {"name": "relevant"},
                "ids": ["1"]
            },
            "keys":[],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "type":"count"
    }
]

query_not_started_in_progress_relevant_user = [
    {
        "object_name": "Assessment",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Person",
                    "op": {"name": "relevant"},
                    "ids": ["1"]
                },
                "op":{"name": "AND"},
                "right": {
                    "left": {
                        "left": "status",
                                "op": {"name": "="},
                                "right": "Not Started"
                    },
                    "op": {"name": "OR"},
                    "right": {
                        "left": "status",
                                "op": {"name": "="},
                                "right": "In Progress"
                    }
                }
            },
            "keys": ["status"],
            "order_by": {"keys": [], "order":"", "compare":None}
        },
        "limit": [0, 10]
    }
]
