#!/usr/bin/env python
import logging

from google.appengine.ext import ndb

from twilio.rest import TwilioRestClient

from engine import Engine

ACCOUNT_SID = "AC94743d49300d49a696cf09bfef229c82"
AUTH_TOKEN = "459bb4d749bdff002e45d44d33a4ad7f"
FROM_PHONE = "+12067454564"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


def main():
    c = Controller()
    c.run_loop()


class Controller(object):
    def __init__(self):
        self.lessons = {}

    def run_loop(self):
        print "Loop called"

    def add_lesson(self, lesson_id, lesson):
        self.lessons[lesson_id] = lesson

    def on_message(self, sender=None, message=None):
        if sender is None or message is None:
            raise Error("Invalid sender or message.")
        student = Student.ensure_student(phone=sender)
        session = Session.ensure_session(student.get_id())
        lesson = self.lessons.get(session.lesson_id)
        if lesson is None:
            raise Error("No such lesson: %s" % session.lesson_id)
        eng = Engine(lesson)
        session.state, messages = eng.process_message(session.state, message)
        if session.state == -1:
            session.key.delete()
        else:
            session.put()
        self.send_SMS_replies(sender, messages)

    def send_SMS_replies(self, recipient, messages):
        joined_message = "\n".join(messages)
        self.send_to_twilio(recipient, joined_message)

    @staticmethod
    def send_to_twilio(recipient, message):
        # There is a bug in SMS stack that corrupts 161 character messages!
        if len(message) == 161:
            message += "."
        logging.info("Sending: %s", message)
        client.messages.create(to=recipient, from_=FROM_PHONE, body=message)


class Student(ndb.Model):
    phone = ndb.StringProperty()

    @classmethod
    def ensure_student(cls, phone=None):
        if phone is None:
            raise Error("Missing phone.")
        student = Student.query(Student.phone == phone).get()
        if student is None:
            student = Student(phone=phone)
            student.put()
        return student

    def get_id(self):
        return self.key.id()


class Session(ndb.Model):
    student_id = ndb.IntegerProperty()
    lesson_id = ndb.StringProperty()
    state = ndb.IntegerProperty(default=0)

    @classmethod
    def ensure_session(cls, student_id=None):
        if student_id is None:
            raise Error("Missing student id.")
        session = Session.query(Session.student_id == student_id).get()
        if session is None:
            session = Session(student_id=student_id, lesson_id="default")
            session.put()
        return session


if __name__ == "__main__":
    main()
