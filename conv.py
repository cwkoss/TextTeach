import json
from pprint import pprint
json_data = open('lesson.json')
data = json.load(json_data)
json_data.close()
#pprint(data['msgChunks'][0])
#x = raw_input()
#print x

print "Welcome to " + data['course']

print "Text L for a lesson or S for settings"
x = raw_input()
while(x.lower() != "l"):
    print "Settings have not been implemented, just text L to continue"
    x = raw_input()

for msgChunk in data['msgChunks']:
    for prompt in msgChunk['prompts']:
        print(prompt)
    if msgChunk['type'] == 'info':
        x = ""
        while(x.lower() != "c"):
            print("Text C to continue.")
            x = raw_input()
    elif msgChunk['type'] == 'multi':
        x = ""
        correct = ""
        for response in msgChunk['responses']:            
            if msgChunk['responses'][response]['correct']:
                correct = response
        x = raw_input().lower()
        while(x != correct):
            if(x == "a" or x == "b" or x == "c" or x == "d"):
                print(msgChunk['responses'][x]['prompts'][0])
            else:
                print "Try again, choosing from A, B, C, or D."
            x = raw_input().lower()
        if x == correct:
            print(msgChunk['responses'][x]['prompts'][0])
        
        


print "Done!"
