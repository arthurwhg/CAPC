###
# a general batch task execution job. 
# - upload batch task file
# - create batch task
# - check task status
# - download output file
#
# v1.0
#
###
import openai
import os
import requests
import time
from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

batch_file = f"{ROOT_DIR}/data/tasks/task_correction.jsonl"
envfile = f"{ROOT_DIR}/.env.production"
print(f".env file: {envfile}")
if not load_dotenv(envfile,verbose=True):
   print("error to load .env.production file")
   exit(1)
else:
  openai.api_key = os.getenv("OPENAI_API_KEY")  # Replace with a dummy key if needed

def get_status_detail(batch_id):
       while True:
        response = requests.get(
            f"https://api.openai.com/v1/batches/{batch_id}",
            headers={"Authorization": f"Bearer {openai.api_key}"}
        )

        status_data = response.json()  # Extract JSON response
        status = status_data.get("status", "unknown")

        print(f"Batch Status: {status}")

        if status == "failed":
            print("❌ Batch task failed!")
            failure_reason = status_data.get("error", {}).get("message")
            print(f"🔍 Failure Reason: {failure_reason}")
            return status_data

        if status == "completed":
            return status_data

        time.sleep(10)  # Wait 10 seconds before checking again


def check_batch_status(batch_id):
    while True:
        response = requests.get(
            f"https://api.openai.com/v1/batches/{batch_id}",
            headers={"Authorization": f"Bearer {openai.api_key}"}
        )
        #batch_status = openai.Batch.retrieve(batch_id)
        status = response.json()
        print(f"Batch Status: {status.get('status', 'unknown')}")

        if status.get("status") in ["completed", "failed"]:
            print(status)
            return status
        print(f"Batch Status: {response['status']} @ {time.now()}")
        time.sleep(300)  # Wait 10 seconds before checking again


# Upload JSONL File to OpenAI
def upload_file():
  print(f"uploading embadding batch file...")
  response = openai.File.create(
    file=open(batch_file, "rb"),
    purpose="batch"
  )

  file_id = response["id"]
  print(f"File uploaded successfully! File ID: {file_id}")
  return file_id


def create_batch_task(file_id):
  batch_response = requests.post(
    "https://api.openai.com/v1/batches",
    headers={"Authorization": f"Bearer {openai.api_key}", "Content-Type": "application/json"},
    json={
        "input_file_id": file_id,
        "endpoint": "/v1/chat/completions",
        "completion_window": "24h",
    },
  )
  # Get Batch ID
  if batch_response.status_code == 200:
    batch_id = batch_response.json()["id"]
    print(f"Batch processing started! Batch ID: {batch_id}")
    return batch_id
  else:
    print(f"Error creating batch task: {batch_response.text}")
    return None
  
fileID = upload_file()
#fileID = "file-GEm2NGuuFEn7EUtw31GDLH"
batch = create_batch_task(fileID)
#batch = "batch_67ca974eb3d881908dfc076ebf0cabfd"

if batch is not None:
   get_status_detail(batch)
