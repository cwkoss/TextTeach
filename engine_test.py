#!/usr/bin/env python
# coding=utf-8

import unittest
from engine import Engine

simple_lesson = {
    "msgChunks": [
        {
            "type": "section",
            "prompts": ["First prompt"]
        },
        {
            "type": "multi",
            "prompts": ["The first question."],
            "correctResponses": ["a"],
            "responses": {
                "a": {"prompts": ["That is correct."]},
                "b": {"prompts": ["Wrong!"]},
            }
        },
        {
            "type": "multi",
            "prompts": ["The second question."],
            "correctResponses": ["a"],
            "responses": {
                "a": {"prompts": ["That is correct."]},
                "b": {"prompts": ["Wrong!"]},
            }
        },
    ]
}


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.x = Engine(simple_lesson)

    def test_new(self):
        self.assertIsNotNone(self.x)

    def test_process_first(self):
        new_state, messages = self.x.process_message()
        self.assertEqual(new_state, 1)
        self.assertEqual(messages, ["First prompt", "The first question."])

    def test_process_correct_answer(self):
        new_state, messages = self.x.process_message(1, "a")
        self.assertEqual(new_state, 2)
        self.assertEqual(messages, ["That is correct.", "The second question."])

    def test_process_incorrect_answer(self):
        new_state, messages = self.x.process_message(2, "b")
        self.assertEqual(new_state, 2)
        self.assertEqual(messages, ["Wrong!"])

    def test_process_last_correct_answer(self):
        new_state, messages = self.x.process_message(2, "a")
        self.assertEqual(new_state, 3)
        self.assertEqual(messages, ["That is correct.", "Lesson Complete!"])
