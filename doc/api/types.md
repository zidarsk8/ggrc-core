## Objects
### GGRC object
|Field name|Type|Description|
|---|---|---|
|id|int|object id|
|href|str|uri reference e.g. "/api/programs/12"|
|type|str|[GGRC object type](#ggrc-object-type)|

### GGRC attribute
|Field name|Type|Description|
|---|---|---|
|AssigneeType|str|comma seperated sequence of [Assignee Type](#assignee-type)|


## Types
### Audit status
||
|---|
|Planned|
|In Progress|
|Manager Review|
|Ready for External Review|
|Completed|

### Assignee Type
||
|---|
|Assessor|
|Verifier|

### Assessment conclusion
||
|---|
|Effective|
|Ineffective|
|Needs improvement|
|Not Applicable|

### GGRC object Type
||
|---|
|Audit|
|AccessGroup|
|Assessment|
|Context|
|Clause|
|Contract|
|Control|
|CycleTaskGroupObjectTask|
|DataAsset|
|Facility|
|Issue|
|Market|
|Objective|
|OrgGroup|
|Person|
|Policy|
|Process|
|Product|
|Program|
|Project|
|Regulation|
|Relationship|
|Request|
|Request
|Risk||
|Section|
|Standard|
|System|
|Threat|
|TaskGroup|
|Vendor|
|Workflow|
|WorkflowPerson|

### Recipient
||
|---|
|Creator|
|Assessor|
|Verifier|

### Role
||
|---|
|Auditor|
|AuditorProgramReader|
|AuditorReader|
|ObjectEditor|
|ProgramBasicReader|
|ProgramReader|
|ProgramCreator|
|ProgramOwner|
|ProgramEditor|
|ProgramAuditOwner|
|ProgramAuditEditor|
|ProgramAuditReader|
|Reader|

### Program status
||
|---|
|Draft|
|Final|
|Effective|
|Ineffective|
|Launched|
|Not Launched|
|In Scope|
|Not in Scope|
|Deprecated|

### Request
||
|---|
|documentation|
|interview|

### Workflow frequency
||
|---|
|one_time|
|weekly|
|monthly|
|quarterly|
|annualy|