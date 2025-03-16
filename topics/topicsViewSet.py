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


class TopicsViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)

    # [post]
    # create a topic
    @swagger_auto_schema(
        request_body=TopicSerializer(many=False),
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
        tags=["topics"],
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
                        description='Topic embedding'
                    ),
                    description='Topic embedding'),
            404: None, 
            500: None,
        },
        operation_summary="Get embedding of a topic",
        tags=["topics"],
    )  
    def get_embedding(self, request, id=None):
        #print(f"get_embedding {id}")
        pass

    # [get]
    # Get ids of similar topics by semantic search
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='topic',  # Parameter name
                in_=openapi.IN_QUERY,  # Location: query parameter
                type=openapi.TYPE_STRING,           
                required=True,
                description="content of a topic"  # A brief description
            ),
            openapi.Parameter(
                name='k',  # Parameter name
                in_=openapi.IN_QUERY,  # Location: query parameter
                type=openapi.TYPE_INTEGER,           
                required=False,
                default=3,
                description="number of matched topics to be returned. default is 3"  # A brief description
            )
        ],
        responses={ 
            200: openapi.Schema (
                    name='ids',  # Parameter name
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='Topic IDs'
                    ),
                    description='Topic IDs'),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Not Found"), 
            500: openapi.Response(description="Internal Server Error"),
        },
        operation_summary="get a topic list similar to the given content",
        tags=["topics"],
    )  
    @action(detail=False, methods=['get'], url_path='similar')
    def get_similary_topics(self, request):
        topic_content = request.query_params.get("topic", None)
        k = request.query_params.get("k", 3)
        TS = TopicSerializer()
        if topic_content is not None:
            topicIds = TS.get_similar_topics(topic_content, k)
            if len(topicIds) > 0:
                return Response(topicIds, status=status.HTTP_200_OK, content_type='application/json')
            else:
                return Response({"error": "No similar topics found"}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        else:
            return Response({"error": "Topic content should be provided"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')