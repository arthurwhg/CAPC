####
# this view set is designed to answer questions on topics
#
# 
#
##




from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from topics.models import Topic
from topics.topicSerializer import TopicSerializer

class AskedViewSet(viewsets.ViewSet):

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)  

    @swagger_auto_schema(
        operation_description="Ask a question on a topic",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'question': openapi.Schema(type=openapi.TYPE_STRING, description='Question to ask'),
            }
        ),
        responses={200: TopicSerializer(many=True)},
        operation_summary="Get topics by IDs",
        tags=["Topics"]
    )
    @action(detail=False, methods=['get'], url_path='')
    def ask(self, request):

        #1. get similar topics by question
        question = request.query_params.get('question', None)
        if not question:
            return Response({"error": "No question provided"}, status=400)
        print(f"question: {question}")
        #2. get verses by topics
        topics = []
        topicsQS = Topic.objects.filter(id__in=id_list).all()   

        #3. return topics and verses
        