import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import os
import json
from embedding import Embedding

#Embedding = Embedding()

# Generate synthetic vector embeddings (100 samples, 100 dimensions each)
#np.random.seed(42)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

datafile = f"{ROOT_DIR}/data/kjv-trainingData.csv"
modelfile = f"{ROOT_DIR}/data/svm_classifier.pkl"

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

# Convert to numpy arrays
X = np.array(X)
y = np.array(y)
print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")


# Split into training & testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize embeddings (Important for NN stability)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# Define a simple feedforward neural network
model = keras.Sequential([
    layers.Input(shape=(1536,)),  # Input layer (1536-dimensional vectors)
    layers.Dense(512, activation="relu"),  # Hidden layer 1
    layers.Dropout(0.6),
    layers.Dense(128, activation="relu"),  # Hidden layer 1
    layers.Dense(64, activation="relu"),  # Hidden layer 1
    layers.Dropout(0.3),
    layers.Dense(21, activation="softmax")  # Output layer (10 classes)
])

# Compile the model
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# Train for 20 epochs with a batch size of 32
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=32)

# Evaluate on the test set
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"✅ Test Accuracy: {test_acc * 100:.2f}%")

