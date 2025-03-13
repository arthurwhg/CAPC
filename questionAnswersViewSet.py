from rest_framework.decorators import action
from sqlalchemy import null
from .serializers import ErrorInfoSerializer
from .answerSerializer import AnswerSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import datetime
import json
import traceback

from llm.models import CommonQuestions, Answer, Comment

###
# Viewset for answers of a question API processes
# /question/pk/answers/ processes
#   Get   
#   Post
#   Delete
##

# category: Answers
class QuestionAnswersViewSet(viewsets.ViewSet):
    queryset = CommonQuestions.objects.all()
    serializer_class = AnswerSerializer

    # [Get]
    @swagger_auto_schema(
        responses={
            200: AnswerSerializer,
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        summary ="get all answers of a question",
        tags=['Question']
    )
    def list(self,request, pk=None, *args, **kwargs):
        print(f"finding answers for question with id {pk}")
        # ... (your logic)
        if pk is not None:
            question = self.queryset.get(id=int(pk))
            reAnswer = AnswerSerializer(question.get_answers(), many=True)  
            return Response(reAnswer.data, status=status.HTTP_200_OK, content_type='application/json')
        else:
            ErrorInfo ={'code': '400', 'detail': 'Bad Request'}
            return Response(ErrorInfo, status= status.HTTP_404_NOT_FOUND, content_type='application/json')

    # [Post]
    @swagger_auto_schema(
        request_body=AnswerSerializer,
        summary ="Add answers to a question",
        tags=['Question']
    )
    def create(self, request, pk=None, *args, **kwargs):
        # ... (your logic)
        answer = AnswerSerializer(request.body)
        question = self.queryset.get(id=int(pk))
        if not question.DoesNotExist:
            question.update_Answer(answer)
            reqanswer = AnswerSerializer(question.get_answers(), many=True)  
            return Response(reqanswer.data, status=status.HTTP_200_OK, content_type='application/json')
        else:
            ErrorInfo =  {'code': '404', 'detail': 'Question not found'}
            return Response(ErrorInfo, status= status.HTTP_404_NOT_FOUND, content_type='application/json')

    @swagger_auto_schema(
        summary ="Delte all answers of a question",
        tags=['Question']
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        None
