/*
 * Copyright (C) 2018 Google Inc.
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {
  Proxy,
  Multi,
  TypeFilter,
} from '../models/mappers/mapper-helpers';
import Mappings from '../models/mappers/mappings';
import {registerHook} from '../plugins/ggrc_utils';
import {getPageInstance} from '../plugins/utils/current-page-utils';

(function ($, CMS, GGRC) {
  let RisksExtension = {};

  // Insert risk mappings to all gov/business object types
  let riskObjectTypes = [
    'AccessGroup',
    'Assessment',
    'Clause',
    'Contract',
    'Control',
    'DataAsset',
    'Document',
    'Facility',
    'Issue',
    'Market',
    'Metric',
    'MultitypeSearch',
    'Objective',
    'OrgGroup',
    'Person',
    'Policy',
    'Process',
    'Product',
    'ProductGroup',
    'Program',
    'Project',
    'Regulation',
    'Requirement',
    'Standard',
    'System',
    'TechnologyEnvironment',
    'Vendor',
  ];

  // Register `risks` extension with GGRC
  GGRC.extensions.push(RisksExtension);

  RisksExtension.name = 'risks';

  // Configure mapping extensions for ggrc_risks
  RisksExtension.init_mappings = function () {
    // Add mappings for risk objects
    let mappings = {
      related: {
        related_objects_as_source: Proxy(null, 'destination', 'Relationship',
          'source', 'related_destinations'),
        related_objects_as_destination: Proxy(
          null, 'source', 'Relationship', 'destination', 'related_sources'),
        related_objects:
          Multi(['related_objects_as_source', 'related_objects_as_destination']),
      },
      related_objects: {
        _canonical: {
          related_objects_as_source: riskObjectTypes,
        },
        related_programs: TypeFilter('related_objects', 'Program'),
        related_data_assets: TypeFilter('related_objects', 'DataAsset'),
        related_access_groups: TypeFilter('related_objects', 'AccessGroup'),
        related_facilities: TypeFilter('related_objects', 'Facility'),
        related_markets: TypeFilter('related_objects', 'Market'),
        related_metrics: TypeFilter('related_objects', 'Metric'),
        related_processes: TypeFilter('related_objects', 'Process'),
        related_products: TypeFilter('related_objects', 'Product'),
        related_product_groups: TypeFilter('related_objects', 'ProductGroup'),
        related_projects: TypeFilter('related_objects', 'Project'),
        related_systems: TypeFilter('related_objects', 'System'),
        related_controls: TypeFilter('related_objects', 'Control'),
        related_clauses: TypeFilter('related_objects', 'Clause'),
        related_requirements: TypeFilter('related_objects', 'Requirement'),
        related_regulations: TypeFilter('related_objects', 'Regulation'),
        related_contracts: TypeFilter('related_objects', 'Contract'),
        related_policies: TypeFilter('related_objects', 'Policy'),
        related_standards: TypeFilter('related_objects', 'Standard'),
        related_objectives: TypeFilter('related_objects', 'Objective'),
        related_issues: TypeFilter('related_objects', 'Issue'),
        related_assessments: TypeFilter('related_objects', 'Assessment'),
        related_people: TypeFilter('related_objects', 'Person'),
        related_org_groups: TypeFilter('related_objects', 'OrgGroup'),
        related_vendors: TypeFilter('related_objects', 'Vendor'),
        related_technology_environments: TypeFilter('related_objects',
          'TechnologyEnvironment'),

      },
      related_risk: {
        _canonical: {
          related_objects_as_source: ['Risk'].concat(riskObjectTypes),
        },
        related_risks: TypeFilter('related_objects', 'Risk'),
      },
      related_threat: {
        _canonical: {
          related_objects_as_source: ['Threat'].concat(riskObjectTypes),
        },
        related_threats: TypeFilter('related_objects', 'Threat'),
      },
      Risk: {
        _mixins: ['related', 'related_objects', 'related_threat'],
        orphaned_objects: Multi([]),
      },
      Threat: {
        _mixins: ['related', 'related_objects', 'related_risk'],
        orphaned_objects: Multi([]),
      },
    };

    can.each(riskObjectTypes, function (type) {
      mappings[type] = _.assign(mappings[type] || {}, {
        _canonical: {
          related_objects_as_source: ['Risk', 'Threat'],
        },
        _mixins: ['related', 'related_risk', 'related_threat'],
      });
    });
    new Mappings('ggrc_risks', mappings);
  };

  registerHook('LHN.Requirements_risk',
    GGRC.mustache_path + '/dashboard/lhn_risks');

  RisksExtension.init_mappings();
})(window.can.$, window.CMS, window.GGRC);
