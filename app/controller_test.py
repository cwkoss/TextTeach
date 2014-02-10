#!/usr/bin/env python
# coding=utf-8

import unittest
# TODO: Move test data to commonly imported file from both tests.
import engine_test
from controller import Controller


class TestController(unittest.TestCase):
    def setUp(self):
        self.c = Controller()
        self.c.add_lesson('default', engine_test.simple_lesson)

    def test_new(self):
        self.assertIsNotNone(self.c)

    def test_add_lesson(self):
        self.assertEqual(len(self.c.lessons), 1)

    def test_message(self):
        self.c.on_message(sender="mike", message="")
        # Add some asserts
