from django.db import models
from pgvector.django import VectorField
from langchain_openai import OpenAIEmbeddings
from django.utils import timezone
import os
from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(ROOT_DIR, '.env.production'))

class Verse(models.Model):
    id = models.AutoField(primary_key=True)
    version_name = models.CharField(max_length=255, null=True, blank=True)
    version_abbr = models.CharField(max_length=255, null=True, blank=True)
    testament_abbr = models.CharField(max_length=64, null=True, blank=True)
    testament_name = models.CharField(max_length=255, null=True, blank=True)
    book_name = models.CharField(max_length=255, null=True, blank=True)
    book_number = models.IntegerField(null=True, blank=True)
    chapter_number = models.IntegerField(null=True, blank=True)
    verse_number = models.IntegerField(null=True, blank=True)
    verse = models.CharField(max_length=1024, null=True, blank=True)
    cid = models.CharField(max_length=255, null=True, blank=False)
    topic = models.IntegerField(null=True, blank=True)
    labeled = models.CharField(max_length=16, null=True, blank=True)
    semantic = models.CharField(null=True, blank=True)
    tokens = models.IntegerField(null=True, blank=True)
    embedding = VectorField(dimensions=1536, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'verse'
        indexes = [
            models.Index(fields=['cid'], name='customId_index'),
            models.Index(fields=['topic'], name='topic_index'),
            models.Index(fields=['id'], name='id_index')
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small", api_key=self.api_key)

    def get_embedding(self,text):
        embedding_vector = self.embeddings_model.embed_query(text)
        #print(text)
        #print(embedding_vector[:10])
        #print(len(embedding_vector))
        return embedding_vector

    def __str__(self):
        return str(self.cid) + self.version_abbr + self.book_name+ str(self.chapter_number) + str(self.verse_number)
    

    def create(self, validated_data):
        if validated_data.get('verse') is None:
          validated_data['embedding'] = self.get_embedding(validated_data['verse'])
        return super().create(validated_data)

    def getVerseswithoutTopic(self):
        return Verse.objects.filter(topic__isnull=True)
    
    def removeEmbedding(self):
        self.embedding = None 
        return self
    
    def getVector(self):
        return self.embedding
    