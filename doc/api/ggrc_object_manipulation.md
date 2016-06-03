- [Creating objects](#creating-objects)
    - [Audit](#audit)
    - [Assessment](#assessment)
    - [Object owners](#object-owners)
    - [Program](#program)
    - [Workflow](#workflow)
    - [Task group](#task-group)
    - [User role](#user-role)
- [Creating relationships between objects](#creating-relationships-between-objects)
    - [Relationship](#relationship)


# Creating objects
## Audit
### Overview
|||
|---|---|
|URL|/api/audits|
|Methods supported|`POST`, `DELETE`|
|Description|Creates an audit object. Note that if we want to add auditors, additional requests to [user roles](#user-role) have to be made.|

### Elements
|Field name|Type|Description|
|---|---|---|
|**Required**|||
|title|str|Audit title|
|status|[Audit status](/src/doc/api/types.md#audit-status)|Status of the audit object. Note that when creating a new audit the value has to be Audit_status.PLANNED|
|program|[GGRC object](/src/doc/api/types.md#ggrc-object)| Program reference|
|context|[GGRC object](/src/doc/api/types.md#ggrc-object)|Context reference from included Program|
|**Optional**|||
|description|str|Description of the audit object|
|slug|None or str|Unique identifier for this audit (can be defined here or if empty will be created on the server and sent in the response)|
|start_date|str|ISO-8601 formatted planned start date|
|end_date|str|ISO-8601 formatted planned end date|
|report_start_date|str|ISO-8601 formatted planned report start date|
|report_end_date|str|ISO-8601 formatted planned report start date|
|contact|[GGRC object](/src/doc/api/types.md#ggrc-object)| Internal audit lead|
|audit_firm|[GGRC object](/src/doc/api/types.md#ggrc-object)|OrgGroup reference|
|custom_attribute_definitions|list||
|custom_attributes|||
|modified_by_id|str||

### Examples
* create an audit object

    Request:
    ```
    {
        "audit": {
            "status": "Planned",
            "custom_attribute_definitions": [],
            "custom_attributes": {},
            "contact": {
                "id": 1,
                "href": "/api/people/1",
                "type": "Person"
            },
            "title": "2016: Test Program - Audit 2",
            "program": {
                "id": 2,
                "href": "/api/programs/2",
                "type": "Program"
            },
            "description": "",
            "audit_firm": {
                "id": 1,
                "href": "/api/org_groups/1",
                "type": "OrgGroup"
            },
            "slug": "example code",
            "modified_by_id": "1",
            "start_date": "2016-05-02",
            "end_date": "2016-05-09",
            "report_start_date": "2016-05-02",
            "report_end_date": "2016-05-17",
            "context": {
                "id": 7,
                "href": "/api/contexts/7",
                "type": "Context"
            }
        }
    }
    ```
    Response:
   ```
  {
      "audit": {
          "custom_attribute_values": [],
          "people": [],
          "object_type": "Assessment",
          "updated_at": "2016-05-19T14:44:25",
          "secondary_contact": null,
          "id": 2,
          "audit_firm": {
              "context_id": null,
              "href": "/api/org_groups/1",
              "type": "OrgGroup",
              "id": 1
          },
          "description": "",
          "object_folders": [],
          "modified_by": {
              "context_id": null,
              "href": "/api/people/1",
              "type": "Person",
              "id": 1
          },
          "title": "2016: Test Program - Audit 2",
          "program": {
              "context_id": 7,
              "href": "/api/programs/2",
              "type": "Program",
              "id": 2
          },
          "object_people": [],
          "type": "Audit",
          "start_date": "2016-05-02",
          "viewLink": "/audits/2",
          "status": "Planned",
          "gdrive_evidence_folder": null,
          "related_sources": [],
          "end_date": "2016-05-09",
          "report_end_date": "2016-05-17",
          "related_destinations": [],
          "slug": "example code",
          "url": null,
          "audit_objects": [],
          "notes": null,
          "reference_url": null,
          "contact": {
              "context_id": null,
              "href": "/api/people/1",
              "type": "Person",
              "id": 1
          },
          "context": {
              "context_id": null,
              "href": "/api/contexts/9",
              "type": "Context",
              "id": 9
          },
          "requests": [],
          "created_at": "2016-05-19T14:44:25",
          "selfLink": "/api/audits/2",
          "report_start_date": "2016-05-02"
      }
  }
   ```


## Assessment
### Overview
|||
|---|---|
|URL|/api/assessments|
|Methods supported|`POST`, `DELETE`|
|Description|Creates an assessment object. <br><br>Notes:<br> - for mapping creators, assessors and verifiers a separate request to the [relationship endpoint](#relationship) has to be made <br> - when creating assessments on the front end it's required that an object and an audit are added. The API doesn't require those fields. However if the "object" and "audit" fields are  left empty, the object will be created in the DB but will not be visible on the page.

### Elements
|Field name|Type|Description|
|---|---|---|
|**Required**|||
|title|str|Assessment title|
|context|None or [GGRC object](/src/doc/api/types.md#ggrc-object)|Context reference object|
|**Optional**|||
|description|str|Assessment description|
|notes|str|Assessment notes|
|test_plan|str|Test plan description|
|start_date|str|ISO-8601 formatted effective date|
|end_date|str|ISO-8601 formatted stop date||
|reference_url|str||
|url|str|Assessment url|
|audit|[GGRC object](/src/doc/api/types.md#ggrc-object)|Audit for assessment|
|contact|[GGRC object](/src/doc/api/types.md#ggrc-object)|Assessment creator|
|secondary_contact|[GGRC object](/src/doc/api/types.md#ggrc-object)|Secondary contact|
|design|[Assessment conclusion](/src/doc/api/types.md#assessment-conclusion)|Conclusion design|
|operationally|[Assessment conclusion](/src/doc/api/types.md#assessment-conclusion)|Conclusion operation
|object|[GGRC object](/src/doc/api/types.md#ggrc-object)|GGRC object under assessment|
|program|[GGRC object](/src/doc/api/types.md#ggrc-object)||
|recipients|str of comma separated [Recipient](/src/doc/api/types.md#recipient)|Recipients of notifications|
|Assessor|bool|Notify assessors|
|Creator|bool|Notify creators|
|Verifier|bool|Notify verifiers|
|custom_attribute_definitions|list||
|custom_attributes|||
|owners|list||
|send_by_default|bool|
|status|str||
|slug|str|Unique identifier for Assessments|
|validate_creator|bool||
|validate_assessor|bool||

### Examples
* create a new assessment

    Request:
    ```
    {
        "assessment": {
            "status": "Not Started",
            "custom_attribute_definitions": [],
            "owners": [],
            "custom_attributes": {},
            "contact": {
                "id": 1,
                "href": "/api/people/1",
                "type": "Person"
            },
            "validate_creator": true,
            "validate_assessor": true,
            "title": "Example title",
            "object": {
                "id": 1,
                "href": "/api/people/1",
                "type": "Person"
            },
            "audit": {
                "id": 1,
                "href": "/api/audits/1",
                "type": "Audit"
            },
            "description": "Example description",
            "send_by_default": true,
            "Creator": true,
            "Assessor": true,
            "Verifier": true,
            "test_plan": "Example plan",
            "secondary_contact": {
                "id": 1,
                "href": "/api/people/1",
                "type": "Person"
            },
            "notes": "Example notes",
            "url": "assessmenturl.com",
            "reference_url": "referenceurl.com",
            "slug": "Example code2",
            "design": "Ineffective",
            "operationally": "Needs improvement",
            "start_date": "2016-05-08",
            "end_date": "2016-05-18",
            "context": null,
            "recipients": "Creator,Assessor,Verifier",
            "program": {
                "id": 1,
                "href": "/api/programs/1",
                "type": "Program"
            }
        }
    }
    ```
    Response:
   ```
  {
      "assessment": {
          "custom_attribute_values": [],
          "people": [],
          "verified_date": null,
          "task_group_objects": [],
          "design": "Ineffective",
          "secondary_contact": {
              "context_id": null,
              "href": "/api/people/1",
              "type": "Person",
              "id": 1
          },
          "id": 2,
          "description": "Example description",
          "finished_date": null,
          "documents": [],
          "verified": false,
          "recipients": "Creator,Assessor,Verifier",
          "title": "Example title",
          "contact": {
              "context_id": null,
              "href": "/api/people/1",
              "type": "Person",
              "id": 1
          },
          "object_people": [],
          "type": "Assessment",
          "start_date": "2016-05-08",
          "viewLink": "/assessments/2",
          "status": "Not Started",
          "related_sources": [],
          "end_date": "2016-05-18",
          "workflow_state": null,
          "os_state": "Draft",
          "object": {},
          "updated_at": "2016-05-20T09:01:26",
          "object_documents": [],
          "modified_by": {
              "context_id": null,
              "href": "/api/people/1",
              "type": "Person",
              "id": 1
          },
          "related_destinations": [
              {
                  "context_id": null,
                  "href": "/api/relationships/None",
                  "type": "Relationship",
                  "id": null
              },
              {
                  "context_id": null,
                  "href": "/api/relationships/None",
                  "type": "Relationship",
                  "id": null
              },
              {
                  "context_id": null,
                  "href": "/api/relationships/None",
                  "type": "Relationship",
                  "id": null
              }
          ],
          "slug": "Example code2",
          "audit": {},
          "owners": [],
          "send_by_default": true,
          "url": "assessmenturl.com",
          "task_groups": [],
          "notes": "Example notes",
          "reference_url": "referenceurl.com",
          "object_owners": [],
          "test_plan": "Example plan",
          "operationally": "Needs improvement",
          "context": null,
          "created_at": "2016-05-20T09:01:26",
          "selfLink": "/api/assessments/2"
      }
  }
   ```

## Object owner
### Overview
|||
|---|---|
|URL|/api/object_owners|
|Methods supported|`POST`, `DELETE`|
|Description|Creates an object owner object.|

### Elements
|Field name|Type|Description|
|---|---|---|
|**Required**|||



## Program
### Overview
|||
|---|---|
|URL|/api/programs|
|Methods supported|`POST`, `DELETE`|
|Description|Creates a program object.|

### Elements
|Field name|Type|Description|
|---|---|---|
|**Required**|||
|title|str|Program unique title|
|context|None or [GGRC object](/src/doc/api/types.md#ggrc-object)|Context reference. When creating a new object, the value has to be set to None.
|**Optional**|||
|description|str|Program description|
|notes|str|Program notes|
|url|str|Program url|
|reference_url_url|str|Reference url|
|kind|[Program status](/src/doc/api/types.md#program-status||
|start_date|str|Effective date in MDY format e.g. "05/31/2016"
|end_date|str|Stop date in MDY format e.g. "05/31/2016"
|contact|[GGRC object](/src/doc/api/types.md#ggrc-object)|Primary contact|
|secondary_contact|None or [GGRC object](/src/doc/api/types.md#ggrc-object)|Secondary contact.|
|custom_attributes|||
|custom_attribute_definitions|list||
|status|str||
|slug|str|Unique string identifier for this program|

### Examples
* create a program

    Request:
    ```
    {
       "program":{
          "custom_attribute_definitions":[],
          "custom_attributes":{},
          "contact":{
             "id":3,
             "href":"/api/people/3",
             "type":"Person"
          },
          "kind":"Directive",
          "title":"Test title",
          "description":"Some description",
          "secondary_contact":{
             "id":4,
             "href":"/api/people/4",
             "type":"Person"
          },
          "notes":"Here are my notes",
          "url":"programurl.com",
          "reference_url":"referenceurl.com",
          "slug":"SOME CODE",
          "start_date":"05/01/2016",
          "end_date":"05/31/2016",
          "status":"Draft",
          "context":null
       }
    }
    ```
    Response:
   ```
   {
      "program":{
         "custom_attribute_values":[ ],
         "people":[],
         "updated_at":"2016-05-19T12:09:15",
         "private":false,
         "task_group_objects":[],
         "audits":[],
         "id":10,
         "description":"Some description",
         "object_folders":[],
         "documents":[],
         "modified_by":{
            "context_id":null,
            "href":"/api/people/1",
            "type":"Person",
            "id":1
         },
         "title":"Test title",
         "secondary_contact":{
            "context_id":null,
            "href":"/api/people/4",
            "type":"Person",
            "id":4
         },
         "risk_assessments":[],
         "object_people":[],
         "type":"Program",
         "start_date":"2016-05-01",
         "viewLink":"/programs/10",
         "status":"Draft",
         "related_sources":[],
         "end_date":"2016-05-31",
         "workflow_state":null,
         "os_state":"Modified",
         "risk_objects":[],
         "owners":[],
         "object_documents":[],
         "related_destinations":[],
         "slug":"SOME CODE",
         "kind":"Directive",
         "url":"programurl.com",
         "task_groups":[],
         "notes":"Here are my notes",
         "reference_url":"referenceurl.com",
         "object_owners":[],
         "contact":{
            "context_id":null,
            "href":"/api/people/3",
            "type":"Person",
            "id":3
         },
         "risks":[],
         "context":{
            "context_id":null,
            "href":"/api/contexts/17",
            "type":"Context",
            "id":17
         },
         "created_at":"2016-05-19T12:09:14",
         "selfLink":"/api/programs/10"
      }
   }
   ```


## Request
### Overview
|||
|---|---|
|URL|/api/requests|
|Methods supported|`POST`, `DELETE`|
|Description|Creates a program object.|

### Elements
|Field name|Type|Description|
|---|---|---|
|**Required**|||
|title|str|Request title|
|audit|[GGRC object](/src/doc/api/types.md#ggrc-object)|Audit mapped to this request object|
|start_date|str|ISO-8601 formatted effective date|
|end_date|str|ISO-8601 formatted stop date||
|**Optional**|||
|status|str||
|custom_attribute_definitions|list||
|custom_attributes|||
|validate_requester|bool||
|validate_assignee|bool||
|description|str|Request description|
|request_type|[Request](/src/doc/api/types.md#request||
|test|str|Test message|
|notes|str|Notes for the request|
|slug|str|Unique identifier for this request|
|context|None or [GGRC object](/src/doc/api/types.md#ggrc-object||

### Examples
* create a new request object

    Request:
    ```
    {
        "request": {
            "status": "Not Started",
            "start_date": "2016-05-20",
            "end_date": "2016-05-27",
            "custom_attribute_definitions": [],
            "custom_attributes": {},
            "validate_requester": true,
            "validate_assignee": true,
            "title": "Example title",
            "audit": {
                "id": 1,
                "href": "/api/audits/1",
                "type": "Audit"
            },
            "description": "Example descritpion",
            "request_type": "documentation",
            "test": "Example test message",
            "notes": "Example notes",
            "slug": "test code",
            "context": {
                "id": 5,
                "href": "/api/contexts/5",
                "type": "Context"
            }
        }
    }
    ```
    Response:
   ```
  {
      "request": {
          "custom_attribute_values": [],
          "people": [],
          "updated_at": "2016-05-20T10:14:42",
          "task_group_objects": [],
          "id": 1,
          "related_sources": [
              {
                  "context_id": null,
                  "href": "/api/relationships/14",
                  "type": "Relationship",
                  "id": 14
              }
          ],
          "finished_date": null,
          "object_folders": [],
          "documents": [],
          "modified_by": {
              "context_id": null,
              "href": "/api/people/1",
              "type": "Person",
              "id": 1
          },
          "recipients": null,
          "title": "Example title",
          "verified": false,
          "requestor": null,
          "object_people": [],
          "test": "Example test message",
          "type": "Request",
          "start_date": "2016-05-20",
          "viewLink": "/requests/1",
          "status": "Not Started",
          "verified_date": null,
          "description": "Example descritpion",
          "end_date": "2016-05-27",
          "workflow_state": null,
          "object_documents": [],
          "gdrive_upload_path": null,
          "related_destinations": [],
          "slug": "test code",
          "audit": {
              "context_id": 5,
              "href": "/api/audits/1",
              "type": "Audit",
              "id": 1
          },
          "send_by_default": null,
          "task_groups": [],
          "notes": "Example notes",
          "request_type": "documentation",
          "context": {
              "context_id": null,
              "href": "/api/contexts/5",
              "type": "Context",
              "id": 5
          },
          "created_at": "2016-05-20T10:14:42",
          "selfLink": "/api/requests/1"
      }
  }
   ```

### Workflow
### Overview
|||
|---|---|
|URL|/api/workflows|
|Methods supported|`POST`, `DELETE`|
|Description|Creates a workflow object. Note that if you want to connect task group to this object, a separate request to [task group](#task-group) needs to be made.|

### Elements
|Field name|Type|Description|
|---|---|---|
|**Required**|||
|title|str|Workflow title|
|context|None or [GGRC object](/src/doc/api/types.md#ggrc-object)||
|**Optional**|||
|description|str|Workflow description|
|frequency_options|list||
|frequency|[Workflow frequency](/src/doc/api/types.md#workflow-frequency)|Note that if this field isn't sent, [Workflow frequency](/src/doc/api/types.md#workflow-frequency).ONE_TIME is used|
|custom_attribute_definitions|||
|custom_attributes||
|notify_on_change|bool|Enable real time email updates|
|task_group_title|str||
|notify_custom_message|str|Custom email message|
|slug|str|Unique identifier for this workflow|
|owners|||

### Examples
* create a new workflow

    Request:
    ```
    {
      "workflow":{
         "frequency_options":[
            {
               "title":"One time",
               "value":"one_time"
            },
            {
               "title":"Weekly",
               "value":"weekly"
            },
            {
               "title":"Monthly",
               "value":"monthly"
            },
            {
               "title":"Quarterly",
               "value":"quarterly"
            },
            {
               "title":"Annually",
               "value":"annually"
            }
         ],
         "frequency":"one_time",
         "custom_attribute_definitions":[],
         "custom_attributes":{},
         "title":"Test title",
         "description":"Some description.&nbsp;<br><b>This part is bold.</b>",
         "notify_on_change":false,
         "task_group_title":"Task Group 1",
         "notify_custom_message":"Example email message.",
         "slug":"Some unique value",
         "owners":null,
         "context":null
      }
   }
    ```
    Response:
    ```
    {
        "workflow":{
           "status":"Draft",
           "notify_custom_message":"Example email message.",
           "custom_attribute_values":[

           ],
           "notify_on_change":false,
           "description":"Some description.\u00a0<br><b>This part is bold.</b>",
           "end_date":null,
           "people":[
              {
                 "context_id":null,
                 "href":"/api/people/1",
                 "type":"Person",
                 "id":1
              }
           ],
           "non_adjusted_next_cycle_start_date":null,
           "updated_at":"2016-05-19T12:57:02",
           "frequency":"one_time",
           "recurrences":false,
           "id":1,
           "object_folders":[

           ],
           "kind":null,
           "modified_by":{
              "context_id":null,
              "href":"/api/people/1",
              "type":"Person",
              "id":1
           },
           "next_cycle_start_date":null,
           "object_approval":false,
           "title":"Test title",
           "task_groups":[

           ],
           "created_at":"2016-05-19T12:57:02",
           "workflow_state":null,
           "slug":"Some unique value",
           "context":{
              "context_id":null,
              "href":"/api/contexts/4",
              "type":"Context",
              "id":4
           },
           "workflow_people":[
              {
                 "context_id":4,
                 "href":"/api/workflow_people/1",
                 "type":"WorkflowPerson",
                 "id":1
              }
           ],
           "cycles":[

           ],
           "type":"Workflow",
           "start_date":null,
           "selfLink":"/api/workflows/1",
           "viewLink":"/workflows/1"
        }
     }
    ```



### Task Group
### Overview
|||
|---|---|
|URL|/api/task_groups|
|Methods supported|`POST`, `DELETE`|
|Description|Creates a task group object|

### Elements
|Field name|Type|Description|
|---|---|---|
|**Required**|||
|title|str|Task group title|
|workflow|[GGRC object](/src/doc/api/types.md#ggrc-object)|Workgroup object reference|
|context|[GGRC object](/src/doc/api/types.md#ggrc-object)|Context reference of the referenced workgroup|
|**Optional**|||
|contact|[GGRC object](/src/doc/api/types.md#ggrc-object)||


### Examples
* map a task group to a workflow

    Request:
     ```
     {
         "task_group":{
             "title":"Task Group 1",
             "workflow":{
                "id":1,
                "href":"/api/workflows/1",
                "type":"Workflow"
             },
             "contact":{
                "id":1,
                "href":"/api/people/1",
                "type":"Person"
             },
             "context":{
                "id":4,
                "href":"/api/contexts/4",
                "type":"Context"
             }
         }
     }
     ```

    Response:

    ```
    {
        "task_group": {
            "description": null,
            "end_date": null,
            "workflow": {
                "context_id": 5,
                "href": "/api/workflows/2",
                "type": "Workflow",
                "id": 2
            },
            "updated_at": "2016-05-19T14:37:23",
            "task_group_objects": [],
            "objects": [],
            "modified_by": {
                "context_id": null,
                "href": "/api/people/1",
                "type": "Person",
                "id": 1
            },
            "secondary_contact": null,
            "id": 2,
            "slug": "TASKGROUP-2",
            "task_group_tasks": [],
            "lock_task_order": null,
            "title": "Task Group 1",
            "created_at": "2016-05-19T14:37:23",
            "sort_index": "",
            "contact": {
                "context_id": null,
                "href": "/api/people/1",
                "type": "Person",
                "id": 1
            },
            "context": {
                "context_id": null,
                "href": "/api/contexts/5",
                "type": "Context",
                "id": 5
            },
            "type": "TaskGroup",
            "start_date": null,
            "selfLink": "/api/task_groups/2"
        }
    }
    ```

## User Role
### Overview
|||
|---|---|
|URL|/api/user_roles|
|Methods supported|`POST`|
|Description|Assigns a role to an user. Note that instead of making a request to [relationship](#relationship) with source=[some_role_object] and destination=[some_user_object], this endpoint is preferred for assigning roles to users.|
### Element
|Field name|Type|Description|
|---|---|---|
|**Required**|||
|person|[GGRC object](/src/doc/api/types.md#ggrc-object)|Person we want to set the role for.|
|role|[GGRC object](/src/doc/api/types.md#ggrc-object)|Role reference.
|**Optional**||
|role_name|[Role](/src/doc/api/types.md#role)|Person role|
### Examples
* add an auditor to an audit object

    Request:
     ```
     {
         "user_role": {
             "context": {
                 "id": 11,
                 "href": "/api/contexts/11",
                 "type": "Context"
             },
             "person": {
                 "id": 1,
                 "href": "/api/people/1",
                 "type": "Person"
             },
             "role_name": "Auditor",
             "role": {
                 "id": 14,
                 "href": "/api/roles/14",
                 "type": "Role"
             }
         }
     }
     ```
    Response:
    ```
    {
        "user_role": {
            "modified_by": {
                "context_id": null,
                "href": "/api/people/1",
                "type": "Person",
                "id": 1
            },
            "created_at": "2016-05-19T14:50:24",
            "updated_at": "2016-05-19T14:50:24",
            "person": {
                "context_id": null,
                "href": "/api/people/1",
                "type": "Person",
                "id": 1
            },
            "role": {
                "context_id": null,
                "href": "/api/roles/14",
                "type": "Role",
                "id": 14
            },
            "context": {
                "context_id": null,
                "href": "/api/contexts/11",
                "type": "Context",
                "id": 11
            },
            "type": "UserRole",
            "id": 7,
            "selfLink": "/api/user_roles/7"
        }
    }
    ```


# Creating relationships between objects

## Relationship
### Overview
|||
|---|---|
|URL|/api/relationships|
|Methods supported|`POST`|
|Description|Creates a relationship between multiple object.|

### Elements
|Field name|Type|Description|
|---|---|---|
|**Required**||
|source|[GGRC object](/src/doc/api/types.md#ggrc-object)|The object we want to connect.|
|destination|[GGRC object](/src/doc/api/types.md#ggrc-object)|The object we want to connect to.|
|**Optional**||
|attrs|[GGRC attribute](/src/doc/api/types.md#ggrc-attribute)|Additional attribute options.|

### Examples
* map a person with id=1 to assessments with id=3 as assessor and verifier

    Request:
    ```
    {
        "relationship": {
            "source": {
                "id": 1,
                "href": "/api/people/1",
                "type": "Person"
            },
            "destination": {
                "id": 3,
                "href": "/api/assessments/3",
                "type": "Assessment"
            },
            "context": null,
            "attrs": {
                "AssigneeType": "Assessor,Verifier"
            }
        }
    }
    ```
    Response:
   ```
  {
      "relationship": {
          "status": "Draft",
          "modified_by": {
              "context_id": null,
              "href": "/api/people/1",
              "type": "Person",
              "id": 1
          },
          "created_at": "2016-05-20T09:19:34",
          "destination": {
              "context_id": null,
              "href": "/api/assessments/3",
              "type": "Assessment",
              "id": 3
          },
          "updated_at": "2016-05-20T09:19:34",
          "source": {
              "context_id": null,
              "href": "/api/people/3",
              "type": "Person",
              "id": 3
          },
          "attrs": {
              "AssigneeType": "Verifier,Assessor"
          },
          "context": null,
          "type": "Relationship",
          "id": 12,
          "selfLink": "/api/relationships/12"
      }
  }
   ```


