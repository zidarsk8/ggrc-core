# cache/cache.py
#
# This module is abstract class for local cache mechanism
#
# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: chandramouliv@google.com
# Maintained By: chandramouliv@google.com
#

from collections import namedtuple
CacheEntry = namedtuple('CacheEntry', 'model_plural class_name cache_type')

def resource(model_plural, class_name, cache_type='local'):
#def resource(model_plural, class_name, cache_type='memcache'):
  return CacheEntry(model_plural, class_name, cache_type)

def all_cache_entries():
  ret = [
   resource('tasks','Task'),
   resource('audits','Audit'),
   resource('categorizations','Categorization'),
   resource('category_bases', 'CategoryBase'),
   resource('control_categories', 'ControlCategory'),
   resource('control_assertions', 'ControlAssertion'),
   resource('contexts', 'Context'),
   resource('controls', 'Control'),
   resource('control_controls', 'ControlControl'),
   resource('control_sections', 'ControlSection'),
   resource('data_assets', 'DataAsset'),
   resource('directives', 'Directive'),
   resource('contracts', 'Contract'),
   resource('policies', 'Policy'),
   resource('regulations', 'Regulation'),
   resource('standards', 'Standard'),
   resource('directive_controls', 'DirectiveControl'),
   resource('documents', 'Document'),
   resource('events', 'Event'),
   resource('facilities', 'Facility'),
   resource('helps', 'Help'),
   resource('markets', 'Market'),
   resource('meetings', 'Meeting'),
   resource('object_controls', 'ObjectControl'),
   resource('object_documents', 'ObjectDocument'),
   resource('object_objectives', 'ObjectObjective'),
   resource('object_owners', 'ObjectOwner'),
   resource('object_people', 'ObjectPerson'),
   resource('object_sections', 'ObjectSection'),
   resource('objectives', 'Objective'),
   resource('objective_controls', 'ObjectiveControl'),
   resource('options', 'Option'),
   resource('org_groups', 'OrgGroup'),
   resource('people', 'Person'),
   resource('products', 'Product'),
   resource('projects', 'Project'),
   resource('programs', 'Program'),
   resource('program_controls', 'ProgramControl'),
   resource('program_directives', 'ProgramDirective'),
   resource('relationships', 'Relationship'),
   resource('relationship_types', 'RelationshipType'),
   resource('requests', 'Request'),
   resource('responses', 'Response'),
   resource('documentation_responses', 'DocumentationResponse'),
   resource('interview_responses', 'InterviewResponse'),
   resource('population_sample_responses', 'PopulationSampleResponse'),
   resource('revisions', 'Revision'),
   resource('sections', 'Section'),
   resource('section_objectives', 'SectionObjective'),
   resource('systems_or_processes', 'SystemOrProcess'),
   resource('systems', 'System'),
   resource('processes', 'Process'),
   resource('roles', 'Role'),
   resource('user_roles', 'UserRole'),
   resource('object_folders', 'ObjectFolder'),
   resource('object_files', 'ObjectFile'),
   resource('object_events', 'ObjectEvent'),
   resource('templates', 'Template'),
   resource('risk_assessments', 'RiskAssessment'),
   resource('risk_assessment_mappings', 'RiskAssessmentMapping'),
   resource('risk_assessment_control_mappings', 'RiskAssessmentControlMapping'),
   resource('threats', 'Threat'),
   resource('vulnerabilities', 'Vulnerability'),
  ]

  return ret

class Cache:
  name = None
  config = None
  supported_resources = {}

  def __init__(self, configparam):
    pass

  def get_name(self):
    return None

  def set_config(self, configparam):
    pass
	
  def get_config(self):
    return None

  def get(self, category, resource, filter): 
    return None

  def add(self, category, resource, data): 
    return None

  def update(self, category, resource, data): 
    return None

  def remove(self, category, resource, data): 
    return None

  def clean(self):
    return False

  # Get the Cache key for the specified category and resource
  #
  def get_key(self, category, resource):
    cache_key = category + ":" + resource
    return cache_key

  # parse the filter for incoming request and extracts the 'ids' and 'attrs'
  # This is used for GET collection 
  #
  def parse_filter(self, filter):
    ids = None
    attrs = None

    ids_exist = filter.has_key('ids')
    attrs_exist = filter.has_key('attrs')

    if ids_exist or attrs_exist:
      if ids_exist and attrs_exist:
        ids=filter.get('ids')
        attrs=filter.get('attrs')
      elif ids_exist:
        ids=filter.get('ids')
      else:
        attrs=filter.get('attrs')

    return ids, attrs

  def is_caching_supported(self, category, resource):
    if category is not 'collection':
      return False

    return self.supported_resources.has_key(resource)
