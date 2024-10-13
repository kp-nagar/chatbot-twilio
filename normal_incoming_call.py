from typing import Union
from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse


app = FastAPI()


@app.post("/normal-answer")
async def answer_call(request: Request):
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Thank you for calling! Have a great day.", voice='Polly.Amy')

    return PlainTextResponse(str(resp), media_type="text/xml")
