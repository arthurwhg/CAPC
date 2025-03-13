###
# This utility read verse embeddings from a JSONL file and update into database.
#
# version 1.0
#
###
import json
import os, sys
import django
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(ROOT_DIR)
print(sys.path)
print(f"sys.path: {sys.path}")
# print(f"root directory ******: {ROOT_DIR}")

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "llm.settings")  # Replace `your_project` with the actual Django project name

# Initialize Django
django.setup()

from verses.verseSerializer import VerseSerializer
from verses.models import Verse
from model.embedding import Embedding

kjv_embedding_file = f"{ROOT_DIR}/data/kjv-embedding-small.jsonl"

# Read JSONL file (line by line)
records = []
tokens = 0
prompt_tokens = 0
embedding = Embedding()
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
        customId = record['custom_id'].upper()
        verse = Verse.objects.filter(cid=customId)
        if verse.exists():
          ve = verse.first()
          ve.tokens = record['response']['body']['usage']['total_tokens']
          #verse.save()
          verseSerializer = VerseSerializer()
          # reduce the dimention to 256
          ve = verseSerializer.update_embedding(ve, record['response']['body']['data'][0]['embedding'])
          print(f"updated verse: {ve}")
        else:
          print(f"verse not found: {record['custom_id']}")

      except json.JSONDecodeError as e:
        print(f"Skipping corrupt line: {line} | Error: {e}")
    else:
      print("Skipping empty line")      

print(f"Prompt tokens: {prompt_tokens}, Total tokens: {tokens}")