from django.db import models
from pgvector.django import VectorField

class Topic(models.Model):
    class Meta:
        db_table = 'topic'

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    topic = models.CharField(max_length=255, null=False)
    embedding = VectorField(dimensions=1536)
    book  = models.CharField(max_length=255, null=True, blank=True)
    video = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.topic
    

    def create(self, validated_data):
        validated_data['embedding'] = self.generate_embedding(validated_data['topic'])
        return super().create(validated_data)

    def generate_embedding(self, text):
        # Placeholder function: Replace with actual embedding logic
        return [0.0] * 1536  # Example embedding of dimension 1536
    
    def removeEmbedding(self):
        self.embedding = []
        return self
