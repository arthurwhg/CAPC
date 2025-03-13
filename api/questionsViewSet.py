from rest_framework.decorators import action
from sqlalchemy import null
from .serializers import ErrorInfoSerializer
from .answerSerializer import AnswerSerializer
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
# ViewSet for question list API processes
# /questions/ processes
#   Get   
#   Post
#   Delete
##

# ViewSets with Swagger Decorators
class QuestionsViewSet(viewsets.ModelViewSet):

    queryset = CommonQuestions.objects.prefetch_related('answers')
    serializer_class = QuestionSerializer
    renderer_classes = [JSONRenderer]  # Force JSON response

    #[get]
    # Get all questions published
    @swagger_auto_schema(
        responses={
            200: QuestionSerializer(many=True), 
            404: ErrorInfoSerializer,
            500: ErrorInfoSerializer,
        },
        operation_summary="Get all questions",
        content_type='application/json',
        response=QuestionSerializer,
        tags=["Questions"],
    )
    def list(self, request):
        # ... (your logic as befoqre)
        try:
            # questions = [question for question in self.queryset.values()]

            questions = self.queryset.all()
            if questions.exists() :
                if (questions.count() == 1):
                    # single question responded
                    #print("Answers:",questions[0])
                    #self.queryset.first().answers.all()
                    question = questions.first()
                    answers = question.get_answers()
                    requestions = QuestionSerializer(question, many=False)
                else:
                    # multiple questions responded
                    requestions = QuestionSerializer(questions, many=True) 
                    return Response(requestions.data, status=status.HTTP_200_OK, content_type='application/json')
            else:
                    errinfo ={'code': '404', 'detail': 'no found'}
                    return Response(errinfo, status=status.HTTP_404_NOT_FOUND, content_type='application/json') 
        except Exception as err:
            print(err.__traceback__)
            errinfo = {'code': '500', 'detail': str(err)}
            return Response(errinfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ids',  # Parameter name
                openapi.IN_QUERY,  # Location: query parameter
                description="id array",
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER),
                required=True,
            )
        ],
        responses={
            200: None, 
            404: ErrorInfoSerializer,
            501: ErrorInfoSerializer,
        },
        operation_summary="Delete questions by id",
        content_type='application/json',
        response=QuestionSerializer,
        tags=["Questions"],
    )
    def destroy(self, request, pk=None):
        if pk is not None:
            question = self.queryset.get(id=int(pk))
            question.delete()
            errinfo = {'code': '200', 'detail': f"question {pk} was removed"}
            return Response(errinfo, status=status.HTTP_200_OK, content_type='application/json')
        else:
            errinfo = {'code': '400', 'detail': request.build_absolute_uri()}
            return Response(errinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        None

    # [post]
    @swagger_auto_schema(
        request_body=QuestionSerializer,  # Define request body schema
        responses={
            201: AnswerSerializer(many=True),
            404: ErrorInfoSerializer,
            500: ErrorInfoSerializer
        },  # Correct response schema
        operation_summary="Create a new question",
        tags=["Questions"],
    )
    def create(self, request):
       # ... (your logic)
        # update to get a question from DB by PK
        print("Got Post Request...")
        question = QuestionSerializer(request.body)
        if question.is_valid(raise_exception=False):
            #dbquestion = CommonQuestions()
            #dbquestion.from_model(question.data) # to be implemented
            print("Saving started ...")
            question.save()
            if question.saved():
                return Response(question, status=status.HTTP_201_CREATED, content_type='application/json')
            else:
                errinfo ={'code': '400', 'detail': question.error_messages}
                return Response(errinfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        else:
                errinfo ={'code': '400', 'detail': 'Bad Request!'}
                return Response(errinfo, status=status.HTTP_400_Bad_Request, content_type='application/json')        

