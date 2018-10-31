# -*- coding: utf-8 -*-

true = True
false = False
null = None

assessment_comment_payload = [
    {
        "comment": {
            "description": "<p>e</p>",
            "created_at": "2018-10-20T22:32:12.985Z",
            "modified_by": {
                "type": "Person",
                "id": 354
            },
            "comment": {
                "id": 1145,
                "type": "Context",
                "href": "/api/contexts/1145",
                "context_id": null
            },
            "send_notification": true,
            "context": {
                "id": 1145,
                "type": "Context",
                "href": "/api/contexts/1145",
                "context_id": null
            },
            "assignee_type": "Creators"
        }
    }
]

assessment_comment_map_payload = {
    "assessment": {
        "test_plan_procedure":
        true,
        "assessment_type":
        "Control",
        "status":
        "Not Started",
        "send_by_default":
        true,
        "recipients":
        "Assignees,Creators,Verifiers",
        "custom_attribute_definitions": [
            {
                "mandatory":
                false,
                "attribute_type":
                "Rich Text",
                "updated_at":
                "2017-11-14T10:02:18",
                "definition_type":
                "assessment",
                "helptext":
                "help",
                "placeholder":
                "",
                "id":
                4650,
                "multi_choice_options":
                null,
                "default_value":
                "",
                "modified_by": {
                    "context_id": null,
                    "href": "/api/people/393",
                    "type": "Person",
                    "id": 393
                },
                "title":
                "GCA_rich_text1_GCA_rich_text1_GCA_rich_text1_GCA_rich_text1_GCA_rich_text1_GCA_rich_text1_",
                "multi_choice_mandatory":
                null,
                "created_at":
                "2017-05-29T09:59:49",
                "definition_id":
                null,
                "context":
                null,
                "type":
                "CustomAttributeDefinition",
                "selfLink":
                "/api/custom_attribute_definitions/4650"
            },
            {
                "mandatory":
                false,
                "attribute_type":
                "Date",
                "updated_at":
                "2017-11-10T13:47:49",
                "definition_type":
                "assessment",
                "helptext":
                "",
                "placeholder":
                "",
                "id":
                4651,
                "multi_choice_options":
                null,
                "default_value":
                "",
                "modified_by": {
                    "context_id": null,
                    "href": "/api/people/393",
                    "type": "Person",
                    "id": 393
                },
                "title":
                "GCA_date_GCA_date_GCA_date_GCA_date_GCA_date_GCA_date_GCA_date_",
                "multi_choice_mandatory":
                null,
                "created_at":
                "2017-05-29T10:00:40",
                "definition_id":
                null,
                "context":
                null,
                "type":
                "CustomAttributeDefinition",
                "selfLink":
                "/api/custom_attribute_definitions/4651"
            },
            {
                "mandatory": false,
                "attribute_type": "Dropdown",
                "updated_at": "2017-09-14T07:32:11",
                "definition_type": "assessment",
                "helptext": "",
                "placeholder": "",
                "id": 4653,
                "multi_choice_options": "yes,no,other",
                "default_value": "",
                "modified_by": {
                    "context_id": null,
                    "href": "/api/people/328",
                    "type": "Person",
                    "id": 328
                },
                "title": "GCA_dropdown_GCA_dropdown_GCA_dropdown_GCA_dropdown",
                "multi_choice_mandatory": null,
                "created_at": "2017-05-29T10:01:32",
                "definition_id": null,
                "context": null,
                "type": "CustomAttributeDefinition",
                "selfLink": "/api/custom_attribute_definitions/4653"
            },
            {
                "mandatory": false,
                "attribute_type": "Map:Person",
                "updated_at": "2017-09-14T07:30:49",
                "definition_type": "assessment",
                "helptext": "",
                "placeholder": "",
                "id": 4654,
                "multi_choice_options": null,
                "default_value": null,
                "modified_by": {
                    "context_id": null,
                    "href": "/api/people/328",
                    "type": "Person",
                    "id": 328
                },
                "title": "GCA_person_GCA_person_GCA_person",
                "multi_choice_mandatory": null,
                "created_at": "2017-05-29T10:01:49",
                "definition_id": null,
                "context": null,
                "type": "CustomAttributeDefinition",
                "selfLink": "/api/custom_attribute_definitions/4654"
            },
            {
                "mandatory": false,
                "attribute_type": "Dropdown",
                "updated_at": "2017-07-07T12:55:46",
                "definition_type": "assessment",
                "helptext": "Assessment Category",
                "placeholder": "",
                "id": 12170,
                "multi_choice_options": "Documentation,Interview",
                "default_value": "",
                "modified_by": {
                    "context_id": null,
                    "href": "/api/people/311",
                    "type": "Person",
                    "id": 311
                },
                "title": "Type",
                "multi_choice_mandatory": null,
                "created_at": "2017-07-07T12:55:46",
                "definition_id": null,
                "context": null,
                "type": "CustomAttributeDefinition",
                "selfLink": "/api/custom_attribute_definitions/12170"
            },
            {
                "mandatory": false,
                "attribute_type": "Text",
                "updated_at": "2017-11-09T12:08:21",
                "definition_type": "assessment",
                "helptext": "АС\\ЫЦУМПА",
                "placeholder": "АС\\ЫЦУМПА",
                "id": 13360,
                "multi_choice_options": null,
                "default_value": "",
                "modified_by": {
                    "context_id": null,
                    "href": "/api/people/393",
                    "type": "Person",
                    "id": 393
                },
                "title": "АС\\ЫЦУМПА",
                "multi_choice_mandatory": null,
                "created_at": "2017-08-25T14:23:51",
                "definition_id": null,
                "context": null,
                "type": "CustomAttributeDefinition",
                "selfLink": "/api/custom_attribute_definitions/13360"
            },
            {
                "mandatory":
                false,
                "attribute_type":
                "Text",
                "updated_at":
                "2017-09-14T07:33:12",
                "definition_type":
                "assessment",
                "helptext":
                "",
                "placeholder":
                "",
                "id":
                13521,
                "multi_choice_options":
                null,
                "default_value":
                "",
                "modified_by": {
                    "context_id": null,
                    "href": "/api/people/328",
                    "type": "Person",
                    "id": 328
                },
                "title":
                "Dashboard_data_report_Dashboard_data_report_Dashboard_data_report_Dashboard_data_report_",
                "multi_choice_mandatory":
                null,
                "created_at":
                "2017-08-29T10:56:30",
                "definition_id":
                null,
                "context":
                null,
                "type":
                "CustomAttributeDefinition",
                "selfLink":
                "/api/custom_attribute_definitions/13521"
            },
            {
                "mandatory": false,
                "attribute_type": "Checkbox",
                "updated_at": "2017-11-24T15:17:14",
                "definition_type": "assessment",
                "helptext": "",
                "placeholder": "",
                "id": 13662,
                "multi_choice_options": null,
                "default_value": "0",
                "modified_by": {
                    "context_id": null,
                    "href": "/api/people/480",
                    "type": "Person",
                    "id": 480
                },
                "title": "new_checkbox",
                "multi_choice_mandatory": null,
                "created_at": "2017-09-14T09:33:19",
                "definition_id": null,
                "context": null,
                "type": "CustomAttributeDefinition",
                "selfLink": "/api/custom_attribute_definitions/13662"
            },
            {
                "mandatory":
                false,
                "attribute_type":
                "Text",
                "updated_at":
                "2017-10-31T12:40:13",
                "definition_type":
                "assessment",
                "helptext":
                "help",
                "placeholder":
                "",
                "id":
                14001,
                "multi_choice_options":
                null,
                "default_value":
                "",
                "modified_by": {
                    "context_id": null,
                    "href": "/api/people/456",
                    "type": "Person",
                    "id": 456
                },
                "title":
                " LOREM IPSUM IS SIMPLY DUMMY TEXT OF THE PRINTING AND TYPESETTING INDUSTRY. LOREM IPSUM HAS BEEN THE INDUSTRY'S STANDARD DUMMY TEXT EVER SINCE THE 1500S, WHEN AN UNKNOWN PRINTER TOOK A GALLEY OF TYPE AND SCRAMBLED IT TO MAKE A TYPE SPECIMEN BOOK.",
                "multi_choice_mandatory":
                null,
                "created_at":
                "2017-10-31T12:40:13",
                "definition_id":
                null,
                "context":
                null,
                "type":
                "CustomAttributeDefinition",
                "selfLink":
                "/api/custom_attribute_definitions/14001"
            },
            {
                "mandatory": false,
                "attribute_type": "Map:Person",
                "updated_at": "2018-05-03T13:53:29",
                "definition_type": "assessment",
                "helptext": "",
                "placeholder": "",
                "id": 14773,
                "multi_choice_options": null,
                "default_value": null,
                "modified_by": {
                    "context_id": null,
                    "href": "/api/people/328",
                    "type": "Person",
                    "id": 328
                },
                "title": "CA Person",
                "multi_choice_mandatory": null,
                "created_at": "2018-02-16T12:03:47",
                "definition_id": null,
                "context": null,
                "type": "CustomAttributeDefinition",
                "selfLink": "/api/custom_attribute_definitions/14773"
            }
        ],
        "custom_attribute_values": [
            {
                "attribute_object": null,
                "attribute_value": "",
                "custom_attribute_id": 4650,
                "attribute_object_id": null,
                "modified_by": null,
                "created_at": "2018-10-20T20:02:45",
                "attributable_type": "Assessment",
                "updated_at": "2018-10-20T20:02:45",
                "attributable_id": 24648,
                "context": null,
                "type": "CustomAttributeValue",
                "id": 104444,
                "selfLink": "/api/custom_attribute_values/104444",
                "preconditions_failed": null,
                "def": {
                    "mandatory":
                    false,
                    "attribute_type":
                    "Rich Text",
                    "updated_at":
                    "2017-11-14T10:02:18",
                    "definition_type":
                    "assessment",
                    "helptext":
                    "help",
                    "placeholder":
                    "",
                    "id":
                    4650,
                    "multi_choice_options":
                    null,
                    "default_value":
                    "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/393",
                        "type": "Person",
                        "id": 393
                    },
                    "title":
                    "GCA_rich_text1_GCA_rich_text1_GCA_rich_text1_GCA_rich_text1_GCA_rich_text1_GCA_rich_text1_",
                    "multi_choice_mandatory":
                    null,
                    "created_at":
                    "2017-05-29T09:59:49",
                    "definition_id":
                    null,
                    "context":
                    null,
                    "type":
                    "CustomAttributeDefinition",
                    "selfLink":
                    "/api/custom_attribute_definitions/4650"
                },
                "attributeType": "text",
                "validation": {
                    "empty": false,
                    "mandatory": false,
                    "valid": true
                },
                "errorsMap": {
                    "comment": false,
                    "evidence": false,
                    "url": false
                }
            },
            {
                "attribute_object": null,
                "attribute_value": "",
                "custom_attribute_id": 4651,
                "attribute_object_id": null,
                "modified_by": null,
                "created_at": "2018-10-20T20:02:45",
                "attributable_type": "Assessment",
                "updated_at": "2018-10-20T20:02:45",
                "attributable_id": 24648,
                "context": null,
                "type": "CustomAttributeValue",
                "id": 104445,
                "selfLink": "/api/custom_attribute_values/104445",
                "preconditions_failed": null,
                "def": {
                    "mandatory":
                    false,
                    "attribute_type":
                    "Date",
                    "updated_at":
                    "2017-11-10T13:47:49",
                    "definition_type":
                    "assessment",
                    "helptext":
                    "",
                    "placeholder":
                    "",
                    "id":
                    4651,
                    "multi_choice_options":
                    null,
                    "default_value":
                    "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/393",
                        "type": "Person",
                        "id": 393
                    },
                    "title":
                    "GCA_date_GCA_date_GCA_date_GCA_date_GCA_date_GCA_date_GCA_date_",
                    "multi_choice_mandatory":
                    null,
                    "created_at":
                    "2017-05-29T10:00:40",
                    "definition_id":
                    null,
                    "context":
                    null,
                    "type":
                    "CustomAttributeDefinition",
                    "selfLink":
                    "/api/custom_attribute_definitions/4651"
                },
                "attributeType": "date",
                "validation": {
                    "empty": false,
                    "mandatory": false,
                    "valid": true
                },
                "errorsMap": {
                    "comment": false,
                    "evidence": false,
                    "url": false
                }
            },
            {
                "attribute_object": null,
                "attribute_value": "",
                "custom_attribute_id": 4653,
                "attribute_object_id": null,
                "modified_by": null,
                "created_at": "2018-10-20T20:02:45",
                "attributable_type": "Assessment",
                "updated_at": "2018-10-20T20:02:45",
                "attributable_id": 24648,
                "context": null,
                "type": "CustomAttributeValue",
                "id": 104446,
                "selfLink": "/api/custom_attribute_values/104446",
                "preconditions_failed": null,
                "def": {
                    "mandatory":
                    false,
                    "attribute_type":
                    "Dropdown",
                    "updated_at":
                    "2017-09-14T07:32:11",
                    "definition_type":
                    "assessment",
                    "helptext":
                    "",
                    "placeholder":
                    "",
                    "id":
                    4653,
                    "multi_choice_options":
                    "yes,no,other",
                    "default_value":
                    "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title":
                    "GCA_dropdown_GCA_dropdown_GCA_dropdown_GCA_dropdown",
                    "multi_choice_mandatory":
                    null,
                    "created_at":
                    "2017-05-29T10:01:32",
                    "definition_id":
                    null,
                    "context":
                    null,
                    "type":
                    "CustomAttributeDefinition",
                    "selfLink":
                    "/api/custom_attribute_definitions/4653"
                },
                "attributeType": "dropdown",
                "validation": {
                    "empty": false,
                    "mandatory": false,
                    "valid": true
                },
                "errorsMap": {
                    "comment": false,
                    "evidence": false,
                    "url": false
                },
                "validationConfig": {}
            },
            {
                "attribute_object": null,
                "attribute_value": "Person",
                "custom_attribute_id": 4654,
                "attribute_object_id": null,
                "modified_by": null,
                "created_at": "2018-10-20T20:02:45",
                "attributable_type": "Assessment",
                "updated_at": "2018-10-20T20:02:45",
                "attributable_id": 24648,
                "context": null,
                "type": "CustomAttributeValue",
                "id": 104447,
                "selfLink": "/api/custom_attribute_values/104447",
                "preconditions_failed": null,
                "def": {
                    "mandatory": false,
                    "attribute_type": "Map:Person",
                    "updated_at": "2017-09-14T07:30:49",
                    "definition_type": "assessment",
                    "helptext": "",
                    "placeholder": "",
                    "id": 4654,
                    "multi_choice_options": null,
                    "default_value": null,
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title": "GCA_person_GCA_person_GCA_person",
                    "multi_choice_mandatory": null,
                    "created_at": "2017-05-29T10:01:49",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/4654"
                },
                "attributeType": "person",
                "validation": {
                    "empty": false,
                    "mandatory": false,
                    "valid": true
                },
                "errorsMap": {
                    "comment": false,
                    "evidence": false,
                    "url": false
                }
            },
            {
                "attribute_object": null,
                "attribute_value": "",
                "custom_attribute_id": 12170,
                "attribute_object_id": null,
                "modified_by": null,
                "created_at": "2018-10-20T20:02:45",
                "attributable_type": "Assessment",
                "updated_at": "2018-10-20T20:02:45",
                "attributable_id": 24648,
                "context": null,
                "type": "CustomAttributeValue",
                "id": 104448,
                "selfLink": "/api/custom_attribute_values/104448",
                "preconditions_failed": null,
                "def": {
                    "mandatory": false,
                    "attribute_type": "Dropdown",
                    "updated_at": "2017-07-07T12:55:46",
                    "definition_type": "assessment",
                    "helptext": "Assessment Category",
                    "placeholder": "",
                    "id": 12170,
                    "multi_choice_options": "Documentation,Interview",
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/311",
                        "type": "Person",
                        "id": 311
                    },
                    "title": "Type",
                    "multi_choice_mandatory": null,
                    "created_at": "2017-07-07T12:55:46",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/12170"
                },
                "attributeType": "dropdown",
                "validation": {
                    "empty": false,
                    "mandatory": false,
                    "valid": true
                },
                "errorsMap": {
                    "comment": false,
                    "evidence": false,
                    "url": false
                },
                "validationConfig": {}
            },
            {
                "attribute_object": null,
                "attribute_value": "",
                "custom_attribute_id": 13360,
                "attribute_object_id": null,
                "modified_by": null,
                "created_at": "2018-10-20T20:02:45",
                "attributable_type": "Assessment",
                "updated_at": "2018-10-20T20:02:45",
                "attributable_id": 24648,
                "context": null,
                "type": "CustomAttributeValue",
                "id": 104449,
                "selfLink": "/api/custom_attribute_values/104449",
                "preconditions_failed": null,
                "def": {
                    "mandatory": false,
                    "attribute_type": "Text",
                    "updated_at": "2017-11-09T12:08:21",
                    "definition_type": "assessment",
                    "helptext": "АС\\ЫЦУМПА",
                    "placeholder": "АС\\ЫЦУМПА",
                    "id": 13360,
                    "multi_choice_options": null,
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/393",
                        "type": "Person",
                        "id": 393
                    },
                    "title": "АС\\ЫЦУМПА",
                    "multi_choice_mandatory": null,
                    "created_at": "2017-08-25T14:23:51",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/13360"
                },
                "attributeType": "input",
                "validation": {
                    "empty": false,
                    "mandatory": false,
                    "valid": true
                },
                "errorsMap": {
                    "comment": false,
                    "evidence": false,
                    "url": false
                }
            },
            {
                "attribute_object": null,
                "attribute_value": "",
                "custom_attribute_id": 13521,
                "attribute_object_id": null,
                "modified_by": null,
                "created_at": "2018-10-20T20:02:45",
                "attributable_type": "Assessment",
                "updated_at": "2018-10-20T20:02:45",
                "attributable_id": 24648,
                "context": null,
                "type": "CustomAttributeValue",
                "id": 104450,
                "selfLink": "/api/custom_attribute_values/104450",
                "preconditions_failed": null,
                "def": {
                    "mandatory":
                    false,
                    "attribute_type":
                    "Text",
                    "updated_at":
                    "2017-09-14T07:33:12",
                    "definition_type":
                    "assessment",
                    "helptext":
                    "",
                    "placeholder":
                    "",
                    "id":
                    13521,
                    "multi_choice_options":
                    null,
                    "default_value":
                    "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title":
                    "Dashboard_data_report_Dashboard_data_report_Dashboard_data_report_Dashboard_data_report_",
                    "multi_choice_mandatory":
                    null,
                    "created_at":
                    "2017-08-29T10:56:30",
                    "definition_id":
                    null,
                    "context":
                    null,
                    "type":
                    "CustomAttributeDefinition",
                    "selfLink":
                    "/api/custom_attribute_definitions/13521"
                },
                "attributeType": "input",
                "validation": {
                    "empty": false,
                    "mandatory": false,
                    "valid": true
                },
                "errorsMap": {
                    "comment": false,
                    "evidence": false,
                    "url": false
                }
            },
            {
                "attribute_object": null,
                "attribute_value": "0",
                "custom_attribute_id": 13662,
                "attribute_object_id": null,
                "modified_by": null,
                "created_at": "2018-10-20T20:02:45",
                "attributable_type": "Assessment",
                "updated_at": "2018-10-20T20:02:45",
                "attributable_id": 24648,
                "context": null,
                "type": "CustomAttributeValue",
                "id": 104451,
                "selfLink": "/api/custom_attribute_values/104451",
                "preconditions_failed": null,
                "def": {
                    "mandatory": false,
                    "attribute_type": "Checkbox",
                    "updated_at": "2017-11-24T15:17:14",
                    "definition_type": "assessment",
                    "helptext": "",
                    "placeholder": "",
                    "id": 13662,
                    "multi_choice_options": null,
                    "default_value": "0",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/480",
                        "type": "Person",
                        "id": 480
                    },
                    "title": "new_checkbox",
                    "multi_choice_mandatory": null,
                    "created_at": "2017-09-14T09:33:19",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/13662"
                },
                "attributeType": "checkbox",
                "validation": {
                    "empty": false,
                    "mandatory": false,
                    "valid": true
                },
                "errorsMap": {
                    "comment": false,
                    "evidence": false,
                    "url": false
                }
            },
            {
                "attribute_object": null,
                "attribute_value": "",
                "custom_attribute_id": 14001,
                "attribute_object_id": null,
                "modified_by": null,
                "created_at": "2018-10-20T20:02:45",
                "attributable_type": "Assessment",
                "updated_at": "2018-10-20T20:02:45",
                "attributable_id": 24648,
                "context": null,
                "type": "CustomAttributeValue",
                "id": 104452,
                "selfLink": "/api/custom_attribute_values/104452",
                "preconditions_failed": null,
                "def": {
                    "mandatory":
                    false,
                    "attribute_type":
                    "Text",
                    "updated_at":
                    "2017-10-31T12:40:13",
                    "definition_type":
                    "assessment",
                    "helptext":
                    "help",
                    "placeholder":
                    "",
                    "id":
                    14001,
                    "multi_choice_options":
                    null,
                    "default_value":
                    "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/456",
                        "type": "Person",
                        "id": 456
                    },
                    "title":
                    " LOREM IPSUM IS SIMPLY DUMMY TEXT OF THE PRINTING AND TYPESETTING INDUSTRY. LOREM IPSUM HAS BEEN THE INDUSTRY'S STANDARD DUMMY TEXT EVER SINCE THE 1500S, WHEN AN UNKNOWN PRINTER TOOK A GALLEY OF TYPE AND SCRAMBLED IT TO MAKE A TYPE SPECIMEN BOOK.",
                    "multi_choice_mandatory":
                    null,
                    "created_at":
                    "2017-10-31T12:40:13",
                    "definition_id":
                    null,
                    "context":
                    null,
                    "type":
                    "CustomAttributeDefinition",
                    "selfLink":
                    "/api/custom_attribute_definitions/14001"
                },
                "attributeType": "input",
                "validation": {
                    "empty": false,
                    "mandatory": false,
                    "valid": true
                },
                "errorsMap": {
                    "comment": false,
                    "evidence": false,
                    "url": false
                }
            },
            {
                "attribute_object": null,
                "attribute_value": "Person",
                "custom_attribute_id": 14773,
                "attribute_object_id": null,
                "modified_by": null,
                "created_at": "2018-10-20T20:02:45",
                "attributable_type": "Assessment",
                "updated_at": "2018-10-20T20:02:45",
                "attributable_id": 24648,
                "context": null,
                "type": "CustomAttributeValue",
                "id": 104453,
                "selfLink": "/api/custom_attribute_values/104453",
                "preconditions_failed": null,
                "def": {
                    "mandatory": false,
                    "attribute_type": "Map:Person",
                    "updated_at": "2018-05-03T13:53:29",
                    "definition_type": "assessment",
                    "helptext": "",
                    "placeholder": "",
                    "id": 14773,
                    "multi_choice_options": null,
                    "default_value": null,
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title": "CA Person",
                    "multi_choice_mandatory": null,
                    "created_at": "2018-02-16T12:03:47",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/14773"
                },
                "attributeType": "person",
                "validation": {
                    "empty": false,
                    "mandatory": false,
                    "valid": true
                },
                "errorsMap": {
                    "comment": false,
                    "evidence": false,
                    "url": false
                }
            }
        ],
        "access_control_list": [
            {
                "person_name": "roman@reciprocitylabs.com",
                "parent_id_nn": 0,
                "display_name": "",
                "ac_role_id": 120,
                "context_id": null,
                "created_at": "2018-10-20T20:02:45",
                "object_type": "Assessment",
                "updated_at": "2018-10-20T20:02:45",
                "object_id": 24648,
                "parent_id": null,
                "person_email": "roman@reciprocitylabs.com",
                "person": {
                    "context_id": null,
                    "href": "/api/people/5",
                    "type": "Person",
                    "id": 5
                },
                "base_id": 113157943,
                "modified_by_id": null,
                "person_id": 5,
                "modified_by": null,
                "type": "AccessControlList",
                "id": 113157943
            },
            {
                "person_name": "zidarsk8",
                "parent_id_nn": 0,
                "display_name": "",
                "ac_role_id": 124,
                "context_id": null,
                "created_at": "2018-10-20T20:02:45",
                "object_type": "Assessment",
                "updated_at": "2018-10-20T20:02:45",
                "object_id": 24648,
                "parent_id": null,
                "person_email": "zidarsk8@gmail.com",
                "person": {
                    "context_id": null,
                    "href": "/api/people/354",
                    "type": "Person",
                    "id": 354
                },
                "base_id": 113157949,
                "modified_by_id": null,
                "person_id": 354,
                "modified_by": null,
                "type": "AccessControlList",
                "id": 113157949
            }
        ],
        "audit": {
            "id": 49,
            "type": "Audit",
            "href": "/api/audits/49"
        },
        "context": {
            "id": 1145,
            "type": "Context",
            "href": "/api/contexts/1145",
            "context_id": null
        },
        "design":
        "",
        "operationally":
        "",
        "mappedObjectsChanges": [],
        "title":
        "a",
        "notes":
        "",
        "slug":
        "ASSESSMENT-24648",
        "provisional_id":
        "provisional_1540065767226",
        "verified_date":
        null,
        "people": [],
        "labels": [],
        "last_comment_id":
        null,
        "last_comment":
        null,
        "task_group_objects": [],
        "id":
        24648,
        "finished_date":
        null,
        "archived":
        false,
        "verified":
        false,
        "end_date":
        null,
        "test_plan":
        "",
        "object_people": [],
        "folder":
        "",
        "type":
        "Assessment",
        "start_date":
        null,
        "viewLink":
        "/assessments/24648",
        "description":
        "",
        "workflow_state":
        null,
        "object": {},
        "updated_at":
        "2018-10-20T20:02:45.000Z",
        "modified_by": {
            "context_id": null,
            "href": "/api/people/354",
            "type": "Person",
            "id": 354
        },
        "issue_tracker": {
            "hotlist_id": null,
            "issue_priority": null,
            "component_id": null,
            "issue_type": null,
            "title": null,
            "issue_id": null,
            "enabled": false,
            "_warnings": [],
            "issue_url": null,
            "issue_severity": null
        },
        "preconditions_failed":
        false,
        "task_groups": [],
        "created_at":
        "2018-10-20T20:02:44.000Z",
        "selfLink":
        "/api/assessments/24648",
        "selectedTabIndex":
        1,
        "actions": {
            "add_related": [{
                "id": 2695,
                "type": "Comment"
            }]
        }
    }
}

