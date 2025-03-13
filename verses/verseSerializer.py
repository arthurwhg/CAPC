from rest_framework import serializers
from verses.models import Verse
from langchain_openai import OpenAIEmbeddings
#from django.db.models.functions import CosineDistance
#from django.db.models import F

class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},  # Allow `id` to be writable for update operations.
            'topic': {'required': False},
            'embedding': {'required': False},
            'book': {'required': False},
            'video': {'required': False},
            'version_abbr': {'required': False},
            'version_name': {'required': False},
            'testament_abbr': {'required': False},
            'testament_name': {'required': False},
            'book_name': {'required': False},
            'book_number': {'required': False},
            'chapter_number': {'required': False},
            'verse_number': {'required': False},
            'verse': {'required': False},
            'customId': {'required': False},
            'topic':{'required': False},
            'semantic':{'required': False},
            'tokens':{'required': False},
            'embedding':{'required': False}
        }

    def update_embedding(self, instance, new_embedding):
        """
        Updates the embedding for the given verse instance with a provided embedding.
        """
        if new_embedding is not None:
            instance.embedding = new_embedding  # Assign the new embedding
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({"error": "New embedding is required for update."})