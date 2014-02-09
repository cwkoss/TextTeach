import webapp2
from google.appengine.api import memcache


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write("Hello, student.")
        self.response.write(memcache.get(key='body'))


class ReceiveSMS(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        message = self.request.get('Body')
        memcache.set(key="body", value=message)


application =webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sms', ReceiveSMS)
], debug=True)
