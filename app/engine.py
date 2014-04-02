import logging
import random

logging.getLogger().setLevel(logging.INFO)


class Engine(object):
    def __init__(self, lesson):
        self.lesson = lesson
        self.state = 0

    def set_state(self, state=0):
        self.state = state

    def set_next_state(self):
        if self.state == -1:
            return
        self.state += 1
        if self.state >= self.get_num_states():
            self.set_lesson_complete()

    def is_lesson_complete(self):
        return self.state == -1

    def set_lesson_complete(self):
        self.state = -1

    def get_current_state(self):
        return self.lesson['msgChunks'][self.state]

    def get_current_type(self):
        return self.get_current_state()['type']

    def get_current_responses(self):
        return self.get_current_state()['responses']

    def get_correct_responses(self):
        return self.get_current_state()['correctResponses']

    def get_num_states(self):
        return len(self.lesson['msgChunks'])

    # Gets the top-level prompt from the current state.
    def get_current_state_prompts(self):
        return self.get_current_state()['prompts']

    def get_prompts_from_response(self, response):
        return self.get_current_responses()[response]['prompts']

    def advance_messages(self):
        messages = []
        while not self.is_lesson_complete():
            messages += self.get_current_state_prompts()
            if self.get_current_type() == "multi":
                break
            self.set_next_state()
        else:
            messages.append("Quiz Complete!")
        return messages

    @staticmethod
    def clean_input(s):
        return s.strip().lower()

    def help_command(self, words):
        """ This command returns help about commands. """
        return self.state, ["This is help."]

    def restart_command(self, words):
        """ Restart the current lesson. """
        self.set_state(0)
        return self.repeat_command([])

    def repeat_command(self, words):
        """ Repeat the last question. """
        return self.state, self.advance_messages()

    def process_message(self, state=0, message=""):
        messages = []

        message = self.clean_input(message)
        logging.info("Called with state=%s and message='%s'", str(state), message)
        self.set_state(state)

        words = message.split(' ')
        command_func_name = words[0] + '_command'
        if command_func_name in self.__class__.__dict__:
            fn = self.__class__.__dict__[command_func_name]
            if callable(fn):
                return fn(self, words[1:])

        if self.get_current_type() == "multi":
            # Just look at initial letter of response
            message = message[0].lower()
            responses = self.get_current_responses()

            if message not in responses:
                messages += ["Invalid response, try again."]
                return self.state, messages

            messages += self.get_prompts_from_response(message)
            if message not in self.get_correct_responses():
                return self.state, messages

            self.set_next_state()

        messages += self.advance_messages()

        return self.state, messages

    def process_message_dev(self, message, student):
        return_msgs = []
        keep_looping = True
        while keep_looping:
            if self.lesson['sections'][student.sectionIndex]["type"] == "instructional":
                return_msgs.append(self.lesson['sections'][student.sectionIndex]["body"])
                student.sectionIndex += 1
                logging.info("instructional")
            elif self.lesson['sections'][student.sectionIndex]["type"] == "add-question":
                student.questionHistory[self.lesson['sections'][student.sectionIndex]["id"]] = {"reviewcount": 0, "totalscore": 0, "history": []}
                logging.info(student.questionHistory[self.lesson['sections'][student.sectionIndex]["id"]])
                student.sectionIndex += 1
            elif self.lesson['sections'][student.sectionIndex]["type"] == "review":
                logging.info("Review" + str(student.currentQuestion) )

                if student.currentQuestion is None:  # Initialize New Question
                    next_q = self.get_lowest_score_q(student.questionHistory)
                    student.currentQuestion = self.build_question_from_qid(next_q)
                    return_msgs.append(student.currentQuestion['prompt'])
                    return_msgs.append("A. " + student.currentQuestion["options"][0] + "\nB. " + student.currentQuestion["options"][1] + "\nC. " + student.currentQuestion["options"][2] + "\nD. " + student.currentQuestion["options"][3] + "\nE. " + student.currentQuestion["options"][4])
                    logging.info("initalizing question: " + next_q)
                    logging.info(student.currentQuestion['prompt'])
                    break
                else:
                    #Complete Question if answer is correct
                    mult_options = ["a", "b", "c", "d", "e"]
                    if ["a", "b", "c", "d", "e"].count(message[0].lower()) > 0:
                        if student.currentQuestion["correctIndex"] == mult_options.index(message[0].lower()):
                            curr_id = student.currentQuestion["id"]
                            student.questionHistory[curr_id]["reviewcount"] += 1

                            mult_scores = [100,50,25,10]
                            curr_score = mult_scores[min(3, student.currentQuestion["attempts"])]
                            student.questionHistory[curr_id]["totalscore"] += curr_score
                            return_msgs.append("Correct!")
                            return_msgs.append("You earned " + str(curr_score) + " points!")
                            student.currentQuestion = None
                            if not self.below_threshold_scores_remain(student.questionHistory, self.lesson['sections'][student.sectionIndex]["threshold"]):
                                student.sectionIndex += 1
  
                        else:
                            return_msgs.append("Wrong, try again!")
                            student.currentQuestion["attempts"] += 1
                            break
                    else:
                        return_msgs.append("Message not understood")
                        break
                   
    

            if student.sectionIndex >= len(self.lesson['sections']):
                break
        student.put()
        #return [self.lesson['sections'][0]["body"]]
        return return_msgs

    def get_lowest_score_q(self, questionHistory):
        lowest_score = -1
        lowest_qs = []
        for qid in questionHistory:
            if lowest_score == -1:
                lowest_score = questionHistory[qid]['totalscore']
                lowest_qs.append(qid)
            elif lowest_score > questionHistory[qid]['totalscore']:
                lowest_score = questionHistory[qid]['totalscore']
                lowest_qs = [qid]
            elif lowest_score == questionHistory[qid]['totalscore']:
                lowest_qs.append(qid)
        # TODO add random selection of lowest qs
        logging.info(lowest_qs[0])
        return lowest_qs[0]

    def below_threshold_scores_remain(self, questionHistory, threshold):
        for qid in questionHistory:
            if questionHistory[qid]['totalscore'] < threshold:
                return True
        return False

    def build_question_from_qid(self, qid):
        sect = -1
        for section in self.lesson['sections']:
            if section['type'] == "add-question":
                if section['id'] == qid:
                    sect = section
                    break
        options = [sect['correct-answer'], sect['distractors'][0], sect['distractors'][1], sect['distractors'][2], sect['distractors'][3]]
        logging.info(options)        
        random.shuffle(options) 
        logging.info(options)  
        correct_index = -1
        for i in xrange(len(options)):
            if options[i] == sect['correct-answer']:
                correct_index = i
        logging.info("length of options is " + str(len(options)))
        return {"id": qid, "prompt": sect['prompt'], "options": options, "correctIndex": correct_index, "attempts": 0}

