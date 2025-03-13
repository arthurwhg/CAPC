import pandas as pd
import json
import os, sys
import django
import numpy as np

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

labeledfile = f"{ROOT_DIR}/data/kjv-labeledbyTopics.csv"
trainingdataFile = f"{ROOT_DIR}/data/kjv-trainingData.csv"


## remove embedding attribute and return a dict
def RemoveEmbeddingAttribute(verse, verseLabeled):
    new_verse ={}
    new_verse["id"] = verse.id
    new_verse["version_name"] = verse.version_name
    new_verse["version_abbr"] = verse.version_abbr
    new_verse["testament_abbr"] = verse.testament_abbr
    new_verse["testament_name"] = verse.testament_name
    new_verse["book_name"] = verse.book_name
    new_verse["book_number"] = verse.book_number
    new_verse["chapter_number"] = verse.chapter_number
    new_verse["verse_number"] = verse.verse_number
    new_verse["topic"] = verseLabeled['topic_number']

    return new_verse

counter_by_topic = np.zeros(30)
counter_by_books = np.zeros(70)

csv = pd.read_csv(f"{ROOT_DIR}/data/kjv-labeledbyTopics.csv")
id=0
records = csv.shape[0]
list = []
#print(f"total records: {records}")
# verses = csv.to_json(orient="records")
# print(verses[1])
# print(verses[2])
# print(f"total records: {records}, first 5 records: {verses[2:6]}")
print(f"total records: {records}")
updated =0
for id in range(records):
    print(f"id {id} topic: {csv.iloc[id]['topic_number']}")
    #print(csv.iloc[id].to_json())
    data = csv.iloc[id].to_json()
    dict = csv.iloc[id].to_dict()
    verses = Verse.objects.all()
    if dict['topic_number'] != 'nan' and dict['topic_number'] > 0 and dict['topic_number'] is not None:


        custom_id = dict['version_abbr']+'-'+str(id)
        verse = verses.get(cid=custom_id)
        if verse is not None:
            top = int(dict['topic_number']) -1
            print(top)
            counter_by_topic[top]+= 1
            counter_by_books[verse.book_number]+= 1
            new_verse = RemoveEmbeddingAttribute(verse, dict)
            print("update the verse")
            verseSerializer = VerseSerializer()
            #verseSerializer.update(verse, new_verse)
            updated += 1

            data = {}
            data['topic'] = dict['topic_number']
            data['embedding'] = verse.embedding.tolist()
            data['cid'] = verse.cid
            
            list.append(data)
    else:
        print("ignore the verse")

with open( trainingdataFile,"w", encoding="utf-8") as f:
    for rec in list:
        #print(rec)
        f.write(f"{json.dumps(rec)} \n")
f.close
print(f"updated: {updated} records")
for id in range(len(counter_by_topic)):
    print(f"Topic: {id}, Count: {counter_by_topic[id]}")
for id in range(len(counter_by_books)):
    print(f"Book: {id}, Count: {counter_by_books[id]}")

