import pandas as pd
import json

csv = pd.read_csv("./data/kjv.csv")

embadding_batch_file = "./data/embedding_batch.jsonl"

id=0
with open(embadding_batch_file,"w", encoding="utf-8") as f:
  for text in csv["verse_text"]:
    custom_id = "kjv-"+str(id)
    id+=1
    #line = f'{"method": "POST","url":"/v1/embeddings","body":{"input": {text}, "model": "text-embedding-3-small","encoding_format": "float"},"custom_id": "{custom_id}"}\n'
    line = f'{{"method": "POST","url":"/v1/embeddings","body":{{"input": "{text}", "model": "text-embedding-3-small","encoding_format": "float"}},"custom_id": "{custom_id}"}}\n'
    f.write(line)
# ckeep = csv[['verse_text']]
# ckeep = ckeep.rename(columns={
#     'verse_text': 'input'
# })
# ckeep.to_json(embadding_batch_file_fixed, orient="records", lines=True, force_ascii=False)    
print(f"JSONL file '{embadding_batch_file}' created successfully!")