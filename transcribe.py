from openai import OpenAI
import os

client = OpenAI(api_key="api")


def transcribe_video(file_path: str):
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file
        )

    return {
        "text": transcript.text
    }