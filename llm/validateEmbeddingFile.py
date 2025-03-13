import json
kjv_embedding_file = "./data/kjv-embedding-small.jsonl"

# Read JSONL file (line by line)
records = []
tokens = 0
prompt_tokens = 0
with open(kjv_embedding_file, "r", encoding="utf-8") as f:
  for line in f:
    line = line.strip()
    if line:  # Skip blank lines
      try:
        record = json.loads(line)
        records.append(record)
        #print(record.keys())
        print(f"verse: {record['custom_id']}, embedding: {len(record['response']['body']['data'][0]['embedding'])}, token:{record['response']['body']['usage']['total_tokens']}")
        #print(len(record['response']['body']['data'][0]['embedding']))
        tokens += int(record["response"]["body"]["usage"]["total_tokens"])
        prompt_tokens += int(record["response"]["body"]["usage"]["prompt_tokens"])
        #print(f"verse: {record.id}, embedding: {len(record.body.data[0].embedding)}, token:{record.usage.total_tokens}\n")
      except json.JSONDecodeError as e:
        print(f"Skipping corrupt line: {line} | Error: {e}")
    else:
      print("Skipping empty line")      

print(f"Prompt tokens: {prompt_tokens}, Total tokens: {tokens}")
#print(len(records))  # List of dictionaries
# Read JSON file
# df = pd.read_json(kjv_embedding_file)  # Works for JSON lists
# print(df.head())
# print(df.head(2).to_json(orient="records"))