program_audit_tree_view_query = [
    {
        "object_name": "Audit",
        "filters": {
            "expression": {
                "object_name": "Program",
                "op": {
                    "name": "relevant"
                },
                "ids": [None]
            }
        },
        "limit": [0, 10],
        "order_by": [{
            "name": "updated_at",
            "desc": true
        }]
    }
]

audit_assessment_tree_view_query = [
    {
        "object_name": "Assessment",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "relevant"
                },
                "ids": [None]
            }
        },
        "limit": [0, 10],
        "order_by": [{
            "name": "updated_at",
            "desc": true
        }]
    }
]

assessment_payload = [
    {
        "assessment": {
            "test_plan_procedure":
            true,
            "assessment_type":
            "Control",
            "status":
            "Not Started",
            "send_by_default":
            true,
            "recipients":
            "Assignees,Creators,Verifiers",
            "custom_attribute_definitions": [
                {
                    "mandatory":
                    false,
                    "attribute_type":
                    "Rich Text",
                    "updated_at":
                    "2017-11-14T10:02:18",
                    "definition_type":
                    "assessment",
                    "helptext":
                    "help",
                    "placeholder":
                    "",
                    "id":
                    4650,
                    "multi_choice_options":
                    None,
                    "default_value":
                    "",
                    "modified_by": {
                        "context_id": None,
                        "href": "/api/people/393",
                        "type": "Person",
                        "id": 393
                    },
                    "title":
                    "GCA_rich_text1_GCA_rich_text1_GCA_rich_text1_GCA_rich_text1_GCA_rich_text1_GCA_rich_text1_",
                    "multi_choice_mandatory":
                    None,
                    "created_at":
                    "2017-05-29T09:59:49",
                    "definition_id":
                    None,
                    "context":
                    None,
                    "type":
                    "CustomAttributeDefinition",
                    "selfLink":
                    "/api/custom_attribute_definitions/4650"
                },
                {
                    "mandatory":
                    false,
                    "attribute_type":
                    "Date",
                    "updated_at":
                    "2017-11-10T13:47:49",
                    "definition_type":
                    "assessment",
                    "helptext":
                    "",
                    "placeholder":
                    "",
                    "id":
                    4651,
                    "multi_choice_options":
                    None,
                    "default_value":
                    "",
                    "modified_by": {
                        "context_id": None,
                        "href": "/api/people/393",
                        "type": "Person",
                        "id": 393
                    },
                    "title":
                    "GCA_date_GCA_date_GCA_date_GCA_date_GCA_date_GCA_date_GCA_date_",
                    "multi_choice_mandatory":
                    None,
                    "created_at":
                    "2017-05-29T10:00:40",
                    "definition_id":
                    None,
                    "context":
                    None,
                    "type":
                    "CustomAttributeDefinition",
                    "selfLink":
                    "/api/custom_attribute_definitions/4651"
                },
                {
                    "mandatory":
                    false,
                    "attribute_type":
                    "Dropdown",
                    "updated_at":
                    "2017-09-14T07:32:11",
                    "definition_type":
                    "assessment",
                    "helptext":
                    "",
                    "placeholder":
                    "",
                    "id":
                    4653,
                    "multi_choice_options":
                    "yes,no,other",
                    "default_value":
                    "",
                    "modified_by": {
                        "context_id": None,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title":
                    "GCA_dropdown_GCA_dropdown_GCA_dropdown_GCA_dropdown",
                    "multi_choice_mandatory":
                    None,
                    "created_at":
                    "2017-05-29T10:01:32",
                    "definition_id":
                    None,
                    "context":
                    None,
                    "type":
                    "CustomAttributeDefinition",
                    "selfLink":
                    "/api/custom_attribute_definitions/4653"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Map:Person",
                    "updated_at": "2017-09-14T07:30:49",
                    "definition_type": "assessment",
                    "helptext": "",
                    "placeholder": "",
                    "id": 4654,
                    "multi_choice_options": None,
                    "default_value": None,
                    "modified_by": {
                        "context_id": None,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title": "GCA_person_GCA_person_GCA_person",
                    "multi_choice_mandatory": None,
                    "created_at": "2017-05-29T10:01:49",
                    "definition_id": None,
                    "context": None,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/4654"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Dropdown",
                    "updated_at": "2017-07-07T12:55:46",
                    "definition_type": "assessment",
                    "helptext": "Assessment Category",
                    "placeholder": "",
                    "id": 12170,
                    "multi_choice_options": "Documentation,Interview",
                    "default_value": "",
                    "modified_by": {
                        "context_id": None,
                        "href": "/api/people/311",
                        "type": "Person",
                        "id": 311
                    },
                    "title": "Type",
                    "multi_choice_mandatory": None,
                    "created_at": "2017-07-07T12:55:46",
                    "definition_id": None,
                    "context": None,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/12170"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Text",
                    "updated_at": "2017-11-09T12:08:21",
                    "definition_type": "assessment",
                    "helptext": "АС\\ЫЦУМПА",
                    "placeholder": "АС\\ЫЦУМПА",
                    "id": 13360,
                    "multi_choice_options": None,
                    "default_value": "",
                    "modified_by": {
                        "context_id": None,
                        "href": "/api/people/393",
                        "type": "Person",
                        "id": 393
                    },
                    "title": "АС\\ЫЦУМПА",
                    "multi_choice_mandatory": None,
                    "created_at": "2017-08-25T14:23:51",
                    "definition_id": None,
                    "context": None,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/13360"
                },
                {
                    "mandatory":
                    false,
                    "attribute_type":
                    "Text",
                    "updated_at":
                    "2017-09-14T07:33:12",
                    "definition_type":
                    "assessment",
                    "helptext":
                    "",
                    "placeholder":
                    "",
                    "id":
                    13521,
                    "multi_choice_options":
                    None,
                    "default_value":
                    "",
                    "modified_by": {
                        "context_id": None,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title":
                    "Dashboard_data_report_Dashboard_data_report_Dashboard_data_report_Dashboard_data_report_",
                    "multi_choice_mandatory":
                    None,
                    "created_at":
                    "2017-08-29T10:56:30",
                    "definition_id":
                    None,
                    "context":
                    None,
                    "type":
                    "CustomAttributeDefinition",
                    "selfLink":
                    "/api/custom_attribute_definitions/13521"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Checkbox",
                    "updated_at": "2017-11-24T15:17:14",
                    "definition_type": "assessment",
                    "helptext": "",
                    "placeholder": "",
                    "id": 13662,
                    "multi_choice_options": None,
                    "default_value": "0",
                    "modified_by": {
                        "context_id": None,
                        "href": "/api/people/480",
                        "type": "Person",
                        "id": 480
                    },
                    "title": "new_checkbox",
                    "multi_choice_mandatory": None,
                    "created_at": "2017-09-14T09:33:19",
                    "definition_id": None,
                    "context": None,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/13662"
                },
                {
                    "mandatory":
                    false,
                    "attribute_type":
                    "Text",
                    "updated_at":
                    "2017-10-31T12:40:13",
                    "definition_type":
                    "assessment",
                    "helptext":
                    "help",
                    "placeholder":
                    "",
                    "id":
                    14001,
                    "multi_choice_options":
                    None,
                    "default_value":
                    "",
                    "modified_by": {
                        "context_id": None,
                        "href": "/api/people/456",
                        "type": "Person",
                        "id": 456
                    },
                    "title":
                    " LOREM IPSUM IS SIMPLY DUMMY TEXT OF THE PRINTING AND TYPESETTING INDUSTRY. LOREM IPSUM HAS BEEN THE INDUSTRY'S STANDARD DUMMY TEXT EVER SINCE THE 1500S, WHEN AN UNKNOWN PRINTER TOOK A GALLEY OF TYPE AND SCRAMBLED IT TO MAKE A TYPE SPECIMEN BOOK.",
                    "multi_choice_mandatory":
                    None,
                    "created_at":
                    "2017-10-31T12:40:13",
                    "definition_id":
                    None,
                    "context":
                    None,
                    "type":
                    "CustomAttributeDefinition",
                    "selfLink":
                    "/api/custom_attribute_definitions/14001"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Map:Person",
                    "updated_at": "2018-05-03T13:53:29",
                    "definition_type": "assessment",
                    "helptext": "",
                    "placeholder": "",
                    "id": 14773,
                    "multi_choice_options": None,
                    "default_value": None,
                    "modified_by": {
                        "context_id": None,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title": "CA Person",
                    "multi_choice_mandatory": None,
                    "created_at": "2018-02-16T12:03:47",
                    "definition_id": None,
                    "context": None,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/14773"
                }
            ],
            "custom_attribute_values": [
                {
                    "attribute_object": None,
                    "attribute_value": "",
                    "custom_attribute_id": 4650,
                    "attribute_object_id": None
                },
                {
                    "attribute_object": None,
                    "attribute_value": "",
                    "custom_attribute_id": 4651,
                    "attribute_object_id": None
                },
                {
                    "attribute_object": None,
                    "attribute_value": "",
                    "custom_attribute_id": 4653,
                    "attribute_object_id": None
                },
                {
                    "attribute_object": None,
                    "attribute_value": "Person",
                    "custom_attribute_id": 4654,
                    "attribute_object_id": None
                },
                {
                    "attribute_object": None,
                    "attribute_value": "",
                    "custom_attribute_id": 12170,
                    "attribute_object_id": None
                },
                {
                    "attribute_object": None,
                    "attribute_value": "",
                    "custom_attribute_id": 13360,
                    "attribute_object_id": None
                },
                {
                    "attribute_object": None,
                    "attribute_value": "",
                    "custom_attribute_id": 13521,
                    "attribute_object_id": None
                },
                {
                    "attribute_object": None,
                    "attribute_value": "0",
                    "custom_attribute_id": 13662,
                    "attribute_object_id": None
                },
                {
                    "attribute_object": None,
                    "attribute_value": "",
                    "custom_attribute_id": 14001,
                    "attribute_object_id": None
                },
                {
                    "attribute_object": None,
                    "attribute_value": "Person",
                    "custom_attribute_id": 14773,
                    "attribute_object_id": None
                }
            ],
            "access_control_list": [
                {
                    "ac_role_id": 124,
                    "person": {
                        "id": 354
                    },
                    "person_id": 354
                }, {
                    "ac_role_id": 120,
                    "person": {
                        "id": 5
                    },
                    "person_id": 5
                }
            ],
            "audit": {
                "id": None,
                "type": "Audit",
            },
            "context": {
                "id": 1145,
                "type": "Context",
                "href": "/api/contexts/1145"
            },
            "design":
            "",
            "operationally":
            "",
            "mappedObjectsChanges": [],
            "title":
            "a",
            "notes":
            "",
            "slug":
            ""
        }
    }
]

audit_payload = [
    {
        "audit": {
            "status": "Planned",
            "custom_attribute_definitions": [
                {
                    "mandatory": false,
                    "attribute_type": "Rich Text",
                    "updated_at": "2016-09-26T12:10:27",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 1506,
                    "multi_choice_options": null,
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/246",
                        "type": "Person",
                        "id": 246
                    },
                    "title": "rich text-1",
                    "multi_choice_mandatory": null,
                    "created_at": "2016-09-26T12:10:27",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/1506"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Date",
                    "updated_at": "2016-09-26T12:13:37",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 1536,
                    "multi_choice_options": null,
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/246",
                        "type": "Person",
                        "id": 246
                    },
                    "title": "date-1",
                    "multi_choice_mandatory": null,
                    "created_at": "2016-09-26T12:13:37",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/1536"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Checkbox",
                    "updated_at": "2016-09-26T12:16:39",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 1564,
                    "multi_choice_options": null,
                    "default_value": "0",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/246",
                        "type": "Person",
                        "id": 246
                    },
                    "title": "checkbox-1",
                    "multi_choice_mandatory": null,
                    "created_at": "2016-09-26T12:16:39",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/1564"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Map:Person",
                    "updated_at": "2017-08-15T10:35:12",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 1593,
                    "multi_choice_options": null,
                    "default_value": null,
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/425",
                        "type": "Person",
                        "id": 425
                    },
                    "title": "person-1",
                    "multi_choice_mandatory": null,
                    "created_at": "2016-09-26T12:19:59",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/1593"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Dropdown",
                    "updated_at": "2016-09-26T12:25:01",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 1621,
                    "multi_choice_options": "4,5,6",
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/246",
                        "type": "Person",
                        "id": 246
                    },
                    "title": "dropdown-1",
                    "multi_choice_mandatory": null,
                    "created_at": "2016-09-26T12:25:01",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/1621"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Text",
                    "updated_at": "2017-07-11T09:35:21",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 3229,
                    "multi_choice_options": null,
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/425",
                        "type": "Person",
                        "id": 425
                    },
                    "title": "text-1",
                    "multi_choice_mandatory": null,
                    "created_at": "2017-04-11T09:09:33",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/3229"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Text",
                    "updated_at": "2017-08-23T13:07:27",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 13252,
                    "multi_choice_options": null,
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title": "Dashboard_Data_report1",
                    "multi_choice_mandatory": null,
                    "created_at": "2017-08-23T13:07:27",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/13252"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Text",
                    "updated_at": "2017-08-29T10:54:02",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 13517,
                    "multi_choice_options": null,
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title": "Dashboard_Data_report2",
                    "multi_choice_mandatory": null,
                    "created_at": "2017-08-29T10:54:02",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/13517"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Text",
                    "updated_at": "2017-08-29T10:54:10",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 13518,
                    "multi_choice_options": null,
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title": "Dashboard_Data_report3",
                    "multi_choice_mandatory": null,
                    "created_at": "2017-08-29T10:54:10",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/13518"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Text",
                    "updated_at": "2017-08-29T10:54:20",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 13519,
                    "multi_choice_options": null,
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title": "Dashboard_Data_report4",
                    "multi_choice_mandatory": null,
                    "created_at": "2017-08-29T10:54:20",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/13519"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Rich Text",
                    "updated_at": "2017-09-19T15:11:48",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 13695,
                    "multi_choice_options": null,
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/425",
                        "type": "Person",
                        "id": 425
                    },
                    "title": "Dashboard_Rich_Data_report1",
                    "multi_choice_mandatory": null,
                    "created_at": "2017-09-19T15:11:48",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/13695"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Text",
                    "updated_at": "2017-10-30T11:34:30",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 13997,
                    "multi_choice_options": null,
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title": "Dashboard_rep1",
                    "multi_choice_mandatory": null,
                    "created_at": "2017-10-30T11:34:30",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/13997"
                },
                {
                    "mandatory": false,
                    "attribute_type": "Text",
                    "updated_at": "2017-10-30T12:12:56",
                    "definition_type": "audit",
                    "helptext": "",
                    "placeholder": "",
                    "id": 13999,
                    "multi_choice_options": null,
                    "default_value": "",
                    "modified_by": {
                        "context_id": null,
                        "href": "/api/people/328",
                        "type": "Person",
                        "id": 328
                    },
                    "title": "Dashboard_data_report_check",
                    "multi_choice_mandatory": null,
                    "created_at": "2017-10-30T12:12:56",
                    "definition_id": null,
                    "context": null,
                    "type": "CustomAttributeDefinition",
                    "selfLink": "/api/custom_attribute_definitions/13999"
                }
            ],
            "custom_attribute_values": [
                {
                    "attribute_object": null,
                    "attribute_value": "",
                    "custom_attribute_id": 1506,
                    "attribute_object_id": null
                },
                {
                    "attribute_object": null,
                    "attribute_value": "",
                    "custom_attribute_id": 1536,
                    "attribute_object_id": null
                },
                {
                    "attribute_object": null,
                    "attribute_value": "0",
                    "custom_attribute_id": 1564,
                    "attribute_object_id": null
                },
                {
                    "attribute_object": null,
                    "attribute_value": "Person",
                    "custom_attribute_id": 1593,
                    "attribute_object_id": null
                },
                {
                    "attribute_object": null,
                    "attribute_value": "",
                    "custom_attribute_id": 1621,
                    "attribute_object_id": null
                },
                {
                    "attribute_object": null,
                    "attribute_value": "",
                    "custom_attribute_id": 3229,
                    "attribute_object_id": null
                },
                {
                    "attribute_object": null,
                    "attribute_value": "",
                    "custom_attribute_id": 13252,
                    "attribute_object_id": null
                },
                {
                    "attribute_object": null,
                    "attribute_value": "",
                    "custom_attribute_id": 13517,
                    "attribute_object_id": null
                },
                {
                    "attribute_object": null,
                    "attribute_value": "",
                    "custom_attribute_id": 13518,
                    "attribute_object_id": null
                },
                {
                    "attribute_object": null,
                    "attribute_value": "",
                    "custom_attribute_id": 13519,
                    "attribute_object_id": null
                },
                {
                    "attribute_object": null,
                    "attribute_value": "",
                    "custom_attribute_id": 13695,
                    "attribute_object_id": null
                },
                {
                    "attribute_object": null,
                    "attribute_value": "",
                    "custom_attribute_id": 13997,
                    "attribute_object_id": null
                },
                {
                    "attribute_object": null,
                    "attribute_value": "",
                    "custom_attribute_id": 13999,
                    "attribute_object_id": null
                }
            ],
            "access_control_list": [{
                "ac_role_id": 129,
                "person": {
                    "type": "Person",
                    "id": 11
                }
            }],
            "title": "2018: 123 - Audit 1",
            "program": {
                "id": 71,
                "type": "Program"
            },
            "context": {
                "id": 807,
                "type": "Context",
                "href": "/api/contexts/807"
            },
            "audit_firm": null,
            "slug": "",
            "modified_by_id": "11",
        }
    }
]

