from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import UserMessage, TimeEntry
from clockify_api import get_slower_workspace_id, get_project_id, create_time_entry
from time_entry_agent import extract_time_entries
from datetime import datetime

import sys


app = FastAPI()

origins = [
    "http://localhost:3000", # Port của Next.js bạn đang dùng
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Cho phép các origin trong danh sách
    allow_credentials=True,
    allow_methods=["*"],              # Cho phép tất cả các method (GET, POST, PUT, DELETE,...)
    allow_headers=["*"],              # Cho phép tất cả các headers (Content-Type, X-Api-Key,...)
)

slower_workspace_id = get_slower_workspace_id()
if not slower_workspace_id:
    print("[Error] Cannot found workspace Slower in Clockify.", file=sys.stderr)
    exit(1)
project_id = get_project_id(slower_workspace_id, "PxPoint")
if not project_id:
    print("[Warn] Cannot found PxPoint project in workspace Slower.", file=sys.stderr)

@app.post("/add-time-entry")
async def add_time_entry(user_message: UserMessage):
    msg = user_message.message
    time_entries = await extract_time_entries(msg)
    for index, time_entry in enumerate(time_entries):
        print(f"Task {index} -- start: {time_entry.start_time}, end: {time_entry.end_time}, description: {time_entry.description}")

        start_time = datetime.fromisoformat(time_entry.start_time)
        end_time = datetime.fromisoformat(time_entry.end_time)

        ret, response = create_time_entry(slower_workspace_id, start_time, end_time, time_entry.description, project_id)
        if not ret:
            print(f"[Error] Failed to add time entry for task {index}: {response}", file=sys.stderr)
            raise HTTPException(status_code=500, detail=f"Failed to add time entry for task {index}: {response}")
    return {"message": "Time entry added successfully!"}