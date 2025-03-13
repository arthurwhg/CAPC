from rest_framework import viewsets
from .models import Topic
from .topicSerializer import TopicSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
import traceback

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    # [post]
    # Get a question detail by ID/PK
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'topic': openapi.Schema(type=openapi.TYPE_STRING, description='Topic name')
            },
        ),
        responses={
            201: TopicSerializer, 
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
                    topic = TopicSerializer(new_topic, many=False)
                    return Response(topic.data, status=status.HTTP_201_CREATED, content_type='application/json')
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
        tags=["topic"],
    )  
    def get_embedding(self, request, id=None):
        #print(f"get_embedding {id}")
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


    # [put]
    # Get ids of similar topics by semantic search
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',  # Parameter name
                openapi.IN_QUERY,  # Location: query parameter
                type=openapi.TYPE_INTEGER,           
                required=True,
                description="ID of the tipic to update"  # A brief description
            )
        ],
        request_body=TopicSerializer,  # Define request body schema,  
        responses={ 
            200: openapi.Schema (
                    'content',  # Parameter name
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='Topic IDs'
                    ),
                    description='Topic IDs'),
            404: None, 
            500: None,
        },
        operation_summary="update a topic",
        tags=["topic"],
    )  
    def update(self, request, id=None, pk=None):
        print(f"update {id}")
        print(f"got pk: {pk}")
        if id is not None:
            topic = Topic.objects.get(pk=int(id))
            new_topic = json.loads(request.body.decode('utf-8'))
            if topic is not None:
                serializer = TopicSerializer(topic, data=new_topic, partial=True)  # Enable partial update
                if not serializer.is_valid():
                    print(serializer.error_messages)
                try:
                    if serializer.is_valid():
                        updated_instance = serializer.save()  # Calls update() in the serializer
                        return Response(TopicSerializer(updated_instance).data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)           
                except Exception as err:
                    #traceback.print_exc()
                    return Response({"code":500, "detail": "Internal Error"}, status=500, content_type='application/json')
            else:
                print(f"topic not found by id: {id}")
                return Response({"error": "Topic not found"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        else:
            return Response({"error": "Topic ID should be provided"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')