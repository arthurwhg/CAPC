from rest_framework.decorators import action
from .serializers import ErrorInfoSerializer
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


# /about/id/ process
class AboutViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        responses={
            201: None, 
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        operation_summary="return version information about APIs",  # Provide a summary
        tags=["about"],   # Add tags to group endpoints
        content_type='application/json'
    )
    def list(self,request, *args, **kwargs):
        # ... (your logic)
        print(args)
        print(kwargs)
        print(request.method)
        pk = request.method
        res = {'version': pk, 'description': 'API list for the LLM service'}
        return Response(res, status=status.HTTP_200_OK, content_type='application/json')


    @swagger_auto_schema(
        responses={
            201: None, 
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        operation_summary="create version information about APIs",  # Provide a summary
        tags=["about"],   # Add tags to group endpoints
        content_type='application/json'
    )
    def create(self,request,question_pk=None, *args, **kwargs):
        # ... (your logic)
        pk = request.method
        res = {'version': question_pk, 'description': 'API for the LLM service'+request.method}
        return Response(res.data, status=status.HTTP_200_OK, content_type='application/json')


class AboutViewSet2(viewsets.ViewSet):
    @swagger_auto_schema(
        responses={
            201: None, 
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        operation_summary="update version information about APIs",  # Provide a summary
        tags=["about"],   # Add tags to group endpoints
        content_type='application/json'
    )
    def retrieve(self,request, pk=None, *args, **kwargs):
        # ... (your logic)
        print(args)
        print(kwargs)
        print(request.path.split('/'))
        pkp = request.method
        res = {'version': pk, 'description': 'Get API for the LLM service:'+pkp}
        return Response(res, status=status.HTTP_200_OK, content_type='application/json')


    @swagger_auto_schema(
        responses={
            201: None, 
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        operation_summary="update version information about APIs",  # Provide a summary
        tags=["about"],   # Add tags to group endpoints
        content_type='application/json'
    )
    def update(self,request, pk=None, *args, **kwargs):
        # ... (your logic)
        print(args)
        print(kwargs)
        print(request.path.split('/'))
        pkp = request.method
        res = {'version': pk, 'description': 'update API for the LLM service:'+pkp}
        return Response(res, status=status.HTTP_200_OK, content_type='application/json')


    @swagger_auto_schema(
        responses={
            201: None, 
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },  # Correct response is an array of Answer objects
        operation_summary="Destroy version information about APIs",  # Provide a summary
        tags=["about"],   # Add tags to group endpoints
        content_type='application/json'
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        # ... (your logic)
        print(args)
        print(kwargs)
        print(request.method)
        res = {'version': pk, 'description': 'destroy API for the LLM service:' + request.method}
        return Response(res, status=status.HTTP_200_OK, content_type='application/json')
