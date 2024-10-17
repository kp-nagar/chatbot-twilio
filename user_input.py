from fastapi import FastAPI, Request
from fastapi.responses import Response, HTMLResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = FastAPI()


@app.post("/normal-answer")
async def voice(request: Request):
    """Handles incoming voice calls."""
    response = VoiceResponse()
    
    gather = Gather(input='dtmf speech', action='/gather', method='POST')
    gather.say("Press 1 to ask a query to the bot, press 2 to hang up.")
    response.append(gather)
    response.redirect('/normal-answer')  # Redirect to get input if no input is received

    return HTMLResponse(content=str(response), status_code=200)

@app.post("/gather")
async def gather(request: Request):
    """Processes user input from the gather."""
    response = VoiceResponse()
    data = await request.form()

    user_input = data.get("Digits")
    
    if user_input == "1":
        response.say("Please ask your question after the beep.")
        response.record(action='/record', max_length=10, transcribe=True, transcribe_callback="/transcription")
    elif user_input == "2":
        response.say("Goodbye!")
        response.hangup()
    else:
        response.say("Invalid option. Press 1 to ask a question or 2 to hang up.")
        response.redirect('/voice')

    return HTMLResponse(content=str(response), status_code=200)

# Endpoint to receive transcriptions
@app.post("/transcription")
async def transcription(request: Request):
    form_data = await request.form()
    transcription_text = form_data.get("TranscriptionText")
    print("Transcription:", transcription_text)
    return {"status": "success"}
