from sklearn.decomposition import PCA
import umap
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.optimizers import Adam

class Embedding():

    def __init__(self):
        super()
        # Example: Original embeddings (N samples, 1536 dimensions)
        self.reduced_embeddings = None 
        self.input_dim = 1536
        self.err = ""
        self.model = None

    def ReduceDim(self,model, embedding, n_components= 256):
        self.original_embeddings = embedding
        self.input_dim = embedding.shape[1]
        self.reduced_dim = n_components
        # Ensure embedding is 2D: (samples, features)
        if self.original_embeddings.shape[0] == 1:
            self.original_embeddings = self.original_embeddings.reshape(1, -1)
            self.input_dim = self.original_embeddings.shape[1]

        self.reduced_dim = n_components
        if model == 'PCA':
            return self.PCAReduceDim(embedding)
        elif model == 'UMAP':
            return self.UMAPReduceDim(embedding)
        elif model == 'AutoEncoder':
            return self.AutoEncoder(embedding)
        else:
            return None

    def PCAReduceDim(self,embedding):

            # Check shape before PCA
            print(f"Embedding shape before PCA: {self.original_embeddings.shape}")  

            # Reduce dimensions to 256
            pca = PCA(n_components=self.reduced_dim)
            self.reduced_embeddings = pca.fit_transform(self.original_embeddings)
            self.model = pca
            # Check shape before PCA
            print(f"Embedding shape after PCA: {self.reduced_embeddings.shape}")  

            return(self.reduced_embeddings)

    def UMAPReduceDim(self,embedding):
        # Reduce to 256 dimensions
        umap_model = umap.UMAP(n_components=self.reduced_dim)
        self.reduced_embeddings = umap_model.fit_transform(self.original_embeddings)
        self.model = umap_model
        return(self.reduced_embeddings)
    
    def AutoEncoder(self, embedding):
        # Define Autoencoder Model
        input_layer = layers.Input(shape=(self.input_dim,))
        encoded = layers.Dense(self.reduced_dim, activation='relu')(input_layer)
        encoded = layers.Dense(self.reduced_dim-120, activation='relu')(encoded)
        encoded = layers.Dense(self.reduced_dim-240, activation='relu')(encoded)

        decoded = layers.Dense(self.input_dim * 2, activation='relu')(encoded)
        decoded = layers.Dense(round(self.input_dim * 1.1), activation='relu')(encoded)
        decoded = layers.Dense(self.input_dim, activation='sigmoid')(decoded)

        autoencoder = Model(input_layer, decoded)
        encoder = Model(input_layer, encoded)  # Use encoder to get reduced embeddings

        # Compile & Train
        autoencoder.compile(optimizer=Adam, loss='mse', metrics=['accuracy'])
        autoencoder.fit(self.original_embeddings, self.original_embeddings, epochs=40, batch_size=32)

        # Get Reduced Embeddings
        self.reduced_embeddings = encoder.predict(self.original_embeddings)
        print(self.reduced_embeddings.shape)  # Output: (1000, 256)
        self.model = autoencoder

        return self.reduced_embeddings
    
    ###
    # return model for further process such as visualize
    def getModel(self):
        return self.model
    
    def getErr(self):
        return self.err

    