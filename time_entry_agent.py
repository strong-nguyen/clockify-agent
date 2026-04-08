from pydantic_ai import Agent
from model import TimeEntry
from datetime import datetime
import asyncio


# 2. Setup the Agent (Use your Gemini API Key)
agent = Agent(
    # 'google-gla:gemini-3-flash-preview',
    "google-gla:gemini-2.5-flash",
    output_type=list[TimeEntry],
    system_prompt="You are a helpful assistant that extracts time entry details from user messages. Each time entry should include a start time, end time, and description. The start and end times should be in ISO format (YYYY-MM-DDTHH:MM:SS). " \
    "If the user says 'today', use the current date provided in the context.")

async def extract_time_entries(user_message: str) -> list[TimeEntry]:
    today = datetime.now().strftime("%Y-%m-%d")
    message = f"Current Date: {today}, User Message: {user_message}"

    # We need to retry here because the models is busy sometimes
    for retry in range(5):
        try:
            result = await agent.run(message)
            return result.output
        except Exception as e:
            print(f"Error extracting time entries: {e}")

            if retry < 4:
                print("Retrying...")
                await asyncio.sleep(1)  # Wait for a bit before retrying
                continue

            return []
