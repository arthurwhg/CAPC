###
# This utilit is designed to explore the output file from a batch task. It read batch task output file and show cotent provided.
# Task Type: chat completion
# 
# v1.0
#
###
import pandas as pd
import json
import os


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

# embadding_batch_file = "./data/embadding_batch.jsonl"
# embadding_batch_file_fixed = "./data/embedding_batch20.jsonl"
file = f"{ROOT_DIR}/data/batch_67d3d0cc7b748190b9a52a72c0a1e3e4_output.jsonl"
#file = f"{ROOT_DIR}/data/tasks/task_correction_small.jsonl"
# Read and re-save the file to ensure UTF-8 encoding
#df = pd.read_json(embadding_batch_file, lines=True)
#print(df.describe())
#df.to_json(embadding_batch_file_fixed, orient='records', lines=True)
#df.to_json(embadding_batch_file_fixed, orient="records", lines=True, force_ascii=False)

totalToken = {
  'prompt_tokens' : 0,
  'completion_tokens' : 0,
  'total_tokens' : 0
}

with open(file, "r", encoding="utf-8") as f:
  i=0
  lines = f.readlines()
  print(len(lines))
  for line in lines:
    try:
      #print(i)
      i+=1
      data = json.loads(line)
      #print(data)
      print(data["response"]["body"]["choices"][0]["message"]["content"])
      totalToken["total_tokens"] += data["response"]["body"]["usage"]["total_tokens"]
      totalToken["completion_tokens"] += data["response"]["body"]["usage"]["completion_tokens"]
      totalToken["prompt_tokens"] += data["response"]["body"]["usage"]["prompt_tokens"]
    except json.JSONDecodeError as e:
      print(f"Error on line: {e} i")

print(f"Total token: {totalToken}")