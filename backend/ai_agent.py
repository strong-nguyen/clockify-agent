from pydantic_ai import Agent, BinaryContent, UserPromptPart, ModelRequest
from model import TimeEntry, SpeechTranscript
from datetime import datetime
import asyncio
from google import generativeai as genai

import os


print("LisT gemini models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"{m.name}")

time_entry_agent = Agent(
    "google-gla:gemini-3.1-flash-lite-preview",
    output_type=list[TimeEntry],
    system_prompt=
    "You are a helpful assistant that extracts time entry details from user messages. " \
    "Each time entry should include a start time, end time, and description. " \
    "The start and end times should be in ISO format (YYYY-MM-DDTHH:MM:SS). " \
    "If the user says 'today', use the current date provided in the context. " \
    "If the user says 'now', use the current time provided in the context.")

model = genai.GenerativeModel('models/gemini-3.1-flash-lite-preview')

async def extract_time_entries(user_message: str) -> list[TimeEntry]:
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Current Date Time: {today}, User Message: {user_message}"

    # We need to retry here because the models is busy sometimes
    for retry in range(5):
        try:
            result = await time_entry_agent.run(message)
            return result.output
        except Exception as e:
            print(f"Error extracting time entries: {e}")

            if retry < 4:
                print("Retrying...")
                await asyncio.sleep(1)  # Wait for a bit before retrying
                continue

            return []

async def agent_speech_to_text(audio_data):
    # We need to retry here because the models is busy sometimes
    for retry in range(5):
        try:
            audio_part = {"mime_type": "audio/wav", "data": audio_data}
            response = model.generate_content(["Transcribe this audio to text:", audio_part])
            transcript_text = response.text
            print(transcript_text)
            return transcript_text
        except Exception as e:
            print(f"Error while transcribe audio: {e}")

            if retry < 4:
                print("Retrying...")
                await asyncio.sleep(1)  # Wait for a bit before retrying
                continue

            return None
