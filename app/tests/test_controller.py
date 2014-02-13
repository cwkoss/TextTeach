#!/usr/bin/env python
# coding=utf-8
import unittest
from mock import Mock, patch, call

from google.appengine.ext import testbed

# TODO: Move test data to commonly imported file from both tests.
import engine_test

import controller


class TestController(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.c = controller.Controller()
        self.c.add_lesson('default', engine_test.simple_lesson)

    def test_new(self):
        self.assertIsNotNone(self.c)

    def test_add_lesson(self):
        self.assertEqual(len(self.c.lessons), 1)

    def test_message(self):
        test_number = '4255551212'
        with patch('controller.client') as client:
            self.c.on_message(sender=test_number, message="start")
            self.assertEqual(client.mock_calls,
                             [call.messages.create(body='First prompt',
                                                   to=test_number,
                                                   from_='+12067454564'),
                              call.messages.create(body='The first question.',
                                                   to=test_number,
                                                   from_='+12067454564')])
