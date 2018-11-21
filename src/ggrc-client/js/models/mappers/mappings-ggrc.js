/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {
  Proxy,
  Direct,
  Search,
  Multi,
  CustomFilter,
} from '../mappers/mapper-helpers';
import Mappings from './mappings';
import CustomAttributeDefinition from '../custom-attributes/custom-attribute-definition';
import AccessControlRole from '../custom-roles/access-control-role';
import {getRoleableModels} from '../../plugins/utils/models-utils';

const businessObjects = [
  'Assessment', 'AccessGroup', 'Audit', 'Contract', 'Control', 'DataAsset',
  'Document', 'Facility', 'Issue', 'Market', 'Metric', 'Objective', 'OrgGroup',
  'Policy', 'Process', 'Product', 'ProductGroup', 'Program', 'Project',
  'Regulation', 'Requirement', 'Risk', 'Standard', 'System',
  'TechnologyEnvironment', 'Threat', 'Vendor',
];

const coreObjects = _.difference(businessObjects,
  ['Assessment', 'Audit', 'Document', 'Program']);

const scopingObjects = [
  'AccessGroup', 'DataAsset', 'Facility', 'Market', 'Metric', 'OrgGroup',
  'Process', 'Product', 'ProductGroup', 'Project', 'System',
  'TechnologyEnvironment', 'Vendor',
];

