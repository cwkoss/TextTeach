#!/usr/bin/env python
import logging

from google.appengine.ext import ndb

from engine import Engine


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
        session.put()
        self.reply_with(sender, messages)

    def reply_with(self, sender, messages):
        for message in messages:
            logging.info("Reply with: %s", message)


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
