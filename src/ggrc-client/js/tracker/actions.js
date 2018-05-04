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
};

// Timing Variable in Google Analytics Timing API
export const USER_JOURNEY_KEYS = {
  LOADING: 'Loading',
  NAVIGATION: 'Navigation',
  ADD_ATTACHMENT: 'Add attachment',
  MAPPING_TO_OBJECT: 'Mapping to object',
  API: 'API Methods',
};

// Timing Label in Google Analytics Timing API
export const USER_ACTIONS = {
  CREATE_OBJECT: 'Creating new object',
  UPDATE_OBJECT: 'Updating object',
  LOAD_OBJECT: 'Loading object',
  MULTISELECT_FILTER: 'Multi-select filter',
  TREE_VIEW_PAGE_LOADING: 'Loading of tree view page',
  OPEN_INFO_PANE: 'Open Info pane',
  ADVANCED_SEARCH_FILTER: 'Advanced search filter',
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
