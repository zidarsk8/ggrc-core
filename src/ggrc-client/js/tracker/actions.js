/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

// Timing Category in Google Analytics Timing API
export const FOCUS_AREAS = {
  ASSESSMENT: 'Assessment',
  AUDIT: 'Audit',
  RELATED_ASSESSMENTS: 'Related Assessments',
  SNAPSHOTS: 'Snapshots',
  IMPORT_AND_EXPORT: 'Import/Export',
  LHN: 'LHN',
  MAPPINGS: (type) => `Mappings to ${type}`,
};

// Timing Variable in Google Analytics Timing API
export const USER_JOURNEY_KEYS = {
  LOADING: 'Loading',
  NAVIGATION: 'Navigation',
  ATTACHMENTS: 'Attachments',
  TREEVIEW: 'TreeView',
  MAP_OBJECTS: (type) => `Mapped type: ${type}`,
  API: 'API Methods',
  INFO_PANE: 'Info Pane',
};

// Timing Label in Google Analytics Timing API
export const USER_ACTIONS = {
  CREATE_OBJECT: 'Creating new object',
  UPDATE_OBJECT: 'Updating object',
  LOAD_OBJECT: 'Loading object',
  MAPPING_OBJECTS: (count) => `Mapping objects: ${count}`,
  ADD_ATTACHMENT: (count) => `Attachment of ${count} file(s)`,
  ADD_ATTACHMENT_TO_FOLDER: (count) =>
    `Attachment to folder of ${count} file(s)`,
  ADVANCED_SEARCH_FILTER: 'Advanced search filter',
  TREEVIEW: {
    FILTER: 'Tree view filter',
    TREE_VIEW_PAGE_LOADING: 'Loading of tree view page',
    SUB_TREE_LOADING: 'Loading sub-level of tree view',
  },
  INFO_PANE: {
    OPEN_INFO_PANE: 'Open Info pane',
    ADD_COMMENT_TO_LCA: 'Adding a comment to LCA value',
    ADD_COMMENT: 'Adding a comment',
  },
  LHN: {
    SHOW_LIST: 'LHN: Show list of items',
    SHOW_MORE: 'LHN: Show more items for the list',
  },
  ASSESSMENT: {
    OPEN_ASMT_GEN_MODAL: 'Open Assessment Generation modal',
    CHANGE_STATUS: 'Changing status of Assessment',
    EDIT_LCA: 'Editing Local CA',
  },
  CYCLE_TASK: {
    CHANGE_STATUS: 'Changing status of Task',
    BULK_UPDATE: 'Bulk update',
  },
};
