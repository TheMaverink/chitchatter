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

from functions.openai_requests import convert_audio_to_text

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


# Post bot response
# Note: Not playing back in browser when using post request.
@app.post("/post-audio-get/")
async def get_audio(file: UploadFile = File(...)):
    audio_input = open("myFile.wav", "rb")
    # Decode audio
    message_decoded = convert_audio_to_text(audio_input)
    print("message_decoded")
    print(message_decoded)

    return "Done"