#from myapp.models import Memory
from langchain_openai import OpenAIEmbeddings

# Initialize embeddings
api_key = "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"
embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=api_key)

def store_memory(text):
    embedding_vector = embeddings_model.embed_query(text)
    print(embedding_vector[:10])
    print(len(embedding_vector))
    return embedding_vector


store_memory("And God said, Let there be light: and there was light")



