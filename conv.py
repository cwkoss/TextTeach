import json
from pprint import pprint
json_data = open('lesson.json')
data = json.load(json_data)
json_data.close()

SLEEPTIME = 0 #how long to wait between waitMsg requests in secs

# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import TwilioRestClient
import time

# Your Account Sid and Auth Token from twilio.com/user/account
ACCOUNT_SID = "AC94743d49300d49a696cf09bfef229c82"
AUTH_TOKEN  = "459bb4d749bdff002e45d44d33a4ad7f"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 


# chris - "4252467703"
# james - "2068490631"
PHONENUM = "2068490631"
msgCount = 0

def waitForNewMessage():
    print "Waiting for new message"
    messages = getMessages()
    msgCount = messages.count()
    while True:
        messages = getMessages()
        if isNewMsg(msgCount, messages):
            print "Message found",
            print messages.list()[0].body
            return messages.list()[0].body
        time.sleep(SLEEPTIME)

def confirmMessageSent(body):
    messages = getMessages()
    while messages.list()[0].body != body:
        print "last message not new: " + messages.list()[0].body + "| should be " + body
        #time.sleep(1);
        messages = getMessages()
    print "Confirmed body: " + messages.list()[0].body
    return True



def getMessages():
   
    # A list of message objects with the properties described above
    #try:
    print "Requesting messages"
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    request = client.messages
    #except:
     #   print "Unexpected error", sys.exc_info()[0]
    #result = cl
    return request


def isNewMsg(msgCount, messages):
    if messages.count() > msgCount:
        #print "msgCount ", 
        #print msgCount
        #print "messages.count() ",
        #print messages.count()
        #print "messages.list()[1].body ",
        #print messages.list()[1].body
        return True
    else:
        #print "No new messages"
        return False

def sendMessage(body):
    print "sending message: ",
    print body
    time.sleep(1)    
    client.messages.create(
	    to=PHONENUM, 
	    from_="+12067454564",
        body=body   
    )
    confirmMessageSent(body)

def runLesson():
    #sendMessage("Welcome to " + data['course'])
#
 #   sendMessage("Text L for a lesson or S for settings")
  #  x = waitForNewMessage()
   # while(x.lower() != "l"):
    #    sendMessage("Settings have not been implemented, just text L to continue")
     #   x = waitForNewMessage()

    for msgChunk in data['msgChunks']:
        for prompt in msgChunk['prompts']:
            sendMessage(prompt)
        if msgChunk['type'] == 'info':
            x = ""
            while(x.lower() != "c"):
                sendMessage("Text C to continue.")
                x = waitForNewMessage()
        elif msgChunk['type'] == 'multi':
            x = ""
            correct = ""
            for response in msgChunk['responses']:            
                if msgChunk['responses'][response]['correct']:
                    correct = response
            x = waitForNewMessage().lower()
            while(x != correct):
                if(x == "a" or x == "b" or x == "c" or x == "d" or x == "e" or x == "h"):
                    sendMessage(msgChunk['responses'][x]['prompts'][0])
                else:
                    sendMessage("Try again, choosing from A, B, C, D, E, or H for Hint")
                x = waitForNewMessage().lower()
            if x == correct:
                sendMessage(msgChunk['responses'][x]['prompts'][0])

    sendMessage("Complete!\nYour Score: 300 points\nYour Time: 3:35")
           
#    sendMessage("You have completed Lesson " + str(data['lessonnum']) + ": " + data['name'] #+ ". Text one of the following options.")
#    sendMessage("L - Lesson\nQ - Quiz\nG - Grades\nP - Points\nS - Settings")
#    print "Done!"

runLesson()



# BUG - trailing spaces in prompts cause sent message mismatch error
