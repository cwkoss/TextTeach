#!/usr/bin/env python
# coding=utf-8

import unittest
import engine_test
from controller import Controller


class TestController(unittest.TestCase):
    def test_new(self):
        c = Controller()
        self.assertIsNotNone(c)

    def test_add_lesson(self):
        c = Controller()
        c.add_lesson(engine_test.simple_lesson)
