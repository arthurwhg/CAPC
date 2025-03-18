
from rest_framework.views import APIView
from .model import TopicAnswer
from .topicSerializer import TopicSerializer
from .TopicAnswerSerializer import TopicAnswerSerializer
from verses.verseSerializer import VerseSerializer
from verses.models import Verse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
#from rest_framework.decorators import action
#from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
import traceback
import os


class TopicAnswerView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a set of verses by a list of IDs, vector is not included",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'question': openapi.Schema(type=openapi.TYPE_STRING, description='Question to ask'),
            }
        ),
        responses={200: TopicAnswerSerializer(many=False)},
        operation_summary="Get verses by IDs",
        tags=["TopicQuestion"]
    )
    def post(self, request):
        question = request.data.get('question', None)
        if not question:
            return Response({"error": "No question provided"}, status=400)
        print(f"question: {question}")
        topics = []
        tids = TopicSerializer().get_similar_topics(question,2)
        print(f"found!: {tids}")
        if len(tids) == 0:
            return Response({"error": f"Similar Topic for the question {question} not found. try another question!"}, status=404)

        verses = []
        versesQS = Verse.objects.filter(topic__in=tids).all()[:10]
        if versesQS.count() > 0:
            for verse in versesQS:
                verse.embedding = []
                verses.append(verse)

        #TA= TopicAnswer(question)
        ta ={}
        vSerializer = VerseSerializer(instance=verses, many=True)
        tSerializer = TopicSerializer(instance=topics, many=True)
        topics = tSerializer.data
        ta['topics'] = tids
        ta['verses'] = vSerializer.data   
        # taSerializer = TopicAnswerSerializer(instance=TA, many=False)
        print(ta)
        #TA.setQuestion(question)

        #taSerializer = TopicAnswerSerializer(instance=TA, many=False)
        #print(vSerializer.data)
        #print(f"final: {taSerializer.data} ")
        return Response(ta, status=200)



