from pydantic import BaseModel, Field


class UserMessage(BaseModel):
    message: str = Field(..., min_length=1, description="The user's message containing time entry details.")


class TimeEntry(BaseModel):
    start_time: str
    end_time: str
    description: str


class SpeechTranscript(BaseModel):
    transcript: str
    confidence_score: float
    detected_language: str
    # key_points: list[str]