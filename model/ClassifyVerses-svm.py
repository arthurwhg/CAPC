###
# This utility creates a SVM for verses labeling. 
# The model is saved in file "data/svm_classifier.pkl" by default.
#
# version 1.0
#
###
import numpy as np
import pandas as pd
from sklearn.svm import NuSVC, SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
import os
import json
from embedding import Embedding
from sklearn.model_selection import GridSearchCV
import pickle
import matplotlib.pyplot as plt



# Generate synthetic vector embeddings (100 samples, 100 dimensions each)
#np.random.seed(42)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

datafile = f"{ROOT_DIR}/data/kjv-trainingData.csv"
modelfile = f"{ROOT_DIR}/data/svm_classifier.pkl"

X = []
y = []

embedding = Embedding()

# read labeled data from file
with open(datafile, "r", encoding="utf-8") as f:
  for line in f:
    line = line.strip()
    if line:
      rec = json.loads(line)
      # recude X dimention to 256
      emb = rec['embedding']
      X.append(emb)
      y.append(rec['topic'])
f.close() 

# Convert to numpy arrays
X = np.array(X)
y = np.array(y)
print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")

# scaler = StandardScaler(with_mean=True, with_std=True)
# X_scaled = scaler.fit_transform(X)
# y_scaled =scaler.transform(y)

# X = embedding.ReduceDim('UMAP', X, 64)


# Normalize features

#X_test_scaled = scaler.transform(X_test)

RESULT = pd.DataFrame()

def manual_search(RESULT, dim, reDim = None ):
   # reduce dimention
   if reDim is not None:
      X_red = embedding.ReduceDim(reDim,X,dim)
   else:
      X_red = X


   # Split data into training (80%) and testing (20%)
   X_train, X_test, y_train, y_test = train_test_split(X_red, y, test_size=0.2, random_state=42)
   for kernel in ["linear", "poly", "rbf", "sigmoid"]:
   # Initialize and train the SVM classifier
      for c in [1.0,1.5,2.0,2.5,3.0,4.0,.5,5.0,5.5,6.0,7.0,8.0,9.0,10.0] : 
      #svm_model = make_pipeline(StandardScaler(), NuSVC(nu=0.5, kernel=kernel, degree=5))
      #svm_model.fit(X_train, y_train)
      #make_pipeline(steps=[('standardscaler', StandardScaler()), ('nusvc', NuSVC())])
         for degree in [2,3,4,5,9]:
            svm_model = SVC(kernel=kernel, C=c, degree=degree)
            svm_model.fit(X_train, y_train)
      # Make predictions on the test set
            y_pred = svm_model.predict(X_test)
      # Calculate accuracy
            accuracy = accuracy_score(y_test, y_pred)
            mse = np.mean((y_test - y_pred) ** 2)
            if kernel != 'poly':
               print(f"ReDim: {reDim}, kernel: {kernel}, C: {c}, MSE: {mse:.2f}, Accuracy: {accuracy * 100:.2f}%")
            else:
               print(f"ReDim: {reDim}, jkernel: {kernel}, C: {c}, degree: {degree}, MSE: {mse:.2f}, Accuracy: {accuracy * 100:.2f}%")
            row = pd.DataFrame([{'R-DIM':reDim, 'kernel':kernel, 'C': c,'Degree':degree, 'MSE':mse, 'Accuracy':accuracy}])     
            RESULT = pd.concat([RESULT, row], ignore_index=True)

   #print(RESULT)
   return(RESULT)

def GridSearch():
   param_grid = {
    "C": [0.1, 1.0,1.5,2.0,2.5,9,10],
    "kernel": ["linear", "poly", "rbf", "sigmoid"],
    "degree": [2,3,4,5,6,7,8,9],  # Only for poly kernel
    "gamma": ["scale", "auto"]
}
   svm_model = SVC()
   grid_search = GridSearchCV(svm_model, param_grid, cv=5, scoring="accuracy")
   grid_search.fit(X_train, y_train)
   return grid_search

# grid_search = GridSearch()
# print(f"✅ Best SVM Parameters: {grid_search.best_params_}")
def train_model(X_train, y_train):
   hyperParameter = {
        "kernel": "poly", 
        "c": 2.5, 
        "degree": 2,
   }
   svm_model = SVC(kernel=hyperParameter['kernel'], C=hyperParameter['c'], degree=hyperParameter['degree'])
   svm_model.fit(X_train, y_train)
   return svm_model

def save_model(model, file):
    # Save model using pickle
    with open(file, "wb") as f:
        try:
            pickle.dump(model, f)
            f.close()
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False

def load_model(file):
    try:
        with open(file, "rb") as f:
            model = pickle.load(f)
            f.close()
            return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def test_model(model, X_test, y_test):
   y_pred = model.predict(X_test)
   accuracy = accuracy_score(y_test, y_pred)
   mse = np.mean((y_test - y_pred) ** 2)
   return(accuracy, mse)

def predict(model,X):
   y = model.predict(X)
   return y

def draw_plot(df, title):
   linecolor = ("Red","Blue","Green","Cyan","Yellow","Cyan")
   C = df['C'].unique()
   plt.figure(figsize=(10, 6))
   for kernel in df['kernel'].unique():
      kernel_data = df[df['kernel'] == kernel]
      data_grouped = kernel_data.groupby(['C','kernel']).agg({'Accuracy': 'mean'})
      plt.plot(C,data_grouped['Accuracy'], label=kernel)
      if kernel == 'poly':
         color = 0
         for degree in kernel_data['Degree'].unique():
            degree_data = kernel_data[kernel_data['Degree'] == degree]
            #data_grouped = degree_data.groupby(['C','kernel','Degree']).agg({'Accuracy': 'mean'})
            plt.plot(C, degree_data['Accuracy'], color=linecolor[color], linestyle='--', label=f"{kernel}:Degree {degree}")
            color += 1
   
   plt.xlabel('C')
   plt.ylabel('Accuracy')
   plt.title(f'Accuracy vs. C {title}')
   plt.legend()  
   plt.show()
   return


RESULT = pd.DataFrame()
origin = manual_search(RESULT, 0)
#print(RESULT)
draw_plot(origin,"1536-D")


umap = manual_search(RESULT, 16, "UMAP")
#print(umap)
draw_plot(umap,"UMAP 16-D")


AutoEncoder = manual_search(RESULT, 16, "AutoEncoder")
# print(AutoEncoder)
draw_plot(AutoEncoder,"AutoEncoder 16-D")


### main process
# model = train_model(X_train, y_train)
# accuracy, mse = test_model(model, X_test, y_test)
# print(f"Accuracy: {accuracy * 100:.2f}%, MSE: {mse:.2f}")
# saved = save_model(model, modelfile )
# if saved: print(f"the model is saved to {modelfile}")
# print(f"load model to test")
# loaded_model = load_model(modelfile)
# accuracy2, mse2 = test_model(loaded_model, X_test, y_test)
# print(f"Accuracy: {accuracy2 * 100:.2f}%, MSE: {mse2:.2f}")

# rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
# rf_model.fit(X_train, y_train)
# y_pred = rf_model.predict(X_test)
# # Calculate accuracy
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Accuracy: {accuracy * 100:.2f}%")


