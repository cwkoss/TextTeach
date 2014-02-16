#!/usr/bin/env python
import logging
from time import sleep
from datetime import datetime

logging.getLogger().setLevel(logging.INFO)

from twilio.rest import TwilioRestClient

ACCOUNT_SID = "AC94743d49300d49a696cf09bfef229c82"
AUTH_TOKEN = "459bb4d749bdff002e45d44d33a4ad7f"
FROM_PHONE = "+12067454564"
MESSAGE_DELAY = 6
LINE_LENGTH = 35

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)


def main(run_name=""):
    test_concat(run_name)


def test_concat(run_name):
    MESSAGE_LEN = 500
    message = "%s: This message has %d characters." % (run_name, MESSAGE_LEN)
    line_number = 1
    while len(message) < MESSAGE_LEN:
        line_size = min(MESSAGE_LEN - len(message), LINE_LENGTH)
        if line_size < 5:
            message += "\n" + "-" * (line_size - 1)
        else:
            message += "\n%02d. %s" % (line_number, "x" * (line_size - 5))
        line_number += 1
    send_to_twilio(message)


def test_separate(run_name):
    run_name += " (%ds delay)" % (MESSAGE_DELAY, )
    for i in xrange(10):
        message = "%s: This is message number %d." % (run_name, i)
        if i != 0:
            sleep(MESSAGE_DELAY)
        send_to_twilio(message)


def send_to_twilio(message):
    if len(message) == 161:
        logging.info("Adjusting message at boundary.")
        message += '.'
    logging.info("Sending '%s'.", message)
    client.messages.create(to="4252467703", from_=FROM_PHONE, body=message)


if __name__ == '__main__':
    run_name = "%s" % (datetime.now().strftime("%H:%M:%S"),)
    main(run_name)
