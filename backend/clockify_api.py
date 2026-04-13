import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CLOCKIFY_API_KEY")
ICT_Timezone = "+07:00"  # I am using Vietnam timezone, you can change it to your timezone if needed


def get_slower_workspace_id():
  headers = {"X-Api-Key": api_key}

  response = requests.get("https://api.clockify.me/api/v1/workspaces", headers=headers)
  workspaces = response.json()

  for workspace in workspaces:
    if workspace["name"] == "Slower":
      return workspace["id"]
  return None

def list_clockify_workspace():
  headers = {"X-Api-Key": api_key}

  response = requests.get("https://api.clockify.me/api/v1/workspaces", headers=headers)
  workspaces = response.json()

  list_workspaces = []
  for workspace in workspaces:
    list_workspaces.append({"name": workspace["name"], "id": workspace["id"]})
  print(list_workspaces)
  return list_workspaces


def get_project_id(workspace_id, project_name):
  headers = {"X-Api-Key": api_key}
  url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects"
  response = requests.get(url, headers=headers)
  projects = response.json()

  for project in projects:
    if project["name"] == project_name:
      return project["id"]
  return None

def list_clockify_projects(workspace_id: str):
  headers = {"X-Api-Key": api_key}
  url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects"
  response = requests.get(url, headers=headers)
  projects = response.json()

  list_projects = []
  for project in projects:
    list_projects.append({"name": project["name"], "id": project["id"]})
  return list_projects

def create_time_entry(workspace_id, start_time, end_time, description, project_id=None):
  headers = {
    "X-Api-Key": api_key,
    "Content-Type": "application/json"
  }

  data = {
    "start": start_time.isoformat() + ICT_Timezone, 
    "end": end_time.isoformat() + ICT_Timezone,
    "description": description,
  }
  if project_id:
    data["projectId"] = project_id

  url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/time-entries"
  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 201:
    return (True, response.text)
  else:
    return (False, response.text)

