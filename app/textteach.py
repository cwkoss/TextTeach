import json
import logging

import webapp2
import time

from google.appengine.api import memcache
from google.appengine.ext import ndb

from controller import Controller
from controller import Student

studentAttrDict = {"multiAttempts": "Multiple Choice Questions Attempted",
                   "multiCorrectFirst": "MultiChoice Correct First Try",
                   "totalMsgReceived": "Total Messages Received",
                   "totalMsgSent": "Total Messages Sent",
                   "totalSMSSent": "Total SMS Msgs Sent"}


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # self.response.write("Hello, student.")
        tempstr = "<html><head>"
        tempstr += "<style>td { padding: 5px; border: 1px solid black;}</style>"
        tempstr += "</head><body>"
        tempstr += "<h1>Text Teach Admin Dashboard</h1><br><br>"
        tempstr += "<table style='width:100%; padding: 15px;'><b><tr>"
        tempstr += "<td>Phone Number</td><td>Creation Time</td>"
        # tempstr += "<td>MultChoice Attempts</td><td>MultChoice Correct First Try</td>"
        tempstr += "<td>Total Msg Received</td><td>"
        tempstr += "Total Msgs Sent</td><td>Total SMS Msgs Sent</td></tr></b>"
        #logging.info(Student.ensure_student('+14252467703').totalSMSSent)
        for student in Student.query().iter():
            tempstr += "<tr>"
            #logging.info(student.phone)
            tempstr += "<td>" + student.phone + "</td>>"
            tempstr += "<td>" + str(time.ctime(student.createdDateTime)) + "</td>>"
            # tempstr += "<td>" + str(student.multiAttempts) + "</td>>"
            # tempstr += "<td>" + str(student.multiCorrectFirst) + "</td>>"
            tempstr += "<td>" + str(student.totalMsgReceived) + "</td>>"
            tempstr += "<td>" + str(student.totalMsgSent) + "</td>>"
            tempstr += "<td>" + str(student.totalSMSSent) + "</td>>"
            """
            if getattr(student, "createdDateTime") is None:
                tempstr += "<td>N/A</td>"
                student.createdDateTime = 1393977600
                student.put()
            else:
                tempstr += "<td>" + time.ctime(student.createdDateTime) + "</td>"
            #tempstr += "Phone Number: " + getattr(student, 'phone') + "<br>"
            for key in studentAttrDict:
                if getattr(student, key) is None:
                    tempstr += "<td>N/A</td>"
                    setattr(student, key, 0)
                    student.put()
                else:
                    tempstr += "<td>" + str(getattr(student, key)) + "</td>"
            """

            tempstr += "</tr>"
        tempstr += "</table></body></html>"
        self.response.write(tempstr)
        # self.response.write(memcache.get(key='data'))


class ReceiveSMS(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        message = json.dumps(dict(self.request.params))
        logging.info("Twillio Data: %s", message)
        # memcache.set(key="data", value=message)

        c = Controller()
        #import engine_test

        json_data = open('lesson.json')
        data = json.load(json_data)
        json_data.close()

        c.add_lesson('default', data)
        c.on_message(self.request.get('From'), self.request.get('Body'))


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sms', ReceiveSMS)
], debug=True)
