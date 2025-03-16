from rest_framework import viewsets
from .models import Topic
from .topicSerializer import TopicSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
import traceback
import os
from dotenv import load_dotenv


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)

    @swagger_auto_schema(
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Topic ID'),
                    'topic': openapi.Schema(type=openapi.TYPE_STRING, description='Topic name'),
                    'embedding': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT), description='Topic embedding'),
                    'book': openapi.Schema(type=openapi.TYPE_STRING, description='Book name'),
                    'video': openapi.Schema(type=openapi.TYPE_STRING, description='Video URL')
                }),
            404: None, 
            500: None
        },
        operation_summary="get topic by id",
        tags=["topic"],
    )
    def retrieve(self, request, pk=None):
        print(f"retrieve by {pk}")
       # ...
        if pk is not None:
            try:            
                topic = self.get_queryset().get(pk=int(pk))
                if topic:
                    TS = TopicSerializer(topic, many=False)
                    return Response(TS.data, status=status.HTTP_201_CREATED, content_type='application/json')
                else:
                    errorinfo = {"code":"404","detail":f"not found by id {pk}"}
                    return Response(errorinfo, status=status.HTTP_404_NOT_FOUND, content_type='application/json')                            
            except Exception as err:
                errorinfo = {"code":"500","detail":str(err)}
                return Response(errorinfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')  
        else:
            errorinfo = {"code":"400","detail":"please privde an valid id"}
            return Response(errorinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json') 

    # [post]
    # create a topic
    @swagger_auto_schema(
        request_body=TopicSerializer,
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Topic ID'),
                    'topic': openapi.Schema(type=openapi.TYPE_STRING, description='Topic name'),
                    'embedding': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT), description='Topic embedding'),
                    'book': openapi.Schema(type=openapi.TYPE_STRING, description='Book name'),
                    'video': openapi.Schema(type=openapi.TYPE_STRING, description='Video URL')
                }),
            404: None, 
            500: None
        },
        operation_summary="Create a new topic",
        tags=["topic"],
    )
    def create(self, request):
       # ...
        request_data = request.body.decode('utf-8')
        requestData = json.loads(request_data)
        if requestData:
            try:            
                topicSerializer = TopicSerializer(data=requestData, many=False)
                if topicSerializer.is_valid(raise_exception=True):
                    new_topic = topicSerializer.save()
                    #topic = TopicSerializer(new_topic, many=False)
                    return Response(new_topic, status=status.HTTP_201_CREATED, content_type='application/json')
                else:
                    errorinfo = {"code":"400","detail":topicSerializer.errors}
                    return Response(errorinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')                            
            except Exception as err:
                errorinfo = {"code":"400","detail":str(err)}
                return Response(errorinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')  
        else:
            errorinfo = {"code":"400","detail":"Invalid request data"}

    # [get]
    # Get embedding of a topic
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',  # Parameter name
                openapi.IN_QUERY,  # Location: query parameter
                type=openapi.TYPE_INTEGER,           
                required=True,
                description="Id of the topic to get its embedding"  # A brief description
            )
        ],    
        responses={ 
            200: openapi.Schema (
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_FLOAT,
                        description='Topic vector'
                    ),
                    description='Topic embedding'),
            404: None, 
            500: None,
        },
        operation_summary="Get vector of a topic",
        tags=["topic"],
    )  
    def get_embedding(self, request, id=None, pk=None):
        print(f"get_embedding by {id} or pk: {pk}")
        if id is not None:
            try:
                topic = self.get_queryset().get(pk=id)
                print(topic)
                if topic is None:
                    errorinfo = {"code":"404","detail":"Topic not found"}
                    return Response(None,status=status.HTTP_404_NOT_FOUND)
                else:
                    #print(f"return 200ok {topic.embedding[:10]}")
                    return Response(topic.embedding, status=status.HTTP_200_OK, content_type='application/json')
            except Topic.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except Exception as err:
                errorinfo = {"code":"400","detail":str(err)}
                return Response(errorinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        else:
            errorinfo = {"code":"400","detail":"Invalid Topic ID provided"}
            return Response(errorinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