new Mappings({
  base: {},

  Person: {
    _related: ['CycleTaskGroupObjectTask', 'TaskGroupTask', 'Workflow',
      ...getRoleableModels().map((model) => model.model_singular)],
  },

  Program: {
    _canonical: [...coreObjects, 'Document'],
    _related: ['Audit', 'Person', 'TaskGroup', 'Workflow'],
  },

  Document: {
    _canonical: [...coreObjects, 'Program'],
    _related: ['Person'],
  },

  // Core objects
  Issue: {
    _canonical: [...coreObjects, 'Document', 'Program'],
    _related: ['Assessment', 'Audit', 'Person', 'TaskGroup', 'Workflow'],
  },
  Contract: {
    _canonical: _.difference(businessObjects, ['Assessment', 'Contract']),
    _related: ['Assessment', 'Person', 'TaskGroup', 'Workflow'],
  },
  Control: {
    _canonical: _.difference(businessObjects, ['Assessment']),
    _related: ['Assessment', 'Person', 'TaskGroup', 'Workflow'],
  },
  Objective: {
    _canonical: _.difference(businessObjects, ['Assessment']),
    _related: ['Assessment', 'Person', 'TaskGroup', 'Workflow'],
  },
  Policy: {
    _canonical: _.difference(businessObjects, ['Assessment', 'Policy']),
    _related: ['Assessment', 'Person', 'TaskGroup', 'Workflow'],
  },
  Requirement: {
    _canonical: _.difference(businessObjects, ['Assessment']),
    _related: ['Assessment', 'Person', 'TaskGroup', 'Workflow'],
  },
  Regulation: {
    _canonical: _.difference(businessObjects,
      [...scopingObjects, 'Assessment', 'Regulation']),
    _related:
      [...scopingObjects, 'Assessment', 'Person', 'TaskGroup', 'Workflow'],
  },
  Risk: {
    _canonical: _.difference(businessObjects, ['Assessment']),
    _related: ['Assessment', 'Person', 'TaskGroup', 'Workflow'],
  },
  Standard: {
    _canonical: _.difference(businessObjects,
      [...scopingObjects, 'Assessment', 'Standard']),
    _related:
      [...scopingObjects, 'Assessment', 'Person', 'TaskGroup', 'Workflow'],
  },
  Threat: {
    _canonical: _.difference(businessObjects, ['Assessment']),
    _related: ['Assessment', 'Person', 'TaskGroup', 'Workflow'],
  },

  // Scoping objects
  AccessGroup: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'AccessGroup', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },
  DataAsset: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },
  Facility: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },
  Market: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },
  Metric: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },
  OrgGroup: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },
  Process: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },
  Product: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },
  ProductGroup: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },
  Project: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },
  System: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },
  TechnologyEnvironment: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },
  Vendor: {
    _canonical: _.difference(businessObjects,
      ['Assessment', 'Standard', 'Regulation']),
    _related: ['Assessment', 'Person', 'Regulation', 'Standard', 'TaskGroup',
      'Workflow'],
  },

  // Audit
  Audit: {
    _canonical: coreObjects,
    _related:
      ['Assessment', 'AssessmentTemplate', 'Evidence', 'Person', 'Program'],
  },
  Assessment: {
    _canonical: coreObjects,
    _related: ['Audit', 'Evidence', 'Person'],
  },
  Evidence: {
    _related: ['Assessment', 'Audit', 'Person'],
  },
  AssessmentTemplate: {
    _related: ['Audit'],
  },

  // Workflow
  TaskGroup: {
    _canonical: [...coreObjects, 'Program'],
  },
  TaskGroupTask: {
    _related: ['Person', 'Workflow'],
  },
  Workflow: {
    _related: ['Person', 'TaskGroup', 'TaskGroupTask'],
  },
  CycleTaskGroupObjectTask: {
    // It is needed for an object list generation. This object list
    // describes which objects can be mapped to CycleTaskGroupObjectTask.
    // Types placed within this collection will be intersected
    // with TreeViewConfig.base_widgets_by_type["CycleTaskGroupObjectTask"]
    // collection. The result of the operation is the total list.
    _canonical: [...coreObjects, 'Audit', 'Program'],
    _related: ['Person'],
    // Needed for related_objects mapper
    related_objects_as_source: Proxy(
      null,
      'destination', 'Relationship',
      'source', 'related_destinations'
    ),
    // Needed for related_objects mapper
    related_objects_as_destination: Proxy(
      null,
      'source', 'Relationship',
      'destination', 'related_sources'
    ),
    // Needed to show mapped objects for CycleTaskGroupObjectTask
    related_objects: Multi(
      ['related_objects_as_source', 'related_objects_as_destination']
    ),
    /**
       * "cycle" mapper is needed for mapped objects under
       * CycleTaskGroupObjectTask into mapping-tree-view component.
       */
    cycle: Direct(
      'Cycle', 'cycle_task_group_object_tasks', 'cycle'),
    /**
       * This mapping name is needed for objects mapped to CTGOT.
       * It helps to filter results of objects mapped to CTGOT.
       * We can just remove some objects from results.
       */
    info_related_objects: CustomFilter(
      'related_objects',
      function (relatedObjects) {
        return !_.includes([
          'CycleTaskGroup',
          'Comment',
          'Document',
          'Person',
        ],
        relatedObjects.instance.type);
      }
    ),
  },

  // Other
  UserRole: {
    person: Direct('Person', 'user_roles', 'person'),
    role: Direct('Role', 'user_roles', 'role'),
  },
  MultitypeSearch: {
    _canonical: [
      'AccessGroup', 'Assessment', 'AssessmentTemplate', 'Audit',
      'Contract', 'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
      'Document', 'Evidence', 'Facility', 'Issue', 'Market', 'Metric',
      'Objective', 'OrgGroup', 'Person', 'Process', 'Product',
      'ProductGroup', 'Project', 'Policy', 'Program', 'Regulation',
      'Requirement', 'Risk', 'Standard', 'System', 'TaskGroup',
      'TaskGroupTask', 'TechnologyEnvironment', 'Threat',
      'Vendor', 'Workflow',
    ],
  },
  // Used by Custom Attributes widget
  CustomAttributable: {
    custom_attribute_definitions: Search(function (binding) {
      return CustomAttributeDefinition.findAll({
        definition_type: binding.instance.root_object,
        definition_id: null,
      });
    }, 'CustomAttributeDefinition'),
  },
  // used by the Custom Roles admin panel tab
  Roleable: {
    access_control_roles: Search(function (binding) {
      return AccessControlRole.findAll({
        object_type: binding.instance.model_singular,
        internal: false,
      });
    }, 'AccessControlRole'),
  },
});
