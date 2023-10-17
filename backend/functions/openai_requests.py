import openai
from decouple import config

from dotenv import dotenv_values

config = dotenv_values(".env")
openaiOrgKey = config["OPEN_AI_ORG"]
openaiApiKey = config["OPEN_API_KEY"]

# Retrieve Enviornment Variables
openai.organization = openaiOrgKey
openai.api_key = openaiApiKey


# Open AI - Whisper
# Convert audio to text
def convert_audio_to_text(audio_file):
  try:
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    message_text = transcript["text"]
    return message_text
  except Exception as e:
    return
