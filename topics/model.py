from verses.models import Verse
from topics.models import Topic


class TopicAnswer():
    def __init__(self, answer):
        self.answer = answer
        self.verses = []
        self.topics = None

    def __str__(self):
        return self.answer
    
    def setVerse(self, verse):
        self.verses =verse

    def setTopics(self, topics):
        self.topics = topics

    def addVerse(self, verse):
        self.verses.append(verse)

