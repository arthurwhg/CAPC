from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .askSerializer import AskSerializer
from .questionSerializer import QuestionSerializer
from .serializers import ErrorInfoSerializer
from drf_yasg.utils import swagger_auto_schema
import json
import traceback
class AskViewSet(viewsets.ViewSet):
    """ViewSet to handle 'Ask' requests from users."""

# POST /ask/
    @swagger_auto_schema(
        request_body=AskSerializer,
        responses={
            200: QuestionSerializer, 
            400: ErrorInfoSerializer,
            404: ErrorInfoSerializer,
        },
        operation_summary="ask a question",
        content_type='application/json',
        tags=["Ask"],
    )
    def create(self, request):
        """Process an ask request and save it to CommonQuestion."""
        print("asking a question .......")
        requested_data = request.body.decode('utf-8')
        print("got data", requested_data)
        serializer = AskSerializer(data=json.loads(requested_data))
        if serializer.is_valid(raise_exception=True):
          try:
              print("deserialized", serializer.data)
              asked = json.loads(requested_data)
              print(asked)
              # 1. get asks
              question = serializer.create(asked)
              print(f"question: {question}")
              print(f"asked: {asked}")
              print(type(asked))
              for key in asked.keys():
                print(f"{key}: {asked[key]}")
              print(asked["agent"])
              # 2. Initiate an agent 
              if asked["agent"] == 'Pastor':
                print("GOt question for a pastor")
                agent = None
              if asked["agent"] == 'Prist': 
                print("Got a question for a prister")
                agent = None

              # 3. ask question and get answers 
              #question = agent.ask(asked)
              print("asking question to agent")
              # 4. save the question and answers
              # question_to_save = serializer.create_question_from_ask(asked)
              # question_to_save.save()
              print("saving question and answers")

              # 5. resposne answers
              print("respond asks")
              question["answers"] = []
              requestion = QuestionSerializer(question, many=False)
              return Response(requestion.data, status=status.HTTP_201_CREATED, content_type='application/json')
              
          except Exception as err:
            traceback.print_exc()
            errinfo = {'code': '500', 'detail': str(err)}
            return Response(errinfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
    