people_ids = [
    2,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    26,
    29,
    30,
    31,
    32,
    33,
    34,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    88,
    89,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
    100,
    101,
    102,
    103,
    104,
    105,
    106,
    107,
    108,
    109,
    110,
    111,
    112,
    113,
    114,
    115,
    116,
    117,
    118,
    119,
    122,
    123,
    124,
    125,
    126,
    127,
    128,
    129,
    130,
    131,
    132,
    133,
    134,
    135,
    136,
    137,
    138,
    139,
    140,
    141,
    142,
    143,
    144,
    145,
    146,
    147,
    148,
    149,
    150,
    151,
    152,
    153,
    154,
    155,
    156,
    157,
    158,
    159,
    160,
    161,
    162,
    163,
    164,
    165,
    166,
    167,
    168,
    169,
    170,
    171,
    172,
    173,
    174,
    175,
    176,
    177,
    178,
    179,
    180,
    181,
    182,
    183,
    184,
    185,
    186,
    187,
    188,
    189,
    190,
    192,
    193,
    194,
    196,
    197,
    199,
    200,
    201,
    202,
    203,
    204,
    205,
    206,
    207,
    208,
    209,
    210,
    211,
    212,
    213,
    214,
    215,
    216,
    217,
    218,
    219,
    220,
    221,
    222,
    223,
    224,
    225,
    226,
    227,
    228,
    229,
    230,
    232,
    234,
    235,
    236,
    237,
    238,
    239,
    240,
    241,
    242,
    246,
    247,
    248,
    249,
    250,
    251,
    252,
    253,
    255,
    256,
    257,
    258,
    259,
    260,
    261,
    262,
    263,
    264,
    265,
    266,
    267,
    268,
    269,
    270,
    271,
    272,
    273,
    275,
    276,
    277,
    278,
    279,
    280,
    281,
    282,
    283,
    284,
    288,
    289,
    290,
    291,
    292,
    293,
    294,
    295,
    296,
    297,
    298,
    299,
    300,
    301,
    302,
    303,
    304,
    305,
    306,
    307,
    308,
    309,
    310,
    311,
    312,
    313,
    314,
    315,
    316,
    317,
    318,
    319,
    320,
    321,
    322,
    323,
    324,
    325,
    326,
    327,
    328,
    329,
    330,
    331,
    332,
    333,
    334,
    335,
    336,
    337,
    338,
    339,
    340,
    341,
    343,
    344,
    345,
    346,
    347,
    349,
    350,
    351,
    353,
    354,
    355,
    356,
    357,
    361,
    362,
    363,
    364,
    365,
    366,
    367,
    368,
    369,
    370,
    371,
    372,
    375,
    377,
    379,
    380,
    381,
    382,
    383,
    384,
    385,
    386,
    388,
    390,
    391,
    392,
    393,
    394,
    398,
    399,
    400,
    401,
    402,
    403,
    404,
    405,
    406,
    407,
    408,
    409,
    410,
    411,
    412,
    413,
    414,
    415,
    416,
    417,
    418,
    419,
    420,
    421,
    422,
    423,
    424,
    425,
    426,
    427,
    428,
    429,
    430,
    431,
    432,
    433,
    434,
    435,
    436,
    437,
    438,
    439,
    440,
    441,
    442,
    443,
    444,
    446,
    447,
    448,
    449,
    450,
    451,
    452,
    453,
    454,
    455,
    456,
    457,
    458,
    459,
    460,
    461,
    462,
    463,
    464,
    465,
    466,
    467,
    468,
    469,
    470,
    471,
    472,
    473,
    474,
    475,
    476,
    477,
    478,
    479,
    480,
    481,
    482,
    483,
    484,
    485,
    486,
    490,
    491,
    492,
    493,
    494,
    495,
    496,
    497,
    500,
    501,
    502,
    503,
    504,
    505,
    506,
    509,
    510,
    511,
    512,
    513,
    514,
    515,
    516,
    517,
    518,
    519,
    520,
    521,
    522,
    523,
    524,
    525,
    526,
    527,
]

