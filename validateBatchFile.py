import pandas as pd
import json

embadding_batch_file = "./data/embadding_batch.jsonl"
embadding_batch_file_fixed = "./data/embedding_batch20.jsonl"

# Read and re-save the file to ensure UTF-8 encoding
#df = pd.read_json(embadding_batch_file, lines=True)
#print(df.describe())
#df.to_json(embadding_batch_file_fixed, orient='records', lines=True)
#df.to_json(embadding_batch_file_fixed, orient="records", lines=True, force_ascii=False)

with open(embadding_batch_file_fixed, "r", encoding="utf-8") as f:
  i=0
  for line in f:
    try:
      print(i)
      i+=1
      json.loads(line)
    except json.JSONDecodeError as e:
      print(f"Error on line: {e} i")