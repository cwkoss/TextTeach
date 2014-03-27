import logging

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
        student.questionHistory = {"foo":"bar"}
        student.put()
        return [self.lesson['sections'][0]["body"]]
