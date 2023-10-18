# uvicorn main:app
# uvicorn main:app --reload

# Main imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
from dotenv import dotenv_values

config = dotenv_values(".env")
openaiOrgKey = config["OPEN_AI_ORG"]
openaiApiKey = config["OPEN_API_KEY"]

from functions.database import store_messages,reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.text_to_speech import convert_text_to_speech

# Get Environment Vars
openai.organization = openaiOrgKey
openai.api_key = openaiApiKey

app = FastAPI()

# CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
]

# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Check health
@app.get("/health")
async def check_health():
    return {"response": "healthy"}

# reset messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "conversation reset"}




# Post bot response
# Note: Not playing back in browser when using post request.
@app.post("/post-audio/")
async def post_audio(file:UploadFile=File(...)):
    # audio_input = open("test.mp3", "rb")
    with open(file.filename,"wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename,"rb")


    # Decode audio
    message_decoded = convert_audio_to_text(audio_input)

    if not message_decoded:
        return HTTPException(status_code=400,detail="Failed to decode Audio")
    print("message_decoded")
    print(message_decoded)

    chat_response = get_chat_response(message_decoded)

    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")
    
    store_messages(message_decoded,chat_response)

    print("chat_response")
    print(chat_response)

    audio_output = convert_text_to_speech(chat_response)

    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get audio")

    # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    # Use for Post: Return output audio
    return StreamingResponse(iterfile(),  media_type="application/octec-stream")