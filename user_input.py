from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = FastAPI()

class XMLResponse(Response):
    media_type = "application/xml"


@app.post("/normal-answer")
async def voice(request: Request):
    """Handles incoming voice calls."""
    response = VoiceResponse()
    
    gather = Gather(input='dtmf speech', action='/gather', method='POST')
    gather.say("Press 1 to ask a query to the bot or press 2 to hang up.")
    response.append(gather)
    response.redirect('/normal-answer')  # Redirect to get input if no input is received

    return XMLResponse(content=str(response))

@app.post("/gather")
async def gather(request: Request):
    """Processes user input from the gather."""
    response = VoiceResponse()
    data = await request.form()

    user_input = data.get("Digits")
    
    if user_input == "1":
        response.say("Please ask your question after the beep.")
        response.record(action='/record', max_length=10, transcribe=True, transcribe_callback="")
    elif user_input == "2":
        response.say("Goodbye!")
        response.hangup()
    else:
        response.say("Invalid option. Press 1 to ask a question or 2 to hang up.")
        response.redirect('/voice')

    return XMLResponse(content=str(response))
