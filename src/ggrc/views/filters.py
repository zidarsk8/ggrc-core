
from ggrc.app import app
import ggrc.views
"""Filters for GRC specific Jinja processing
"""

@app.template_filter("viewlink")
def view_link_filter(obj):
  """Create a view link for an object, that navigates
  to its object-view page in the app
  """
  view = getattr(ggrc.views, obj.__class__.__name__, None)
  return view.url_for(obj) if view else None

@app.template_filter("display_class")
def get_display_class_filter(obj):
  """Return the display class for an instance, model, or name.
  Returns one of 'business', 'governance', 'risk', 'programs'.
  """
  from ggrc.models.mixins import Base
  from ggrc.models import get_model
  if isinstance(obj, type):
    obj = obj.__name__
  elif isinstance(obj, Base):
    obj = obj.__class__.__name__

  if isinstance(obj, (str, unicode)):
    model = get_model(obj)
    obj = model._inflector.model_singular

  if obj in ('Program'):
    return 'program'
  elif obj in ('Control', 'Directive', 'Contract', 'Policy', 'Regulation'):
    return 'governance'
  elif obj in (
      'OrgGroup', 'Project', 'Facility', 'Product', 'DataAsset', 'Market',
      'System', 'Process'):
    return 'business'
  elif obj in ('Risk', 'RiskyAttribute'):
    return 'risk'
  else:
    return ''


# Additional generic filters
#

@app.template_filter("underscore")
def underscore_filter(s):
  """Change spaces to underscores and make lowercase
  """
  return "_".join(s.lower().split(' '))

@app.template_filter("nospace")
def nospace_filter(s):
  """Remove spaces
  """
  return "".join(s.split(' '))
