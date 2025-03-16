import django
from tensorflow.keras.models import load_model
import os,sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(ROOT_DIR)
print(sys.path)
print(f"sys.path: {sys.path}")
# print(f"root directory ******: {ROOT_DIR}")

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "llm.settings")  # Replace `your_project` with the actual Django project name

# Initialize Django
django.setup()

from verses.models import Verse
from verses.verseSerializer import VerseSerializer
from model.embedding import Embedding
import numpy as np



modelfile = f"{ROOT_DIR}/data/nm_classifier.h5"

# load model from file
model = load_model(modelfile)
model.summary() 


# Get all verses vector from database where no topic marked
verses = Verse()
#verse_list = verses.getVerseswithoutTopic().all()
#verse_list = verses.objects.all()
verse_list = Verse.objects.filter(topic__isnull=True).only('id', 'cid')
print(f"total {verse_list.count()} to be updated!")

X = []
Verses = []
print("Adding vectors to the list ...")
for verse in verse_list.iterator():
    print(f"adding verse {verse.id} {verse.cid} vector in to the list ...")
    vt = {
        "id": verse.id,
        "cid": verse.cid,
    }
    Verses.append(vt)
    X.append(verse.embedding)

X = np.array(X)
print(f"X shape: {X.shape}")

#embedding = Embedding()


# predict topics
y_topic = model.predict(X)
print(f"y_topic shape: {y_topic.shape}")
y_topic = np.argmax(y_topic, axis=1)
print(y_topic[10:])

# update topic into database
for i in range(X.shape[0]):
    verse = Verses[i]
    verse_rec = Verse.objects.get(id=verse["id"])
    verse["topic"] = y_topic[i]
    verse["labeled"] = "Auto"
    verseSerializer = VerseSerializer(instance=verse_rec, data=verse, many=False)
    print(f'updating verse {verse["id"]} by topic {verse["topic"]}')
    if verseSerializer.is_valid(raise_exception=True):
        try:
            verseSerializer.save()
        except Verse.DoesNotExist:
            print(f"Verse {verse['id']} not found")
            continue
    else:
        print(f"Error: {verseSerializer.errors}")

