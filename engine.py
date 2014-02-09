import logging

logging.getLogger().setLevel(logging.INFO)

class Engine:
	def __init__(self, lesson):
		self.lesson = lesson

	def process_message(self, state=0, message=""):
		logging.info("Called with state=%s and message='%s'", str(state), message)
		messages = self.lesson['msgChunks'][state]['prompts']
		return state + 1, messages