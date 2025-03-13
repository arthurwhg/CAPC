import tensorflow as tf
from tensorflow.keras.models import load_model
import os
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

datafile = f"{ROOT_DIR}/data/kjv-trainingData.csv"
modelfile = f"{ROOT_DIR}/data/nm_classifier.h5"

X = []
y = []

# read labeled data from file
with open(datafile, "r", encoding="utf-8") as f:
  for line in f:
    line = line.strip()
    if line:
      rec = json.loads(line)
      # recude X dimention to 256
      emb = rec['embedding']
      X.append(emb)
      y.append(rec['topic'] if rec['topic'] < 21 else 20)
f.close() 

model = load_model(modelfile)

# Recompile the model with the original loss and metrics
#model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

loss, accuracy = model.evaluate(X, y, batch_size=32, verbose=2)
print(f"evaluation loss {loss}")
print(f"evaluation accuracy {accuracy}")