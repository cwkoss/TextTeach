#!/usr/bin/env python


def main():
    c = Controller()
    c.run_loop()


class Controller(object):
    def __init__(self):
        self.lessons = []

    def run_loop(self):
        print "Loop called"

    def add_lesson(self, lesson):
        self.lessons.append(lesson)


if __name__ == "__main__":
    main()
