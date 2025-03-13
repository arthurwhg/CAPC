from rest_framework.decorators import action
from sqlalchemy import null
from .serializers import  ErrorInfoSerializer
from .answerSerializer import AnswerSerializer
from .commentSerializer import CommentSerializer
from .questionSerializer import QuestionSerializer
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
# Viewset for answer.comments API processes
# /answer/id/comments processes
#   Get   
#   Post
#   Delete
##

class AnswerCommentsViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    CommentSerializer = CommentSerializer()
    answerqueryset = Answer.objects.all()
    answerSerializer = AnswerSerializer()

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of comments",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Comment ID"),
                            'author': openapi.Schema(type=openapi.TYPE_STRING, description="Author's name"),
                            'content': openapi.Schema(type=openapi.TYPE_STRING, description="Comment text"),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Creation timestamp"),
                        },
                    ),
                ),
            ),
            404: ErrorInfoSerializer,
            400: ErrorInfoSerializer,
        },
        operation_summary="Get all comments of an Answer",
        content_type='application/json',
        summary="Get all comments of an answer",
        tags=['Comments']
    )
    def list(self, request, pk=None):
        # 
        if pk is not None:
            answer = self.queryset.get(id=int(pk))
            if answer is not None:
                comments = answer.get_comments()
                reqcomment = CommentSerializer(comments, many=True)    
                if reqcomment.is_valid(raise_exception=True): 
                    AnswerSerializer.update(answer, request.body)
                    return Response(reqcomment.data, status=status.HTTP_200_OK, content_type="application/Json")
                else:
                    errorInfo = {'code': '400', 'detail': reqcomment.error_messages()}
                    return Response(errorInfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
            else:
                errorInfo = {'code': '404', 'detail': 'Answer not found'}
                return Response(errorInfo, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        else:
            errorInfor = {'code': '404', 'detail': 'Answer not found'}
            return Response(errorInfor, status=status.HTTP_404_NOT_FOUND, content_type='application/json')        

    @swagger_auto_schema( 
        responses={
            200: AnswerSerializer,
            404: ErrorInfoSerializer,
            400: ErrorInfoSerializer,
        },
        operation_summary= "add comments to an answer",
        tags=['Comments'],
        request_body=CommentSerializer,
    )
    def create(self, request, pk=None)   :
        # ... (your logic)
        if answer is not None:
            answer = Answer.find(id=int(pk))
            ncomments = CommentSerializer(request.body, many=True)
            self.commentserializer.save(answer, ncomments)
            if reqanswer.is_valid(raise_exception=True):
                errorinfo = {'code': '400', 'detail': 'Bad Request'}
                return Response(errorinfo.data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
            else:
                answer.add_comments(ncomments)
                if answer.updated():
                    reqanswer = AnswerSerializer(answer, many=False)  
                    return Response(reqanswer.data, status=status.HTTP_200_OK, content_type='application/json')
                else:
                    errorinfo = {'code': '500', 'detail': 'Internal Error'}  
                    return Response(errorinfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
            errorInformation = {'code': '404', 'detail': 'Answer not found'}
            return Response(errorInformation, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

    #@action(detail=False, methods=['delete'])
    @swagger_auto_schema( 
        responses={
            200: None,
            404: ErrorInfoSerializer,
            400: ErrorInfoSerializer,
        },
        operation_summary= "delete comments of an answer",
        tags=['Comments'],
    )
    def destroy(self, request, pk=None):
        # ... (your logic)
        return Response(None, status=status.HTTP_200_OK, content_type='application/json')




# class AskViewSet(viewsets.ViewSet):
#     @swagger_auto_schema(
#         request_body=QuestionSerializer,
#         responses={
#             201: AnswerSerializer(many=True), 
#             404: ErrorInfoSerializer, 
#             500: ErrorInfoSerializer
#         },  # Correct response is an array of Answer objects
#         operation_summary="Ask a question",  # Provide a summary
#         tags=["Question"]   # Add tags to group endpoints
#     ) 
#     def list(request):
#         # ... your logic
#         pass
#         return Response({'test':'test'}, status=status.HTTP_201_CREATED, content_type='application/json')
