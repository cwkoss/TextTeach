import json
import logging

import webapp2

from google.appengine.api import memcache

from controller import Controller


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write("Hello, student.<input type='button' value='hi'>\n")
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

        json_data = open('lesson.json')
        data = json.load(json_data)
        json_data.close()

        c.add_lesson('default', data)
        c.on_message(self.request.get('From'), self.request.get('Body'))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sms', ReceiveSMS)
], debug=True)
