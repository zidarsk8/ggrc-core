# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for collection post service."""

import json

from integration.ggrc import services


class TestCollectionPost(services.TestCase):

  def get_location(self, response):
    """Ignore the `http://localhost` prefix of the Location"""
    return response.headers['Location'][16:]

  def headers(self, *args, **kwargs):
    ret = list(args)
    ret.append(('X-Requested-By', 'Unit Tests'))
    ret.extend(kwargs.items())
    return ret

  def test_collection_post_successful(self):
    data = json.dumps(
        {'services_test_mock_model': {'foo': 'bar', 'context': None}})
    self.client.get("/login")
    response = self.client.post(
        self.mock_url(),
        content_type='application/json',
        data=data,
        headers=self.headers(),
    )
    self.assertStatus(response, 201)
    self.assertIn('Location', response.headers)
    response = self.client.get(
        self.get_location(response), headers=self.headers())
    self.assert200(response)
    self.assertIn('Content-Type', response.headers)
    self.assertEqual('application/json', response.headers['Content-Type'])
    self.assertIn('services_test_mock_model', response.json)
    self.assertIn('foo', response.json['services_test_mock_model'])
    self.assertEqual('bar', response.json['services_test_mock_model']['foo'])
    # check the collection, too
    response = self.client.get(self.mock_url(), headers=self.headers())
    self.assert200(response)
    self.assertEqual(
        1, len(response.json['test_model_collection']['test_model']))
    self.assertEqual(
        'bar', response.json['test_model_collection']['test_model'][0]['foo'])

  def test_collection_post_successful_single_array(self):
    data = json.dumps(
        [{'services_test_mock_model': {'foo': 'bar', 'context': None}}])
    self.client.get("/login")
    response = self.client.post(
        self.mock_url(),
        content_type='application/json',
        data=data,
        headers=self.headers(),
    )
    self.assert200(response)
    self.assertEqual(type(response.json), list)
    self.assertEqual(len(response.json), 1)

    response = self.client.get(self.mock_url(), headers=self.headers())
    self.assert200(response)
    self.assertEqual(
        1, len(response.json['test_model_collection']['test_model']))
    self.assertEqual(
        'bar', response.json['test_model_collection']['test_model'][0]['foo'])

  def test_collection_post_successful_multiple(self):
    data = json.dumps([
        {'services_test_mock_model': {'foo': 'bar1', 'context': None}},
        {'services_test_mock_model': {'foo': 'bar2', 'context': None}},
    ])
    self.client.get("/login")
    response = self.client.post(
        self.mock_url(),
        content_type='application/json',
        data=data,
        headers=self.headers(),
    )
    self.assert200(response)
    self.assertEqual(type(response.json), list)
    self.assertEqual(len(response.json), 2)
    self.assertEqual(
        'bar1', response.json[0][1]['services_test_mock_model']['foo'])
    self.assertEqual(
        'bar2', response.json[1][1]['services_test_mock_model']['foo'])
    response = self.client.get(self.mock_url(), headers=self.headers())
    self.assert200(response)
    self.assertEqual(
        2, len(response.json['test_model_collection']['test_model']))

  def test_collection_post_successful_multiple_with_errors(self):
    data = json.dumps([
        {'services_test_mock_model':
         {'foo': 'bar1', 'code': 'f1', 'context': None}},
        {'services_test_mock_model':
            {'foo': 'bar1', 'code': 'f1', 'context': None}},
        {'services_test_mock_model':
            {'foo': 'bar2', 'code': 'f2', 'context': None}},
        {'services_test_mock_model':
            {'foo': 'bar2', 'code': 'f2', 'context': None}},
    ])
    self.client.get("/login")
    response = self.client.post(
        self.mock_url(),
        content_type='application/json',
        data=data,
        headers=self.headers(),
    )

    self.assertEqual(403, response.status_code)
    self.assertEqual([201, 403, 201, 403], [i[0] for i in response.json])
    self.assertEqual(
        'bar1', response.json[0][1]['services_test_mock_model']['foo'])
    self.assertEqual(
        'bar2', response.json[2][1]['services_test_mock_model']['foo'])
    response = self.client.get(self.mock_url(), headers=self.headers())
    self.assert200(response)
    self.assertEqual(
        2, len(response.json['test_model_collection']['test_model']))

  def test_collection_post_bad_request(self):
    response = self.client.post(
        self.mock_url(),
        content_type='application/json',
        data='This is most definitely not valid content.',
        headers=self.headers(),
    )
    self.assert400(response)

  def test_collection_post_bad_content_type(self):
    response = self.client.post(
        self.mock_url(),
        content_type='text/plain',
        data="Doesn't matter, now does it?",
        headers=self.headers(),
    )
    self.assertStatus(response, 415)
