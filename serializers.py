from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from llm.models import Comment, CommonQuestions, Answer
import datetime

class ErrorInfoSerializer(serializers.Serializer):
    code = serializers.CharField()
    detail = serializers.CharField(required=False, allow_blank=True)


class ErrorInfoSerializer(serializers.Serializer):
    code = serializers.CharField()
    detail = serializers.CharField(required=False, allow_blank=True)

