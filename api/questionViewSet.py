from rest_framework.decorators import action
from .serializers import  ErrorInfoSerializer
from .answerSerializer import AnswerSerializer
from .questionSerializer import QuestionSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
import traceback
from django.shortcuts import get_object_or_404

from llm.models import CommonQuestions, Answer, Comment

###
# ViewSet for question API processes
# /question/id/ processes
#   Get   
#   Post
#   Put
#   Delete
#   Post updateRating
##

class QuestionViewSet(viewsets.ViewSet):
    queryset = CommonQuestions.objects
    serializer_class = QuestionSerializer

    # [post]
    # Get a question detail by ID/PK
    @swagger_auto_schema(
        request_body=QuestionSerializer,
        responses={
            201: QuestionSerializer, 
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },
        operation_summary="Create a new question",
        tags=["Question"],
    )
    def create(self, request, pk=None):
       # ...
       if ( pk == None ):
            if request.method == 'POST':
                try:
                    request_data = request.body.decode('utf-8')
                    requestData = json.loads(request_data)
                    req = QuestionSerializer(data=requestData, many=False)
                    if req.is_valid(raise_exception=True):
                        new_question = req.save()
                        print(new_question)
                        requestion = QuestionSerializer(new_question, many=False)
                        return Response(requestion.data, status=status.HTTP_201_CREATED, content_type='application/json')
                    else:
                        errorinfo = {"code":"400","detail":req.errors}
                        return Response(errorinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')                            
                except Exception as err:
                    traceback.print_exc()
                    errorinfo = {"code":"400","detail":str(err)}
                    return Response(errorinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')  
       else:
           errorinfo = {"code":"400","detail":"Bad Request"}
           return Response(errorinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    # [put] 
    @swagger_auto_schema(
        request_body=QuestionSerializer,
        responses={
            200: QuestionSerializer, 
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },
        operation_summary="Update a question by ID",
        tags=["Question"],
    )
    def update(self, request,  pk=None):
       print(f"Got update for  & {pk}")
       # ...
       if pk is not None:
        try:
            question = self.queryset.get(id=int(pk))
            if question is not None:
                request_data = request.body.decode('utf-8')
                print(request_data)
                requestData = json.loads(request_data)
                #requestData.pop('answers', None)
                #request_data = bitstring.bit_string.decode('uft-8')
                #request_data = json.dumps(requestData)
                #print(requestData)
                serializer = QuestionSerializer(question, data=requestData, partial=True)
                if serializer.is_valid():
                    new_question = serializer.save()
                    #new_question = self.serializer_class.update(question, requestData)
                    print(new_question)
                    requestion = QuestionSerializer(new_question, many=False)
                    return Response(requestion.data, status=status.HTTP_200_OK, content_type='application/json')
                else:
                    errorinfo = {"code":"400","detail":serializer.errors}
                    return Response(errorinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')   
            else:
                errorinfo = {"code":"404","detail":"No found"}
                return Response(errorinfo,status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        except Exception as err:
            errorinfo = {"code":"404","detail":"No found,"+str(err)}
            traceback.print_exc()
            print(errorinfo)
            return Response(errorinfo,status=status.HTTP_404_NOT_FOUND, content_type='application/json')
       else:
           errorinfo = {"code":"400","detail":"Bad Request"}
           return Response(errorinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


    # [get]
    # Get a question detail by ID/PK
    @swagger_auto_schema(
        responses={
            200: QuestionSerializer, 
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },
        operation_summary="Retrieve a question by ID",
        tags=["Question"],
    )
    def retrieve(self, request, pk=None):
       print(f"Got retrieve for & {pk}")
       # ...
       if ( pk != None ):
            question = CommonQuestions.objects.get(id=int(pk))
            if question.id == int(pk):
                req = QuestionSerializer(question, many=False)
                return Response(req.data, status=status.HTTP_200_OK, content_type='application/json')
            else:
                errinfo = {'code':'404', 'Description':"No found"}
                return Response(errinfo, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
       else:
           errorinfo = {"code":"400","detail":"Bad Request"}
           return Response(errorinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    #[Delete]
    # Get a question detail by ID/PK
    @swagger_auto_schema(
        responses={
            200: QuestionSerializer, 
            404: ErrorInfoSerializer, 
            500: ErrorInfoSerializer
        },
        operation_summary="Delete a question by ID",
        tags=["Question"],
    )
    def destroy(self, request, pk=None):
       # ...
        idlist = request.body.decode('utf-8') 
        if idlist is not  None & idlist.length > 0:
            try:
                for i in idlist:
                    print(f"Deleting record by {int(i)}.", )
                #question = CommonQuestions.objects.get(id=int(pk))
                #question.delete()
                errinfo = {'code':'200', 'Description':f'question {pk} has been removed'}
                return Response(errinfo, status=status.HTTP_200_OK, content_type='application/json')    
            except Exception as err:
                errinfo = {'code':'404', 'Description':"No found," + str(err)}
                return Response(errinfo, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        else:
           errorinfo = {"code":"400","detail":"Bad Request"}
           return Response(errorinfo, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


# /question/pk/rating/  
    @action(detail=True, methods=['put'],url_path='updateRating')
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'rate',  # Parameter name
                openapi.IN_QUERY,  # Location: query parameter
                type=openapi.TYPE_INTEGER,           
                required=True,
                description="array of ids such as 1,2,3,4,5"
            )
        ],
        responses={
            200: None, 
            404: ErrorInfoSerializer,
        },
        operation_summary="Update rating of a questions by id",
        content_type='application/json',
        response=QuestionSerializer,
        tags=["Question"],
    )
    def updateRating(self, request, pk=None ):

        question = get_object_or_404(CommonQuestions, pk=pk)
        new_rating = request.GET.get("rate")

        if new_rating is None or not isinstance(int(new_rating), int):
            return Response({"error": "Invalid rating"}, status=status.HTTP_400_BAD_REQUEST)

        question.rating = int(new_rating)
        question.save()

        #question2 = get_object_or_404(CommonQuestions, pk=pk)
        #print(f"Updated rating by {question2.rating}")
        errinfo={}
        return Response(errinfo, status=status.HTTP_200_OK, content_type='application/json')

# /question/pk/publish/  
    @action(detail=True, methods=['put'],url_path='publish')
    @swagger_auto_schema(
        responses={
            200: None, 
            400: ErrorInfoSerializer,
            404: ErrorInfoSerializer,
        },
        operation_summary="publish a question",
        content_type='application/json',
        response=QuestionSerializer,
        tags=["Question"],
    )
    def publish(self, request, pk=None ):

        question = get_object_or_404(CommonQuestions, pk=pk)

        if question is None:
            return Response({"404": "Question Not found"}, status=status.HTTP_404_NOT_FOUND)

        question.status = 'published'
        question.save()

        errinfo={}
        return Response(errinfo, status=status.HTTP_200_OK, content_type='application/json')

# /question/pk/unpublish/  
    @action(detail=False, methods=['put'],url_path='unpublish')
    @swagger_auto_schema(
        responses={
            200: QuestionSerializer, 
            404: ErrorInfoSerializer,
            400: ErrorInfoSerializer,
        },
        operation_summary="Unpublish a question",
        content_type='application/json',
        tags=["Question"],
    )
    def unpublish(self, request, pk=None ):

        question = get_object_or_404(CommonQuestions, pk=pk)

        if question is None:
            return Response({"404": "Question Not found"}, status=status.HTTP_404_NOT_FOUND)

        question.status = 'asked'
        question.save()

        errinfo={}
        return Response(errinfo, status=status.HTTP_200_OK, content_type='application/json')

# /question/languages/  
    @action(detail=False, methods=['get'],url_path='languages')
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Languages list",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'code': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of a language"),
                            'detail': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the language"),
                        },
                    ),
                ),
            ), 
        },
        operation_summary="options of languages",
        content_type='application/json',
        tags=["Question"],
    )
    def languages(self, request ):
        langs = [
            {"code": "EN", "detail": "English"},
            {"code": "ZH", "detail": "Simplified-Chinese"},
            {"code": "CN", "detail": "Traditional-Chinese"},
            {"code": "FR", "detail": "French"}
            ]

        return Response(langs, status=status.HTTP_200_OK, content_type="application/json")

# /question/status/  
    @action(detail=False, methods=['get'],url_path='status')
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Status options: asked, published",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'code': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of a status"),
                            'detail': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the status"),
                        },
                    ),
                ),
            ), 
        },
        operation_summary="options of status",
        content_type='application/json',
        tags=["Question"],
    )
    def status(self, request ):
        states = [
            {"code": "asked", "detail": "The question was asked but not published yet"},
            {"code": "published", "detail": "A questions has been published"},
            ]

        return Response(states, status=status.HTTP_200_OK, content_type="application/json")

# /question/agents/  
    @action(detail=False, methods=['get'],url_path='agents')
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Agents options: Pastor, Preist",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'code': openapi.Schema(type=openapi.TYPE_INTEGER, description="code of agent"),
                            'detail': openapi.Schema(type=openapi.TYPE_STRING, description="name of the agent"),
                        },
                    ),
                ),
            ), 
        },
        operation_summary="Agents",
        content_type='application/json',
        tags=["Question"],
    )
    def agents(self, request ):
        states = [
            {"code": "Pastor", "detail": "An agent of pastor"},
            {"code": "Preist", "detail": "An agent of preist"},
            ]

        return Response(states, status=status.HTTP_200_OK, content_type="application/json")
