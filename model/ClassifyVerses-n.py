###
# This utility create neral network model and save the model, which model is used to label all other verses. 
# the model is saved in file /data/nm_classifier.h5 by default
#
# version v1.0
#
###
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras
from tensorflow.keras.utils import plot_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import os
import json
from embedding import Embedding

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

datafile = f"{ROOT_DIR}/data/kjv-trainingData.csv"
modelfile = f"{ROOT_DIR}/data/nm_classifier.h5"

X = []
y = []

DIM = 1536  # it is set by setDIM() function 
EPOCHs = 20
BATCH_SIZE = 32

embedding = Embedding()

def read_data(datafile):
  # read labeled data from file
  with open(datafile, "r", encoding="utf-8") as f:
    for line in f:
      line = line.strip()
      if line:
        rec = json.loads(line)
        # recude X dimention to 256
        emb = rec['embedding']
        #print(f"emb: {emb.shape}")
        X.append(emb)
        y.append(rec['topic'] if rec['topic'] < 21 else 20)
  f.close() 
  print(f"X shape: {np.array(X).shape}")
  print(f"y shape: {np.array(y).shape}")
  return np.array(X), np.array(y)

###
# reduce X dimention 
# method in ['PCA','UMAP','AutoEncoder']
# DIM final dimention of X
#  0 < DIM < min(X.shape[0], x.shape[1])
###
def reduce_dimention(method, DIM, X,y):
  # Convert to numpy arrays
  X = np.array(X)
  if DIM < min(X.shape[1], X.shape[0]):
    X = embedding.ReduceDim("AutoEncoder",X,DIM)
  y = np.array(y)
  #print(f"X shape: {X.shape}")
  #print(f"y shape: {y.shape}")
  return X, y

def setDIM(X):
  DIM = X.shape[1]
  return DIM

def split_data(X,y):
  # Split into training & testing sets (80% train, 20% test)
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  print(f"X train shape: {np.array(X_train).shape}")
  print(f"y shape: {np.array(y_train).shape}")
  return X_train, X_test, y_train, y_test

# Normalize embeddings (Important for NN stability)
# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)


def build_model(X, y, epochs, batch_size):

  X_train, X_test, y_train, y_test = split_data(X,y)

  # Define a neural network
  model = keras.Sequential([
      layers.Input(shape=(DIM,)),  # Input layer (1536-dimensional vectors)
      layers.Dense(DIM, activation="relu"),  # Hidden layer 1
      layers.Dropout(0.6), # aovid overfitting
      layers.Dense(128, activation="relu"),  # Hidden layer 1
      layers.Dropout(0.3), # aovid overfitting
      layers.Dense(64, activation="relu"),  # Hidden layer 1
      layers.Dense(21, activation="softmax")  # Output layer (10 classes)
  ])

  # Compile the model
  model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

  # Train for 20 epochs with a batch size of 32
  history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batch_size)
  return model, history, X_test, y_test

#print(f"history {history.history}")
def draw_plot(history, epochs, DIM, method):
  plt.figure(figsize=(12,5))
  plt.plot(epochs, history.history["accuracy"], marker="o", linestyle="-", linewidth=1, label="training")
  plt.plot(epochs, history.history["val_accuracy"], marker="o", linestyle="-", linewidth=1, label="validation")
  plt.legend(loc="upper left")
  plt.xlabel("epochs")
  plt.ylabel("accuracy")
  plt.title(f"accuracy: dimention {DIM} reduced by {method}")

  plt.figure(figsize=(12,5))
  plt.plot(epochs, history.history["loss"], marker="o", linestyle="-", linewidth=1, label="training")
  plt.plot(epochs, history.history["val_loss"], marker="o", linestyle="-", linewidth=1, label="validation")
  # Add Legends
  plt.legend(loc="upper left")
  plt.xlabel("epochs")
  plt.ylabel("loss")
  plt.title(f"loss: dimention {DIM} reduced by {method}")
  plt.show()
  return 


def evaluate_model(model, X_eval, y_eval):
  # Evaluate on the test set
  eval_loss, eval_acc = model.evaluate(X_eval, y_eval)
  print(f"✅ Test Accuracy: {eval_acc * 100:.2f}%")
  print(f"✅ Test loss: {eval_loss * 100:.2f}")
  return eval_loss, eval_acc

def save_model(model):
  model.save(modelfile,include_optimizer=True)
  print(f"✅ Model saved to {modelfile}")
  return

#### main steps starts here 
dim = 16
reduce_method = 'AutoEncoder'
X, y = read_data(datafile)
if dim < X.shape[1]:
  X, y = reduce_dimention(reduce_method, dim, X,y) # it is optional to disable this step to reduce dimention

DIM = setDIM(X)
model, history, X_test, y_test = build_model(X,y, EPOCHs, BATCH_SIZE)
model.summary()
# generate  the model chart
plot_model(model, to_file="model_nm_classifier.png", show_shapes=True, show_layer_names=True)
# generate the auto encoder model chart
if embedding.model is not None:
  plot_model(embedding.model, to_file="model_nm_autoencoder.png", show_shapes=False, show_layer_names=True)
embedding.model.summary()
epochs = range(1, len(history.history["loss"]) + 1)
draw_plot(history, epochs, DIM, reduce_method)
evaluate_model(model, X_test, y_test)
#save_model(model)
