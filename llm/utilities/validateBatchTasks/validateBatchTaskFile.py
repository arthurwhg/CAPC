###
# This utilit is designed to explore the output file from a batch task file. It read batch task file and printout user cotent provided.
# Task type: chart completion 
#
# v1.0
#
###
import pandas as pd
import json
import os


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

file = f"{ROOT_DIR}/data/tasks/task_correction-small.jsonl"
#file = f"{ROOT_DIR}/data/tasks/task_correction_small.jsonl"
# Read and re-save the file to ensure UTF-8 encoding
#df = pd.read_json(embadding_batch_file, lines=True)
#print(df.describe())
#df.to_json(embadding_batch_file_fixed, orient='records', lines=True)
#df.to_json(embadding_batch_file_fixed, orient="records", lines=True, force_ascii=False)

characters = {
  'system' : 0,
  'user' : 0,
  'total' : 0
}

with open(file, "r", encoding="utf-8") as f:
  i=0
  lines = f.readlines()
  #print(len(lines))
  for line in lines:
    try:
      #print(i)
      i+=1
      data = json.loads(line)
      #print(data)
      messages = data["body"]["messages"]
      for message in messages:
            #print(message)
            if message["role"] == 'user':
                print(f'{message["content"]}')
            characters[message["role"]] += len(message["content"])
            characters["total"] += len(message["content"])
      
    #   totalToken["total_tokens"] += data["response"]["body"]["usage"]["total_tokens"]
    #   totalToken["completion_tokens"] += data["response"]["body"]["usage"]["completion_tokens"]
    #   totalToken["prompt_tokens"] += data["response"]["body"]["usage"]["prompt_tokens"]
    except json.JSONDecodeError as e:
      print(f"Error on line: {e} i")

print(f"Total characters: {characters}")