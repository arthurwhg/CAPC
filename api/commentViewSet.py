from rest_framework.decorators import action
from sqlalchemy import null
from .serializers import ErrorInfoSerializer
from .commentSerializer import CommentSerializer
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
# Viewset for comments of comment API processes
# /comment/pk/comments
#   Get   
#   Post
#   Put
#   Delete
##

class CommentViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # [get]
    @swagger_auto_schema(
        responses={
            200: CommentSerializer, 
            404: ErrorInfoSerializer, 
            501: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        summary="delete a comment",
        tags= ['Comment']
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            comment = self.queryset.get(id=int(pk))
            print("get", comment)
            if comment is not null:
                reqcomment = CommentSerializer(comment, many=False)  
                return Response(reqcomment.data, status=status.HTTP_200_OK, content_type='application/json')
            else:
                errorInfo = {'code': '404', 'detail': 'Not Found' }
                return Response(errorInfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
            errorInfo ={'code': '400', 'detail': 'Bad Request'}
            return Response(errorInfo.data, status=status.htto_400_Bad_Request,content_type= 'application/json')


    # [post]
    @swagger_auto_schema(
        responses={
            200: CommentSerializer, 
            404: ErrorInfoSerializer, 
            501: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        summary="delete a comment",
        tags= ['Comment']
    )
    def create(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            errorInfo = {'code': '501', 'detail': request.build_absolute_uri(), 'pk': pk, 'Method': 'created @ CommentOpsViewSet' }
            return Response(errorInfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
            errorInfo ={'code': '404', 'detail': 'Comment not found'}
            return Response(errorInfo.data, status=status.htto_400_Bad_Request,content_type= 'application/json')

    # [put]
    @swagger_auto_schema(
        responses={
            200: CommentSerializer, 
            404: ErrorInfoSerializer, 
            501: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        summary="delete a comment",
        tags= ['Comment']
    )
    def update(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            errorInfo = {'code': '501', 'detail': request.build_absolute_uri(), 'pk': pk, 'Method': 'created @ CommentOpsViewSet' }
            return Response(errorInfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
            errorInfo ={'code': '404', 'detail': 'Comment not found'}
            return Response(errorInfo.data, status=status.htto_400_Bad_Request,content_type= 'application/json')

    # [delete]
    @swagger_auto_schema(
        responses={
            200: CommentSerializer, 
            404: ErrorInfoSerializer, 
            501: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        summary="delete a comment",
        tags= ['Comment']
    )
    def destroy(self, request, pk):
        if pk is not None:
            errorInfo = {'code': '501', 'detail': request.build_absolute_uri(), 'pk': pk, 'Method': 'destroy @ CommentOpsViewSet' }
            return Response(errorInfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
            errorInfo ={'code': '404', 'detail': 'Comment not found'}
            return Response(errorInfo.data, status=status.htto_400_Bad_Request,content_type= 'application/json')


    # [post]/comment/pk/rating/rate/
    @swagger_auto_schema(
        responses={
            200: CommentSerializer, 
            404: ErrorInfoSerializer, 
            501: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        summary="update rating of a comment",
        tags= ['Comment']
    )
    def updateRating(self, request, pk, rate=1):
        if pk is not None:
            errorInfo = {'code': '501', 'detail': request.build_absolute_uri(), 'pk': pk, 'Method': 'destroy @ CommentOpsViewSet' }
            return Response(errorInfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
            errorInfo ={'code': '400', 'detail': 'Bad Request'}
            return Response(errorInfo.data, status=status.htto_400_Bad_Request,content_type= 'application/json')
        None