audit_49_count = [
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "AccessGroup"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Assessment",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "relevant"
                },
                "ids": ["49"]
            }
        },
        "type": "count"
    },
    {
        "object_name": "AssessmentTemplate",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "relevant"
                },
                "ids": ["49"]
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Contract"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Control"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "DataAsset"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Evidence",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "related_evidence"
                },
                "ids": ["49"]
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Facility"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Issue",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "relevant"
                },
                "ids": ["49"]
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Market"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Metric"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Objective"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "OrgGroup"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Person",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "related_people"
                },
                "ids": ["49"]
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Policy"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Process"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Product"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "ProductGroup"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Program",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "relevant"
                },
                "ids": ["49"]
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Regulation"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Requirement"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Risk"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Standard"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "System"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "TechnologyEnvironment"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Threat"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["49"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Vendor"
                }
            }
        },
        "type": "count"
    }
]  # noqa
audit_4567_count = [
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "AccessGroup"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Assessment",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "relevant"
                },
                "ids": ["4567"]
            }
        },
        "type": "count"
    },
    {
        "object_name": "AssessmentTemplate",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "relevant"
                },
                "ids": ["4567"]
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Contract"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Control"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "DataAsset"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Evidence",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "related_evidence"
                },
                "ids": ["4567"]
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Facility"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Issue",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "relevant"
                },
                "ids": ["4567"]
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Market"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Metric"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Objective"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "OrgGroup"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Person",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "related_people"
                },
                "ids": ["4567"]
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Policy"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Process"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Product"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "ProductGroup"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Program",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {
                    "name": "relevant"
                },
                "ids": ["4567"]
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Regulation"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Requirement"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Risk"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Standard"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "System"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "TechnologyEnvironment"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Threat"
                }
            }
        },
        "type": "count"
    },
    {
        "object_name": "Snapshot",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Audit",
                    "op": {
                        "name": "relevant"
                    },
                    "ids": ["4567"]
                },
                "op": {
                    "name": "AND"
                },
                "right": {
                    "left": "child_type",
                    "op": {
                        "name": "="
                    },
                    "right": "Vendor"
                }
            }
        },
        "type": "count"
    }
]  # noqa
