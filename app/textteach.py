import webapp2
import json
import logging

from google.appengine.api import memcache

from controller import Controller


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write("Hello, student.\n")
        # self.response.write(memcache.get(key='data'))


class ReceiveSMS(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        message = json.dumps(dict(self.request.params))
        logging.info("Twillio Data: %s", message)
        # memcache.set(key="data", value=message)

        c = Controller()
        import engine_test
        c.add_lesson('default', engine_test.simple_lesson)
        c.on_message(self.request.get('From'), self.request.get('Body'))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sms', ReceiveSMS)
], debug=True)
