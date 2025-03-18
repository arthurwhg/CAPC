from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .verseSerializer import VerseSerializer
from .models import Verse

class VersesViewSet(viewsets.ViewSet):
    
    @swagger_auto_schema(
        operation_description="Retrieve a set of verses by a list of IDs, vector is not included",
        manual_parameters=[
            openapi.Parameter(
                'ids',
                in_=openapi.IN_QUERY,
                description="Comma-separated list of verse IDs",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'k',
                in_=openapi.IN_QUERY,
                description="number of verses to be returned",
                type=openapi.TYPE_INTEGER,
                default=5,
                required=False
            )
        ],
        responses={200: VerseSerializer(many=True)},
        operation_summary="Get verses by IDs",
        tags=["Verses"]
    )
    @action(detail=False, methods=['get'], url_path='byIds')
    def get_verses_by_ids(self, request):
        """
        Fetch multiple verses by their IDs.
        """
        id_list = request.query_params.get('ids', None)
        tids = [int(i) for i in id_list.split(',')]
        print(f"ids: {tids}")
        
        if not id_list:
            return Response({"error": "No IDs provided"}, status=400)
        
        # Convert comma-separated string to a list of integers
        try:
            id_list = [int(i) for i in id_list.split(',')]
        except ValueError:
            return Response({"error": "Invalid ID format. Provide comma-separated integers."}, status=400)

        # Query database for matching verses
        verses = []
        versesQS = Verse.objects.filter(id__in=id_list).all()
        if versesQS.count() > 0:
            for verse in versesQS:
                verses.append(verse.removeEmbedding())   
        else:
            return Response({"error": f"Verse with ID {id} not found"}, status=404)
        #verses = Verse.objects.filter(id__in=id_list).all()
        serializer = VerseSerializer(verses, many=True)
        
        return Response(serializer.data, status=200)
    

    @swagger_auto_schema(
        method='get',
        operation_description="Retrieve a set of verses vectors by a list of IDs",
        manual_parameters=[
            openapi.Parameter(
                'ids',
                in_=openapi.IN_QUERY,
                description="Comma-separated list of verse IDs",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: VerseSerializer(many=True)},
        operation_summary="Get verses vectors by verses IDs",
        tags=["Verses"]
    )
    @action(detail=False, methods=['get'], url_path='')
    def get_verses_vectors_by_ids(self, request):
        """
        Fetch multiple verses by their IDs.
        """
        id_list = request.query_params.get('ids', None)
        
        if not id_list:
            return Response({"error": "No IDs provided"}, status=400)
        
        # Convert comma-separated string to a list of integers
        try:
            id_list = [int(i) for i in id_list.split(',')]
        except ValueError:
            return Response({"error": "Invalid ID format. Provide comma-separated integers."}, status=400)

        # Query database for matching verses
        versesQS = Verse.objects.filter(id__in=id_list).all()
        vectors = []
        if versesQS.count() > 0:
            for verse in versesQS:
                vectors.append(verse.getVector())   
        else:
            return Response({"error": f"Verse with ID {id} not found"}, status=404)
        #serializer = VerseSerializer(verses, many=True)
        
        return Response(vectors, status=200)
    
    @swagger_auto_schema(
        operation_description="Retrieve a set of verses by topic numbers, vector is not included",
        manual_parameters=[
            openapi.Parameter(
                'topic_ids',
                in_=openapi.IN_QUERY,
                description="Comma-separated list of topic IDs",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'k',
                in_=openapi.IN_QUERY,
                description="number of verses to be returned",
                type=openapi.TYPE_INTEGER,
                default=10,
                required=False
            )
        ],
        responses={200: VerseSerializer(many=True)},
        operation_summary="Get verses by IDsi",
        tags=["Verses"]
    )
    @action(detail=False, methods=['get'], url_path='bytopic')
    def get_verses_by_topics(self, request):
        id_list = request.query_params.get('topic_ids', None)
        k = int(request.query_params.get('k', 10))
        
        try:
            tids = [int(i) for i in id_list.split(',')]
        except ValueError:
            return Response({"error": "Invalid ID format. Provide comma-separated integers."}, status=400)

        verses = []
        versesQS = Verse.objects.filter(topic__in=tids).all()[:k]
        if versesQS.count() > 0:
            for verse in versesQS:
                verses.append(verse.removeEmbedding())   
        else:
            return Response({"error": f"Verse with ID {id} not found"}, status=404)
        #verses = Verse.objects.filter(id__in=id_list).all()
        serializer = VerseSerializer(verses, many=True)
        return Response(serializer.data, status=200)
