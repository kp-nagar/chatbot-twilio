from fastapi import FastAPI
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/get-transcript")
async def answer_call(request: Request):
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()
    resp.say("Hello, please leave a message after the beep.", voice='Polly.Amy')
    resp.record(transcribe=True, transcribe_callback="/transcription")

    # Read a message aloud to the caller
    resp.say("Thank you for calling! Have a great day.", voice='Polly.Amy')

    # Return the TwiML response as plain text
    return PlainTextResponse(str(resp), media_type="text/xml")

# Endpoint to receive transcriptions
@app.post("/transcription")
async def transcription(request: Request):
    form_data = await request.form()
    transcription_text = form_data.get("TranscriptionText")
    print("Transcription:", transcription_text)
    return {"status": "success"}

