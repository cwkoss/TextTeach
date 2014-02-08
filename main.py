#Q's for dad
# - Logging to file - have a fav package?  Any style notes?

import time

import json
from pprint import pprint
json_data = open('lesson.json')
data = json.load(json_data)
json_data.close()

keepRunning = True #variable for admin to send kill msg
SLEEPTIME = 0 #sets delay in main loop for throttling

sessions = {} #dictionary of sessions, with phone num strings as keys

#init sets up program to start running
def init():
    main()

#main loop which calls sub-functions
def main():
    msgsToSend = []
    newMsgs = getNewMessages()
    for msgConf in newMsgs:
        if msgConf["msgType"] = "start":
            msgsToSend.append(handleStart(msgConf))
        elif msgConf["msgType"] = "input":
            msgsToSend.append(handleNewInput(msgConf))
        elif msgConf["msgType"] = "confirm":
            msgsToSend.append(handleConfirmedMsg(msgConf))
        else:
            print "main() - Message type not recognized"

    sendQueuedMsgs(msgsToSend)


    #loop unless kill message received from admin
    if keepRunning:
        time.sleep(SLEEPTIME)
        main()

#checks message array for new items
#returns array of Confirmed Messages
def getNewMessages():

# creates a new session for the phonenumber which 
# texted "start"
def handleStart(msgConf):
    sessions[msgConf.phoneNum] = Session(msgConf.phoneNum)
    return sessions[msgConf.phoneNum].nextSendableMessage()

#responds to received input
def handleNewInput(msgConf):
    return sessions[msgConf.phoneNum].respondToInput(msgConf)

#
def handleConfirmedMsg(msgConf):
    sessions[msgConf.phoneNum].confirmMessage(msgConf)
    return sessions[msgConf.phoneNum].nextSendableMessage()    

def sendSMS(phoneNum, body):
    print "send to " + phoneNum + ": " + body

class Session:
    def __init__(self, phoneNum):
        self.phoneNum = phoneNum
        self.msgChunk = 1 
        self.promptIndex = 1 
        # TODO: Add time tracking
        #self.startTime = start time
        self.initialMsgIndex = -1 # set to index after start msg confirmed

        self.state = "starting"
        self.lastMsg = ""
        # Session States
        # "starting" - Cue to send first message
        # "msgQueued" - message added to send SMS queue, waiting for confirmation
        # "msgSent" - message has been sent
        # "msgConfirmed" - sent SMS confirmed, go to next prompt or chunk
        # "waitingInput" - waiting for user SMS reply
        # "receivedInput" - state for SMS received, needs to be processed and send next
        # "finish" - lesson complete, close out lesson

    def nextSendableMessage():
        body = data['msgChunks'][self.msgChunk]['prompts'][self.promptIndex]
        self.lastMsg = body
        self.state = "msgQueued"
        return SendableMessage(self.phonenum, body)

    def respondToInput(msgConf):
        x = msgConf.body[0] #use only first char of message
        if(x == "a" or x == "b" or x == "c" or x == "d" or x == "e" or x == "h"):
            body = msgChunk['responses'][x]['prompts'][0]
            #check if correct
            if data['msgChunks'][self.msgChunk]['responses'][x]['correct']:
                self.msgChunk += 1 #if correct, move on to next msgChunk
                self.prompts = 1
        else:
            body = "Try again, choosing from A, B, C, D, E, or H for Hint"
        self.lastMsg = body
        self.state = "msgQueued"
        return SendableMessage(self.phonenum, body)

    def confirmMessage(msgConf):
        if msgConf.body != self.lastMsg:
            print "Error - confirmMessage expected:" + self.lastMsg
            print  "    received: " + msgConf.body
        else:
            self.state = "msgConfirmed"
            
    def moveToNextPrompt():
        if data['msgChunks'][self.msgChunk]['prompts']s
        
        

class MessageConfirmation:
    def __init__(self, msgType, phoneNum, body):    
        self.msgType = msgType
        self.phoneNum = phoneNum
        self.body = body

class SendableMessage:
    def __init__(self, phonenum, body, confType)
        self.phoneNum = phoneNum
        self.body = body
        self.confType = confType
