import openai
from decouple import config

from dotenv import dotenv_values
from functions.database import get_recent_messages

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


def get_chat_response(message_input):
    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)
    print(messages)

    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
        print(response)

        message_text = response["choices"][0]["message"]["content"]
        print(message_text)
        return message_text
    except Exception as error:
        print(error)
        return
