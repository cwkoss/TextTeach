#!/usr/bin/env python
# coding=utf-8

import unittest
from engine import Engine

simple_lesson = {
    "msgChunks": [
        {"type": "section",
         "prompts": ["First prompt"]
     },
                {"type": "multi",
                 "prompts": ["The first question."],
                 "correctResponses": ["a"],
                 "responses": {
                     "a": {"prompts": ["That is correct."]},
                     "b": {"prompts": ["Wrong!"]},
                 }
                },
        ]
}

sample_lesson = {
    "name":"",
    "course":"",
    "lessonnum":1,
    "msgChunks": [
        {"type":"sectmsg",
         "prompts":["This your daily 5-question SAT vocabulary quiz. Text H for a hint at any time."]},
        {"type":"multi",
         "prompts":["1. After observing several vicious territorial fights, Jane Goodall had to revise her earlier opinion that these particular primates were always ------ animals.",
                    "A. ignorant\nB. inquisitive\nC. responsive\nD. peaceful\nE. cruel"],
         "responses":{"a": {"correct":False, "prompts":["Incorrect. If Jane originally thought the apes were “ignorant”, then watching them fight wouldn’t change her opinion. Pick again."]},
                      "b": {"correct":False, "prompts":["Incorrect. If Jane originally thought the apes were “inquisitive”, then watching them fight wouldn’t change her opinion. Pick again."]},
                      "c": {"correct":False, "prompts":["Incorrect. If Jane originally thought the apes were “responsive”, then watching them fight wouldn’t change her opinion. Pick again."]},
                      "d": {"correct":True, "prompts":["Correct. Jane originally thought the primates were always peaceful. After seeing them fight, she changed her opinion."]},
                      "e": {"correct":False, "prompts":["Incorrect. If Jane originally thought the apes were “cruel”, then watching them fight wouldn’t change her opinion. Pick again."]},
                      "h": {"correct":False, "prompts":["Jane had to revise her opinion of the apes after she saw them fight. The correct answer will describe what she originally thought of them."]}
                  }
          },
          {"type":"multi",
           "prompts":["2. There is no doubt that Larry is a genuine ------- : he excels at telling stories that fascinate his listeners.",
                      "A. braggart\nB. dilettante\nC. pilferer\nD. prevaricator\nE. raconteur"],
           "responses":{"a": {"correct":False, "prompts":["Incorrect. While a “braggart” may tell stories, someone who brags isn’t likely to fascinate his listeners. Pick again."]},
                        "b": {"correct":False, "prompts":["Incorrect. A “dilettante” is someone who dabbles in various activties, so it isn’t likely that he “excels” at storytelling. Pick again."]},
                        "c": {"correct":False, "prompts":[" Incorrect. A “pilferer” is a thief, not a storyteller. Pick again."]},
                        "d": {"correct":False, "prompts":["Incorrect. A “prevaricator” is someone who evades the truth. They may tell stories, but their goal is to deceive, not fascinate. Pick again."]},
                        "e": {"correct":True, "prompts":["Correct. A “raconteur” is someone who is good at telling fascinating stories."]},
                        "h": {"correct":False, "prompts":["The correct answer will mean someone who is good at telling fascinating stories. "]}
                    }
          },
          {"type":"multi",
           "prompts":["3. A discerning publishing agent can ------- promising material from a mass of submissions, separating the good from the bad.",
                      "A. supplant\nB. winnow\nC. finagle\nD. dramatize\nE. overhaul"],
           "responses":{"a": {"correct":False, "prompts":["Incorrect. “Supplant” means to replace. That’s not related to “separating the good from the bad”. Pick again."]},
                        "b": {"correct":True, "prompts":["Correct. To “winnow” promising material from the mass of submissions is to separate the good from the bad."]},
                        "c": {"correct":False, "prompts":["Incorrect. “Finagle” means to bargain or strike a deal. That’s not related to “separating the good from the bad”. Pick again."]},
                        "d": {"correct":False, "prompts":["Incorrect. “Dramatize” means to make something into a drama. That’s not related to “separating the good from the bad”. Pick again."]},
                        "e": {"correct":False, "prompts":["Incorrect. “Overhaul” is to re-do or rebuild. That’s not related to “separating the good from the bad”. Pick again."]},
                        "h": {"correct":False, "prompts":["The correct answer will mean the same thing as “separating the good from the bad”."]}
                    }
          },
          {"type":"multi",
           "prompts":["4. Although some think the terms \"bug\" and \"insect\" are ------- , the former term actually refers to ------- group of insects.",
                      "A. parallel . . an identical\nB. precise . . an exact\nC. interchangeable . . a particular\nD. exclusive . . a separate\nE. useful . . a useless"],
           "responses":{"a": {"correct":False, "prompts":["Incorrect. The word “although” sets up a contrast between what people think “bug” means and what it really means. Pick again."]},
                        "b": {"correct":False, "prompts":["Incorrect. The word “although” sets up a contrast between what people think “bug” means and what it really means. Pick again."]},
                        "c": {"correct":True, "prompts":["Correct. Although the two terms are considered “interchangeable”, in fact the term “bug” refers to “a particular” group of insects."]},
                        "d": {"correct":False, "prompts":["Incorrect. The word “although” sets up a contrast between what people think “bug” means and what it really means. Pick again."]},
                        "e": {"correct":False, "prompts":["Incorrect. The word “although” sets up a contrast between what people think “bug” means and what it really means. Pick again."]},
                        "h": {"correct":False, "prompts":["The word “although” sets up a contrast, so the correct answer will logically complete the idea of the sentence."]}
                    }
          },
          {"type":"multi",
           "prompts":["5. The novel's protagonist, a pearl diver, naïvely expects that the buyers will compete among themselves to pay him the best price for his pearl, but instead they ------- to ------- him.",
                      "A. collude . . swindle\nB. pretend . . praise\nC. conspire . . reimburse\nD. refuse . . cheat\nE. venture . . reward"],
           "responses":{"a": {"correct":True, "prompts":["Correct. In contrast to the pearl diver’s naive belief that the buyers will pay a fair price, they do otherwise. They “collude” to “swindle” him."]},
                        "b": {"correct":False, "prompts":["Incorrect. The pearl diver’s naive belief that the buyers will pay a fair price is in contrast to what the buyers will really do. Pick again."]},
                        "c": {"correct":False, "prompts":["Incorrect. The pearl diver’s naive belief that the buyers will pay a fair price is in contrast to what the buyers will really do. Pick again."]},
                        "d": {"correct":False, "prompts":["Incorrect. The pearl diver’s naive belief that the buyers will pay a fair price is in contrast to what the buyers will really do. Pick again."]},
                        "e": {"correct":False, "prompts":["Incorrect. The pearl diver’s naive belief that the buyers will pay a fair price is in contrast to what the buyers will really do. Pick again."]},
                        "h": {"correct":False, "prompts":["The pearl diver believes one thing is going to happen, but the buyers do something different. "]}
                    }
          }
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
            self.assertEqual(new_state, 1)
            self.assertEqual(messages, ["First prompt", "The first question."])
