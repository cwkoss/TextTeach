import webapp2
import json

from google.appengine.api import memcache


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write("Hello, student.\n")
        self.response.write(memcache.get(key='data'))


class ReceiveSMS(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        message = json.dumps(dict(self.request.params))
        memcache.set(key="data", value=message)


application =webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sms', ReceiveSMS)
], debug=True)
