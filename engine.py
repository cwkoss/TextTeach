import logging

logging.getLogger().setLevel(logging.INFO)


class Engine:
    def __init__(self, lesson):
        self.lesson = lesson

    def process_message(self, state=0, message=""):
        logging.info("Called with state=%s and message='%s'", str(state), message)
        messages = []

        if self.lesson['msgChunks'][state]['type'] == "multi":
            if message in self.lesson['msgChunks'][state]['responses']:
                messages += self.lesson['msgChunks'][state]['responses'][message]['prompts']
                if message not in self.lesson['msgChunks'][state]["correctResponses"]:
                    return state, messages
                state += 1
            else:
                messages += ["Invalid response, try again."]
                return state, messages

        while state < len(self.lesson['msgChunks']):
            messages += self.lesson['msgChunks'][state]['prompts']
            if self.lesson['msgChunks'][state]['type'] == "multi":
                break
            state += 1
        else:
            messages.append("Lesson Complete!")

        return state, messages
