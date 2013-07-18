"""Provide commonly-used methods here.

Don't use ``@when``, ``@given``, etc. here, as it will raise
``behave.step_registry.AmbiguousStep``, since this module is included in
multiple steps/*.py modules.
"""

import json
import datetime
from factories import factory_for, FactoryStubMarker
import requests

class Example(object):
  """An example resource for use in a behave scenario, by name."""
  def __init__(self, resource_type, value, response=None):
    self.resource_type = resource_type
    self.value = value
    self.response = response

  def get(self, attr):
    return self.value.get(get_resource_table_singular(self.resource_type)).get(attr)

  def set(self, attr, value):
    self.value[attr] = value

def set_property(obj, attr, value):
  if isinstance(obj, Example):
    obj.set(attr, value)
  else:
    setattr(obj, attr, value)


def handle_example_resource(context, resource_type):
  resource_factory = factory_for(resource_type)
  context.example_resource = resource_factory()

def handle_named_example_resource(context, resource_type, name, **kwargs):
  resource_factory = factory_for(resource_type)
  example = Example(resource_type, resource_factory(**kwargs))
  setattr(context, name, example)

def handle_get_resource_and_name_it(context, url, name):
  response = get_resource(context, url)
  assert response.status_code == 200
  setattr(context, name, response.json())

def get_resource(context, url):
  headers={'Accept': 'application/json',}
  if hasattr(context, 'current_user_json'):
    headers['X-ggrc-user'] = context.current_user_json
  response = requests.get(
      context.base_url+url,
      headers=headers,
      cookies=getattr(context, 'cookies', {})
      )
  context.cookies = response.cookies
  return response

def put_resource(context, url, resource):
  headers={
      'Content-Type': 'application/json',
      'If-Match': resource.response.headers['Etag'],
      'If-Unmodified-Since': resource.response.headers['Last-Modified'],
      }
  if hasattr(context, 'current_user_json'):
    headers['X-ggrc-user'] = context.current_user_json
  data = json.dumps(resource.value, cls=DateTimeEncoder)
  response = requests.put(
      context.base_url+url,
      data=data,
      headers=headers,
      cookies=getattr(context, 'cookies', {})
      )
  context.cookies = response.cookies
  return response

def handle_get_example_resource(context, name, expected_status=200):
  example = getattr(context, name)
  url = example.get('selfLink')
  response = get_resource(context, url)
  assert response.status_code == expected_status
  if expected_status == 200 or expected_status == 201:
    example = Example(
        example.resource_type, response.json(), response=response)
    setattr(context, name, example)

def handle_post_named_example_to_collection_endpoint(
    context, name, expected_status=201):
  """Create a new resource for the given example. Expects that there is a
  `service_description` in `context` to use to lookup the endpoint url. The
  created resource is added to the context as the attribute name given by
  `name`.
  """
  handle_post_named_example(context, name, expected_status)

def handle_post_named_example(context, name, expected_status=201):
  example = getattr(context, name)
  response = post_example(
      context, example.resource_type, example.value)
  assert response.status_code == expected_status, \
      'Expected status code {0}, received {1}'\
        .format(expected_status, response.status_code)
  if expected_status == 200 or expected_status == 201:
    example = Example(example.resource_type, response.json())
    setattr(context, name, example)

def post_example(context, resource_type, example, url=None, context_id=None):
  if context_id is None:
    context_id = example.get("context_id", None)
  if url is None:
    url = get_service_endpoint_url(context, resource_type)

  # Find any required FactoryStubMarker and recurse to POST/create
  # required resources
  for attr, value in example.items():
    if isinstance(value, FactoryStubMarker):
      value_resource_type = value.class_.__name__
      value_resource_factory = factory_for(value_resource_type)
      value_resource = value_resource_factory()
      value_response = post_example(
          context, value_resource_type, value_resource, context_id=context_id)
      # If not a successful creation, then it didn't create the object we need
      if value_response.status_code != 201:
        return value_response
      # Get the value of the first/only (key,value) pair
      #   (and just assume the root key is correct)
      value_data = value_response.json().items()[0][1]
      example[attr] = {
        'href': value_data["selfLink"],
        'id': value_data["id"],
        'type': value_resource_type
        }
  # Assign overriding `context_id`, if specified
  if context_id is not None:
    example["context_id"] = context_id

  headers = {'Content-Type': 'application/json',}
  data = json.dumps(
      {get_resource_table_singular(resource_type): example},
      cls=DateTimeEncoder,
      )
  response = requests.post(
      context.base_url+url,
      data=data,
      headers=headers,
      allow_redirects=False,
      cookies=getattr(context, 'cookies', {}),
      )
  if response.status_code == 302:
    # deal with login redirect, expect noop
    headers={'Accept': 'text/html',}
    if hasattr(context, 'current_user_json'):
      headers['X-ggrc-user'] = context.current_user_json
    response = requests.get(
        response.headers['Location'],
        headers=headers,
        allow_redirects=False,
        )
    context.cookies = response.cookies
    response = requests.post(
        context.base_url+url,
        data=data,
        headers={
          'Content-Type': 'application/json',
          },
        cookies=context.cookies,
        )
  context.cookies = response.cookies
  return response

class DateTimeEncoder(json.JSONEncoder):
  """Custom JSON Encoder to handle datetime objects

  from:
     `http://stackoverflow.com/questions/12122007/python-json-encoder-to-support-datetime`_
  also consider:
     `http://hg.tryton.org/2.4/trytond/file/ade5432ac476/trytond/protocols/jsonrpc.py#l53`_
  """
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.isoformat('T')
    elif isinstance(obj, datetime.date):
      return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
      return (datetime.datetime.min + obj).time().isoformat('T')
    else:
      return super(DateTimeEncoder, self).default(obj)

def get_resource_table_singular(resource_type):
  # This should match the implementation at
  #   ggrc.models.inflector:ModelInflector.underscore_from_camelcase
  import re
  s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', resource_type)
  return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def get_service_endpoint_url(context, endpoint_name):
  """Return the URL for the `endpoint_name`. This assumes that there is a
  `service_description` in the `context` to ues to lookup the endpoint url.
  """
  return context.service_description.get(u'service_description')\
      .get(u'endpoints').get(unicode(endpoint_name)).get(u'href')
