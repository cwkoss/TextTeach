#!/usr/bin/env python
# coding=utf-8

import unittest
from controller import Controller


class TestController(unittest.TestCase):
    def test_new(self):
        c = Controller()
        self.assertIsNotNone(c)
