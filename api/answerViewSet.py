from rest_framework.decorators import action
from .serializers import ErrorInfoSerializer
from .questionSerializer import QuestionSerializer
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
# Viewset for answer API processes
# /answer/id/ processes
#   Get   
#   Post
#   Put
#   Delete
##

# category: Answer
class AnswerViewSet(viewsets.ViewSet):
    # [Get]
    @swagger_auto_schema(
        responses={
            200: QuestionSerializer, 
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        summary ="Get an answer by ID/PK",
        tags=['Answer']
    )
    def retrieve(self, request, pk):
        # ... (your logic)
        answer = Answer.find(pk)
        if answer is not null:
            if answer.updated():
                reqanswer = AnswerSerializer(answer, many=False)  
                return Response(reqanswer.data, status=status.HTTP_200_OK, content_type='application/json')
            else:
                errorInfo = {'code': '500', 'detail': answer.error_message()}
                return Response(errorInfo, status = status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
            ErrorInfo = {'code': '404', 'detail': 'Answer not found'}
            return Response(ErrorInfo, status= status.HTTP_404_NOT_FOUND, content_type='application/json')

    # [Put]
    @swagger_auto_schema(
        responses={
            200: QuestionSerializer, 
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        request_body=AnswerSerializer,
        summary ="Update an answer by ID/PK",
        tags=['Answer']
    )
    def update(self, request, pk=None):
        print("update mothod called!")
        # ... (your logic)
        #answer = Answer.find(pk)
        if pk is not None:
            #answer.update(answer)
            errorInfo = {'code': '501', 'detail': request.build_absolute_uri(), 'pk': pk, 'Method': 'update @ AnswerViewSet'}
            return Response(errorInfo, status = status.HTTP_501_NOT_IMPLEMENTED, content_type='application/json')
        else:
            ErrorInfo ={'code': '404', 'detail': 'Answer not found'}
            return Response(ErrorInfo, status= status.HTTP_404_NOT_FOUND, content_type='application/json')

    # [Delete]
    @swagger_auto_schema(
        responses={
            200: QuestionSerializer, 
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        summary ="delete an answer by ID/PK",
        tags=['Answer']
    )
    def destroy(self, request, pk=None):
        # ... (your logic)
        #answer = Answer.find(pk)
        if pk is not None:
#            answer.remove()
            errorInfo ={'code': '501', 'detail': request.build_absolute_uri(), 'pk': pk, 'Method': 'destroy @ AnswerViewSet'}
            return Response(errorInfo, status = status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
                errorInfo ={'code': '501', 'detail': "not implemented"}
                return Response(errorInfo, status = status.HTTP_501_INTERNAL_SERVER_ERROR, content_type='application/json')


    @action(detail=True, methods=['post'],url_path='updateRating')
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'rate',  # Parameter name
                openapi.IN_QUERY,  # Location: query parameter
                type=openapi.TYPE_INTEGER,           
                enum=[1,2,3,4,5],
                required=True,
            )
        ],
        responses={
            200: None, 
            404: ErrorInfoSerializer,
            501: ErrorInfoSerializer,
        },
        operation_summary="Update rating of an answer by id",
        content_type='application/json',
        response=QuestionSerializer,
        tags=["Answer"],
    )
    def updateRating(self, request, pk=None, rate=0):
        rat = request.query_params.get('rate')
        if pk is not None:
            errinfo={"code":"501","detail":request.build_absolute_uri(), "rate":rat, "pk":pk, "method": "updateRating"}
            return Response(errinfo, status=status.HTTP_501_NOT_IMPLEMENTED, content_type='application/json')
        else:
            errinfo={"code":"400","detail": "Bad Request"}
            return Response(errinfo, status=status.http_501_not_implemented, content_type='application/json')
