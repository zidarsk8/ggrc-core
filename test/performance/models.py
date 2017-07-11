# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Basic GGRC models information for locust tests.

This module contains all model names and needed mappings that are normally
available in the GGRC app.

Items:
  - ROLES = role id to role name map.
  - ROLES_REV = role name to role id map.
  - DEFAULT_USER = default user with superuser rights.
  - CAD_TYPES = types of custom attribute definitions.
  - CUSTOM_ATTRIBUTABLE = List of models that are custom attributable.
  - CUSTOM_ROLABLE = List of models with ACL roles.
  - MODELS = List of all model names
  - TITLES_SINGULAR = Model name to title singular map
  - TITLES_PLURAL = Model name to title plural map
  - TABLES_SINGULAR = Model name to singular table name map
  - TABLES_SINGULAR_REV = Singular table name map to model name
  - TABLES_PLURAL = Model name to plural table name map
  - INITIAL_MODELS = Models that get loaded on every test start
"""

# role ids read from the database after a clean migration.
ROLES = {
    1: "ProgramOwner",
    2: "ProgramEditor",
    3: "ProgramReader",
    5: "Reader",
    6: "Editor",
    8: "Administrator",
    9: "AuditorReader",
    10: "AuditorProgramReader",
    11: "ProgramAuditOwner",
    12: "ProgramAuditEditor",
    13: "ProgramAuditReader",
    14: "Auditor",
    15: "ProgramBasicReader",
    16: "ProgramMappingEditor",
    17: "Creator",
    18: "WorkflowOwner",
    19: "WorkflowMember",
    20: "BasicWorkflowReader",
    21: "WorkflowBasicReader",
}

GLOBAL_ROLES = [
    "Reader",
    "Editor",
    "Administrator",
    "Creator",
]

ROLES_REV = {v: k for k, v in ROLES.items()}

DEFAULT_USER = {
    "id": 1,
    "href": "/api/people/1",
    "type": "Person",
    "name": "Example User",
    "email": "user@example.com",
}

CAD_TYPES = [
    "Map:Person",
    "Dropdown",
    "Checkbox",
    "Date",
    "Rich Text",
    "Text",
]

CUSTOM_ATTRIBUTABLE = {
    'AccessGroup',
    'Assessment',
    'Audit',
    'Clause',
    'Contract',
    'Control',
    'DataAsset',
    'Facility',
    'Issue',
    'Market',
    'Objective',
    'OrgGroup',
    'Person',
    'Policy',
    'Process',
    'Product',
    'Program',
    'Project',
    'Regulation',
    'RiskAssessment',
    'Risk',
    'Section',
    'Standard',
    'System',
    'Threat',
    'Vendor',
    'Workflow',
}

CUSTOM_ROLABLE = {
    'Processes',
    'Projects',
    'Facilities',
    'Products',
    'Data Assets',
    'Markets',
    'Systems',
    'Access Groups',
    'Vendors',
    'Org Groups',
    'Regulations',
    'Policies',
    'Contracts',
    'Controls',
    'Sections',
    'Clauses',
    'Standards',
    'Objectives',
    'Assessments',
    'Programs',
    'Issues',
    'Risks',
    'Threats',
}

MODELS = {
    'AccessControlRole',
    'AccessGroup',
    'Assessment',
    'AssessmentTemplate',
    'Audit',
    'AuditObject',
    'Categorization',
    'CategoryBase',
    'ControlCategory',
    'ControlAssertion',
    'Context',
    'Control',
    'Comment',
    'CustomAttributeDefinition',
    'CustomAttributeValue',
    'DataAsset',
    'Directive',
    'Contract',
    'Policy',
    'Regulation',
    'Standard',
    'Document',
    'Facility',
    'Market',
    'Meeting',
    'Objective',
    'ObjectOwner',
    'ObjectPerson',
    'Option',
    'OrgGroup',
    'Vendor',
    'Person',
    'Product',
    'Program',
    'Project',
    'Relationship',
    'Section',
    'Clause',
    'SystemOrProcess',
    'System',
    'Process',
    'Revision',
    'Event',
    'BackgroundTask',
    'NotificationConfig',
    'Issue',
    'Snapshot',
    'Role',
    'UserRole',
    'TaskGroup',
    'TaskGroupObject',
    'TaskGroupTask',
    'Workflow',
    'WorkflowPerson',
    'Cycle',
    'CycleTaskEntry',
    'CycleTaskGroup',
    'CycleTaskGroupObjectTask',
    'RiskAssessment',
    'Risk',
    'RiskObject',
    'Threat',
    'ObjectEvent',
    'ObjectFile',
    'ObjectFolder',
}

TITLES_SINGULAR = {
    'AccessControlRole': 'access control role',
    'AccessGroup': 'access group',
    'Assessment': 'assessment',
    'AssessmentTemplate': 'assessment template',
    'Audit': 'audit',
    'AuditObject': 'audit object',
    'BackgroundTask': 'background task',
    'Categorization': 'categorization',
    'CategoryBase': 'category base',
    'Clause': 'clause',
    'Comment': 'comment',
    'Context': 'context',
    'Contract': 'contract',
    'Control': 'control',
    'ControlAssertion': 'control assertion',
    'ControlCategory': 'control category',
    'CustomAttributeDefinition': 'custom attribute definition',
    'CustomAttributeValue': 'custom attribute value',
    'Cycle': 'cycle',
    'CycleTaskEntry': 'cycle task entry',
    'CycleTaskGroup': 'cycle task group',
    'CycleTaskGroupObjectTask': 'cycle task',
    'DataAsset': 'data asset',
    'Directive': 'directive',
    'Document': 'document',
    'Event': 'event',
    'Facility': 'facility',
    'Issue': 'issue',
    'Market': 'market',
    'Meeting': 'meeting',
    'NotificationConfig': 'notification config',
    'ObjectEvent': 'object event',
    'ObjectFile': 'object file',
    'ObjectFolder': 'object folder',
    'ObjectOwner': 'object owner',
    'ObjectPerson': 'object person',
    'Objective': 'objective',
    'Option': 'option',
    'OrgGroup': 'org group',
    'Person': 'person',
    'Policy': 'policy',
    'Process': 'process',
    'Product': 'product',
    'Program': 'program',
    'Project': 'project',
    'Regulation': 'regulation',
    'Relationship': 'relationship',
    'Revision': 'revision',
    'Risk': 'risk',
    'RiskAssessment': 'risk assessment',
    'RiskObject': 'risk object',
    'Role': 'role',
    'Section': 'section',
    'Snapshot': 'snapshot',
    'Standard': 'standard',
    'System': 'system',
    'SystemOrProcess': 'system or process',
    'TaskGroup': 'task group',
    'TaskGroupObject': 'task group object',
    'TaskGroupTask': 'task group task',
    'Threat': 'threat',
    'UserRole': 'user role',
    'Vendor': 'vendor',
    'Workflow': 'workflow',
    'WorkflowPerson': 'workflow person'
}

TITLES_PLURAL = {
    'AccessControlRole': 'Access Control Roles',
    'AccessGroup': 'Access Groups',
    'Assessment': 'Assessments',
    'AssessmentTemplate': 'Assessment Templates',
    'Audit': 'Audits',
    'AuditObject': 'Audit Objects',
    'BackgroundTask': 'Background Tasks',
    'Categorization': 'Categorizations',
    'CategoryBase': 'Category Bases',
    'Clause': 'Clauses',
    'Comment': 'Comments',
    'Context': 'Contexts',
    'Contract': 'Contracts',
    'Control': 'Controls',
    'ControlAssertion': 'Control Assertions',
    'ControlCategory': 'Control Categories',
    'CustomAttributeDefinition': 'Custom Attribute Definitions',
    'CustomAttributeValue': 'Custom Attribute Values',
    'Cycle': 'Cycles',
    'CycleTaskEntry': 'Cycle Task Entries',
    'CycleTaskGroup': 'Cycle Task Groups',
    'CycleTaskGroupObjectTask': 'Cycle Tasks',
    'DataAsset': 'Data Assets',
    'Directive': 'Directives',
    'Document': 'Documents',
    'Event': 'Events',
    'Facility': 'Facilities',
    'Issue': 'Issues',
    'Market': 'Markets',
    'Meeting': 'Meetings',
    'NotificationConfig': 'Notification Configs',
    'ObjectEvent': 'Object Events',
    'ObjectFile': 'Object Files',
    'ObjectFolder': 'Object Folders',
    'ObjectOwner': 'Object Owners',
    'ObjectPerson': 'Object People',
    'Objective': 'Objectives',
    'Option': 'Options',
    'OrgGroup': 'Org Groups',
    'Person': 'People',
    'Policy': 'Policies',
    'Process': 'Processes',
    'Product': 'Products',
    'Program': 'Programs',
    'Project': 'Projects',
    'Regulation': 'Regulations',
    'Relationship': 'Relationships',
    'Revision': 'Revisions',
    'Risk': 'Risks',
    'RiskAssessment': 'Risk Assessments',
    'RiskObject': 'Risk Objects',
    'Role': 'Roles',
    'Section': 'Sections',
    'Snapshot': 'Snapshots',
    'Standard': 'Standards',
    'System': 'Systems',
    'SystemOrProcess': 'Systems Or Processes',
    'TaskGroup': 'Task Groups',
    'TaskGroupObject': 'Task Group Objects',
    'TaskGroupTask': 'Task Group Tasks',
    'Threat': 'Threats',
    'UserRole': 'User Roles',
    'Vendor': 'Vendors',
    'Workflow': 'Workflows',
    'WorkflowPerson': 'Workflow People'
}

TABLES_SINGULAR = {
    'AccessControlRole': 'access_control_role',
    'AccessGroup': 'access_group',
    'Assessment': 'assessment',
    'AssessmentTemplate': 'assessment_template',
    'Audit': 'audit',
    'AuditObject': 'audit_object',
    'BackgroundTask': 'background_task',
    'Categorization': 'categorization',
    'CategoryBase': 'category_base',
    'Clause': 'clause',
    'Comment': 'comment',
    'Context': 'context',
    'Contract': 'contract',
    'Control': 'control',
    'ControlAssertion': 'control_assertion',
    'ControlCategory': 'control_category',
    'CustomAttributeDefinition': 'custom_attribute_definition',
    'CustomAttributeValue': 'custom_attribute_value',
    'Cycle': 'cycle',
    'CycleTaskEntry': 'cycle_task_entry',
    'CycleTaskGroup': 'cycle_task_group',
    'CycleTaskGroupObjectTask': 'cycle_task_group_object_task',
    'DataAsset': 'data_asset',
    'Directive': 'directive',
    'Document': 'document',
    'Event': 'event',
    'Facility': 'facility',
    'Issue': 'issue',
    'Market': 'market',
    'Meeting': 'meeting',
    'NotificationConfig': 'notification_config',
    'ObjectEvent': 'object_event',
    'ObjectFile': 'object_file',
    'ObjectFolder': 'object_folder',
    'ObjectOwner': 'object_owner',
    'ObjectPerson': 'object_person',
    'Objective': 'objective',
    'Option': 'option',
    'OrgGroup': 'org_group',
    'Person': 'person',
    'Policy': 'policy',
    'Process': 'process',
    'Product': 'product',
    'Program': 'program',
    'Project': 'project',
    'Regulation': 'regulation',
    'Relationship': 'relationship',
    'Revision': 'revision',
    'Risk': 'risk',
    'RiskAssessment': 'risk_assessment',
    'RiskObject': 'risk_object',
    'Role': 'role',
    'Section': 'section',
    'Snapshot': 'snapshot',
    'Standard': 'standard',
    'System': 'system',
    'SystemOrProcess': 'system_or_process',
    'TaskGroup': 'task_group',
    'TaskGroupObject': 'task_group_object',
    'TaskGroupTask': 'task_group_task',
    'Threat': 'threat',
    'UserRole': 'user_role',
    'Vendor': 'vendor',
    'Workflow': 'workflow',
    'WorkflowPerson': 'workflow_person'
}

TABLES_SINGULAR_REV = {v: k for k, v in TABLES_SINGULAR.items()}

TABLES_PLURAL = {
    'AccessControlRole': 'access_control_roles',
    'AccessGroup': 'access_groups',
    'Assessment': 'assessments',
    'AssessmentTemplate': 'assessment_templates',
    'Audit': 'audits',
    'AuditObject': 'audit_objects',
    'BackgroundTask': 'background_tasks',
    'Categorization': 'categorizations',
    'CategoryBase': 'category_bases',
    'Clause': 'clauses',
    'Comment': 'comments',
    'Context': 'contexts',
    'Contract': 'contracts',
    'Control': 'controls',
    'ControlAssertion': 'control_assertions',
    'ControlCategory': 'control_categories',
    'CustomAttributeDefinition': 'custom_attribute_definitions',
    'CustomAttributeValue': 'custom_attribute_values',
    'Cycle': 'cycles',
    'CycleTaskEntry': 'cycle_task_entries',
    'CycleTaskGroup': 'cycle_task_groups',
    'CycleTaskGroupObjectTask': 'cycle_task_group_object_tasks',
    'DataAsset': 'data_assets',
    'Directive': 'directives',
    'Document': 'documents',
    'Event': 'events',
    'Facility': 'facilities',
    'Issue': 'issues',
    'Market': 'markets',
    'Meeting': 'meetings',
    'NotificationConfig': 'notification_configs',
    'ObjectEvent': 'object_events',
    'ObjectFile': 'object_files',
    'ObjectFolder': 'object_folders',
    'ObjectOwner': 'object_owners',
    'ObjectPerson': 'object_people',
    'Objective': 'objectives',
    'Option': 'options',
    'OrgGroup': 'org_groups',
    'Person': 'people',
    'Policy': 'policies',
    'Process': 'processes',
    'Product': 'products',
    'Program': 'programs',
    'Project': 'projects',
    'Regulation': 'regulations',
    'Relationship': 'relationships',
    'Revision': 'revisions',
    'Risk': 'risks',
    'RiskAssessment': 'risk_assessments',
    'RiskObject': 'risk_objects',
    'Role': 'roles',
    'Section': 'sections',
    'Snapshot': 'snapshots',
    'Standard': 'standards',
    'System': 'systems',
    'SystemOrProcess': 'systems_or_processes',
    'TaskGroup': 'task_groups',
    'TaskGroupObject': 'task_group_objects',
    'TaskGroupTask': 'task_group_tasks',
    'Threat': 'threats',
    'UserRole': 'user_roles',
    'Vendor': 'vendors',
    'Workflow': 'workflows',
    'WorkflowPerson': 'workflow_people'
}


SPECIAL_INITIAL_MODELS = [
    'AccessControlRole',
    # 'Person',
    'UserRole',
]

INITIAL_MODELS = [
    'AccessGroup',
    'Assessment',
    'AssessmentTemplate',
    'Audit',
    'Control',
    'DataAsset',
    'Contract',
    'Policy',
    'Regulation',
    'Standard',
    'Facility',
    'Market',
    'Objective',
    'OrgGroup',
    'Vendor',
    'Person',
    'Product',
    'Program',
    'Project',
    'Section',
    'Clause',
    'Snapshot',
    'System',
    'Process',
    'Issue',
    'TaskGroup',
    'TaskGroupObject',
    'TaskGroupTask',
    'Workflow',
    'WorkflowPerson',
    'Cycle',
    'CycleTaskEntry',
    'CycleTaskGroup',
    'CycleTaskGroupObjectTask',
    'RiskAssessment',
    'Risk',
    'Threat',
]
