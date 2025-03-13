from sklearn.decomposition import PCA
import umap
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Model

class Embedding():

    def __init__(self):
        super()
        # Example: Original embeddings (N samples, 1536 dimensions)
        self.original_embeddings = np.random.rand(1000, 1536)  # Replace with your actual data
        self.reduced_embeddings = None 
        self.input_dim = 1536
        self.reduced_dim = 256



    def ReduceDim(self,model, embedding, n_components= 256):
        self.original_embeddings = np.array(embedding)
        # Ensure embedding is 2D: (samples, features)
        if self.original_embeddings.ndim == 1:
            self.original_embeddings = self.original_embeddings.reshape(1, -1)
            self.input_dim = self.original_embeddings.shape[0]

        self.reduced_dim = n_components
        if model == 'PCA':
            return self.PCAReduceDim(embedding, n_components)
        elif model == 'UMAP':
            return self.UMAPReduceDim(embedding, n_components)
        elif model == 'AutoEncoder':
            return self.AutoEncoder(embedding, n_components)
        else:
            return None

    def PCAReduceDim(self,embedding, n_components= 256):

            # Check shape before PCA
            print(f"Embedding shape before PCA: {self.original_embeddings.shape}")  

            # Reduce dimensions to 256
            pca = PCA(n_components=256)
            self.reduced_embeddings = pca.fit_transform(self.original_embeddings)

            # Check shape before PCA
            print(f"Embedding shape after PCA: {self.reduced_embeddings.shape}")  

            return(self.reduced_embeddings)

    def UMAPReduceDim(self,embedding, n_components= 256):
        # Reduce to 256 dimensions
        umap_model = umap.UMAP(n_components=256)
        self.reduced_embeddings = umap_model.fit_transform(self.original_embeddings)
        return(self.reduced_embeddings)
    
    def AutoEncoder(self, embedding, n_components=256):
        # Define Autoencoder Model
        input_layer = layers.Input(shape=(self.input_dim,))
        encoded = layers.Dense(512, activation='relu')(input_layer)
        encoded = layers.Dense(self.reduced_dim, activation='relu')(encoded)

        decoded = layers.Dense(512, activation='relu')(encoded)
        decoded = layers.Dense(self.input_dim, activation='sigmoid')(decoded)

        autoencoder = Model(input_layer, decoded)
        encoder = Model(input_layer, encoded)  # Use encoder to get reduced embeddings

        # Compile & Train
        autoencoder.compile(optimizer='adam', loss='mse')
        autoencoder.fit(self.original_embeddings, self.original_embeddings, epochs=10, batch_size=32)

        # Get Reduced Embeddings
        self.reduced_embeddings = encoder.predict(self.original_embeddings)
        print(self.reduced_embeddings.shape)  # Output: (1000, 256)

        return self.reduced_embeddings