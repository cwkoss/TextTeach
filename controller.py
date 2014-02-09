#!/usr/bin/env python


def main():
    c = Controller()
    c.run_loop()


class Controller(object):
    def run_loop(self):
        print "Loop called"


if __name__ == "__main__":
    main()
