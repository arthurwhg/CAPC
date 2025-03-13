import pandas as pd
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

csv = pd.read_csv(f"{ROOT_DIR}/data/kjv.csv")
id=0
records = csv.shape[0]
#print(f"total records: {records}")
# verses = csv.to_json(orient="records")
# print(verses[1])
# print(verses[2])
# print(f"total records: {records}, first 5 records: {verses[2:6]}")
print(f"total records: {records}")
for id in range(records):
    print(id)
    print(csv.iloc[id].to_json())
    data = csv.iloc[id].to_json()
    dict = csv.iloc[id].to_dict()
    customer_id = dict['version_abbr']+'-'+str(id)
    print(customer_id)
    dict['customId'] = customer_id
    dict['verse'] = dict['verse_text']
    print(json.dumps(dict))

    verse_serializer = VerseSerializer(data=dict)
    if verse_serializer.is_valid():
        print("saving verse:"+ customer_id)
        verse_serializer.save()
    else:
        print(verse_serializer.errors)
    #line = f'{"method": "POST","url":"/v1/embeddings","body":{"input": {text}, "model": "text-embedding-3-small","encoding_format": "float"},"custom_id": "{custom_id}"}\n'
    #line = f'{{"method": "POST","url":"/v1/embeddings","body":{{"input": "{text}", "model": "text-embedding-3-small","encoding_format": "float"}},"custom_id": "{custom_id}"}}\n'
    #print(version, version_abbr, testment, testament_abbr, book, Blocking_number, chapter, verse, text)