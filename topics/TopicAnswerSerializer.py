from rest_framework import serializers
from verses.verseSerializer import VerseSerializer
from topics.topicSerializer import TopicSerializer

class TopicAnswerSerializer(serializers.Serializer):
    verses = VerseSerializer(many=True)
    #topics = TopicSerializer(many=False)

    
    
