from rest_framework import serializers
from topics.models import Topic
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
#from django.db.models.functions import CosineDistance
#from django.db.models import F

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(ROOT_DIR, '.env.production'))

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'topic', 'embedding','book','video']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},  # Allow `id` to be writable for update operations.
            'topic': {'required': False},
            'embedding': {'required': False},
            'book': {'required': False},
            'video': {'required': False}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # load_dotenv(os.path.join(ROOT_DIR, '.env.production'))
        apikey = os.getenv("OPENAI_API_KEY")
        self.embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=apikey)

    def get_embedding(self,text):
        embedding_vector = self.embeddings_model.embed_query(text)
        #print(text)
        #print(embedding_vector[:10])
        #print(len(embedding_vector))
        return embedding_vector

    def create(self, validated_data):
        print(validated_data)
        validated_data['embedding'] = self.get_embedding(validated_data['ntopic'])
        return super().create(validated_data)

    def get_similar_topics(self,text,k=3):
        query_embedding = self.get_embedding(text)
        
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

        topics = Topic.objects.raw(
            "SELECT id, embedding FROM topic ORDER BY embedding <=> %s LIMIT %s",
            [embedding_str, str(k)]
        )

        #print(query_embedding[:5])
        #topics = Topic.objects.all().order_by("embedding <=>" query_embedding)[:k]
        #topics = topics.objects.annotate(similarity=1- CosineDistance(F('embedding'), query_embedding)).order_by("-similarity")[:k]

        ids =[topic.id for topic in topics]
        return ids

    def update(self, instance, validated_data):
        """
        Custom update method for partial updates.
        - Updates only provided fields.
        - Ensures instance is saved properly.
        """
        print(f"Validated Data in Update: {validated_data}")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # Update each field
        print(validated_data)
        instance.embedding = self.get_embedding(validated_data['topic'])

        instance.save()  # Save the updated instance
        return instance