from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "AC94743d49300d49a696cf09bfef229c82" 
AUTH_TOKEN = "459bb4d749bdff002e45d44d33a4ad7f" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
client.messages.create(
	to="4252467703", 
	from_="+12067454564",
    body="testing123"   
)
