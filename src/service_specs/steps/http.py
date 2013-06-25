# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import datetime
from behave import given, when, then
from iso8601 import parse_date

from .utils import \
    Example, handle_example_resource, handle_named_example_resource, \
    set_property, get_resource, put_resource, get_resource_table_singular, \
    get_service_endpoint_url, handle_get_resource_and_name_it, \
    handle_post_named_example_to_collection_endpoint, \
    handle_post_named_example, post_example, handle_get_example_resource

def get_json_response(context):
  if not hasattr(context, 'json'):
    context.json = context.response.json()
  return context.json

@given('an example "{resource_type}"')
def example_resource(context, resource_type):
  handle_example_resource(context, resource_type)

@given('a new "{resource_type}" named "{name}"')
def named_example_resource(context, resource_type, name, **kwargs):
  handle_named_example_resource(context, resource_type, name, **kwargs)

@given('"{name}" is POSTed to its collection')
def post_named_example_to_collection_endpoint(
    context, name, expected_status=201):
  handle_post_named_example_to_collection_endpoint(
      context, name, expected_status)

@given('HTTP POST of "{name}" to "{url}"')
def simple_post_of_named(context, name, url):
  example = getattr(context, name)
  response = post_example(
      context, example.resource_type, example.value, url)
  assert response.status_code == 200, \
      'Expected status code {0}, received {1}'.format(
          200, response.status_code)
  context.response = response

@given('"{name}" is POSTed to "{url}"')
def post_named_example(context, name, url, expected_status=201):
  handle_post_named_example(context, name, url, expected_status)

@when('the example "{resource_type}" is POSTed to its collection')
def post_example_resource_to_its_collection(context, resource_type):
  endpoint_url = get_service_endpoint_url(context, resource_type)
  post_example_resource(context, resource_type, endpoint_url)

@when('the example "{resource_type}" is POSTed to the "{collection}"')
def post_example_resource(context, resource_type, collection):
  context.response = post_example(
      context, resource_type, context.example_resource, collection)

@when('GET of "{url}" as "{name}"')
def get_resource_and_name_it(context, url, name):
  handle_get_resource_and_name_it(context, url, name)

@when('GET of the resource "{name}"')
def get_example_resource(context, name, expected_status=200):
  handle_get_example_resource(context, name, expected_status)

@then('a "{status_code}" status code is received')
def validate_status_code(context, status_code):
  assert context.response.status_code == int(status_code), \
      'Expected status code {0}, received {1}'.format(
          status_code, context.response.status_code)

@then('a 201 status code is received')
def validate_status_201(context):
  assert context.response.status_code == 201, \
      'Expected status code 201, received {0}'.format(
          context.response.status_code)

@then('the response has a Location header')
def validate_location_header(context):
  assert 'Location' in context.response.headers

@then('we receive a valid "{resource_type}" in the entity body')
def validate_resource_in_response(context, resource_type):
  assert 'application/json' == context.response.headers['Content-Type']
  assert get_resource_table_singular(resource_type) in get_json_response(context)
  #FIXME more more more

def dates_within_tolerance(original, response):
  floor = datetime.datetime(
      original.year, original.month, original.day, original.hour,
      original.minute, original.second, tzinfo=original.tzinfo)
  ceiling = floor + datetime.timedelta(seconds=1)
  return floor <= response <= ceiling

@then('the received "{resource_type}" matches the one we posted')
def check_resource_equality_for_response(context, resource_type):
  root = unicode(get_resource_table_singular(resource_type))
  resp_json = get_json_response(context)[root]
  orig_json = context.example_resource
  for k in orig_json:
    original = context.example_resource[k]
    response = resp_json[unicode(k)]
    if isinstance(original, datetime.datetime):
      response = parse_date(response)
      assert dates_within_tolerance(original, response), \
          'for {0}: expected {1}, received {2}'.format(
              k, original, response)
      return
    elif isinstance(original, datetime.date):
      response = datetime.datetime.strptime(response, '%Y-%m-%d').date()
    assert original == response, 'for {0}: expected {1}, received {2}'.format(
        k, original, response)

@given('current user is "{user_json}"')
def define_current_user(context, user_json):
  import requests
  if hasattr(context, 'current_user_json'):
    # logout current user
    response = requests.get(
        context.base_url+'/logout',
        headers={'Accept': 'text/html'},
        cookies=getattr(context, 'cookies', {})
        )
    assert response.status_code == 200, 'Failed to logout!!'
    delattr(context, 'cookies')
  context.current_user_json = user_json.replace('\\"', '"')

@then('POST of "{resource_name}" to its collection is allowed')
def check_POST_is_allowed(context, resource_name):
  post_named_example_to_collection_endpoint(context, resource_name)

@then('POST of "{resource_name}" to its collection is forbidden')
def check_POST_is_forbidden(context, resource_name):
  post_named_example_to_collection_endpoint(
      context, resource_name, expected_status=403)

@then('GET of "{resource_name}" is allowed')
def check_GET_is_allowed(context, resource_name):
  get_example_resource(context, resource_name)

@then('GET of "{resource_name}" is forbidden')
def check_GET_is_forbidden(context, resource_name):
  get_example_resource(context, resource_name, expected_status=403)

def put_example_resource(context, name, expected_status=200):
  example = getattr(context, name)
  url = example.get('selfLink')
  response = put_resource(context, url, example)
  assert response.status_code == expected_status
  if expected_status == 200 or expected_status == 201:
    example = Example(example.resource_type, response.json())
    setattr(context, name, example)

@then('PUT of "{resource_name}" is allowed')
def check_PUT_is_allowed(context, resource_name):
  put_example_resource(context, resource_name)

@then('PUT of "{resource_name}" is forbidden')
def check_PUT_is_forbidden(context, resource_name):
  put_example_resource(context, resource_name, expected_status=403)

def delete_resource(context, url, resource):
  import requests
  headers={
      'Content-Type': 'application/json',
      'If-Match': resource.response.headers['Etag'],
      'If-Unmodified-Since': resource.response.headers['Last-Modified'],
      }
  if hasattr(context, 'current_user_json'):
    headers['X-ggrc-user'] = context.current_user_json
  response = requests.delete(
      context.base_url+url,
      headers=headers,
      cookies=getattr(context, 'cookies', {})
      )
  context.cookies = response.cookies
  return response

def delete_example_resource(context, name, expected_status=200):
  example = getattr(context, name)
  url = example.get('selfLink')
  response = delete_resource(context, url, example)
  assert response.status_code == expected_status

@then('DELETE of "{resource_name}" is allowed')
def check_DELETE_is_allowed(context, resource_name):
  delete_example_resource(context, resource_name, expected_status=200)

@then('DELETE of "{resource_name}" is forbidden')
def check_DELETE_is_allowed(context, resource_name):
  delete_example_resource(context, resource_name, expected_status=403)
