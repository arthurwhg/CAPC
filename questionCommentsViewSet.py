from rest_framework import serializers
from .answerSerializer import AnswerSerializer
from .questionSerializer import QuestionSerializer
from .serializers import ErrorInfoSerializer
from .commentSerializer import CommentSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from drf_yasg import openapi
import datetime
import json
import traceback
from llm.models import CommonQuestions, Answer, Comment
import datetime


# /question/pk/comments/ processes
class QuestionCommentsViewSet(viewsets.ViewSet):
    queryset = CommonQuestions.objects.all()
    serializer_class = CommentSerializer

    # [Get]
    @swagger_auto_schema(
        responses={
                200: openapi.Response(
                    description="Comments of the question",
                     schema=openapi.Schema(                     
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id" : openapi.Schema(type=openapi.TYPE_INTEGER, description="Comment ID"),
                                "answer_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Answer ID"),
                                "question_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Question ID"),
                                "content": openapi.Schema(type=openapi.TYPE_STRING, description="Comment text"),
                                "date": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Creation timestamp"),
                                "by": openapi.Schema(type=openapi.TYPE_STRING, description="Author's name"),
                                "rating": openapi.Schema(type=openapi.TYPE_INTEGER, description="Rating of the comment"),
                                }
                            ),                
                        ),
                    ),
                404: ErrorInfoSerializer, 
                501: ErrorInfoSerializer
            },  # Correct response is an array of Answer objects
        operation_summary ="get all comments of a question",
        tags=['Comments']
    )
    def list(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            question = self.queryset.get(id=int(pk))
            if question is not None:
                comlist = Comment.objects.filter(question=question)
                if comlist is not None:
                    comments = CommentSerializer(comlist, many=True)  
                    return Response(comments.data, status=status.HTTP_200_OK, content_type='application/json')
                else:
                    errinfo= {'code': '404', 'detail': 'Question not found'}
                    return Response(errinfo,status=status.HTTP_404_NOT_FOUND, content_type='application/json')  
            else: 
                errinfo= {'code': '404', 'detail': 'Question not found'}
                return Response(errinfo,status=status.HTTP_404_NOT_FOUND, content_type='application/json')  
        else:
            errinfo= {'code': '400', 'detail': "Bad Reqeust."}
            return Response(errinfo,status=status)


    # [post]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'content': openapi.Schema(type=openapi.TYPE_STRING, description="Text content of the comment"),
                    'by': openapi.Schema(type=openapi.TYPE_STRING, description="Author of the comment"),
                    'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description="Rating of the comment (optional)"),
                },
                required=['content', 'by']  # Required fields
            ),
        ),
        responses={
            200: QuestionSerializer, 
            404: ErrorInfoSerializer, 
            501: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        operation_summary="Add commentss of a question",
        tags=['Comments']
    )
    def create(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            question = self.queryset.get(id=int(pk))                
            if question is not None:
                try:
                    newComments_data = request.body.decode('utf-8')
                    newComments = json.loads(newComments_data)
                    print(newComments)
                    if newComments is not None:
                        comments = CommentSerializer(data=newComments, many=True)
                        if comments.is_valid(raise_exception=True):
                            comments.save( question=question)
                            reqQuestion = QuestionSerializer(question, many=False)
                            return Response(reqQuestion.data, status=status.HTTP_200_OK, content_type='application/json')
                except Exception as err:
                        errinfo= {'code': '400', 'detail': str(err)}
                        return Response(errinfo,status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
   

            errinfo= {'code': '501', 'detail': request.build_absolute_uri(),'pk': pk,'Method': 'create @ AnswerCommentsViewSet'}
            return Response(errinfo,status=status.HTTP_501_NOT_IMPLEMENTED, content_type='application/json')
        else:
            errinfo= {'code': '400', 'detail': request.build_absolute_uri()}
            return Response(errinfo,status=status)

    @action(detail=False, methods=['delete'])
    @swagger_auto_schema(
        responses={
            200: QuestionSerializer, 
            404: ErrorInfoSerializer, 
            501: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        summary ="delete all comments of a question",
        tags=['Comments']
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        return Response(None, status=status.HTTP_501_NOT_IMPLEMENTED, content_type='application/json')