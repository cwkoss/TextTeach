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

    @staticmethod
    def clean_input(s):
        return s.strip().lower()

    def process_message(self, state=0, message=""):
        messages = []

        message = self.clean_input(message)
        logging.info("Called with state=%s and message='%s'", str(state), message)
        self.set_state(state)

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

        while not self.is_lesson_complete():
            messages += self.get_current_state_prompts()
            if self.get_current_type() == "multi":
                break
            self.set_next_state()
        else:
            messages.append("Lesson Complete!")

        return self.state, messages
