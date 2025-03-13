from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from llm.models import Comment, Answer
from django.contrib.auth.models import User
import datetime
from  .commentSerializer import CommentSerializer

class AnswerSerializer(serializers.ModelSerializer): 
    comments = CommentSerializer(many=True, read_only=False, required=False)
    content = serializers.JSONField(read_only=False)
    date = serializers.DateTimeField(format="%d/%m/%Y", required=False, read_only=False)
    class Meta:
        model = Answer
        fields = ['id', 'question', 'content', 'date', 'rating', 'user', 'comments']
        read_only_fields = ['id', 'date', 'comments']  # Prevent direct modification of comments here

    def create(self, validated_data):
        """
        Handle answer creation.
        - Creates a new answer.
        - Does not allow direct creation of comments (handled separately).
        """
        return Answer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing answer.
        - Updates `content`, `rating`, and `user` fields.
        - Does not modify `date` or `comments` directly.
        """
        instance.content = validated_data.get('content', instance.content)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.user = validated_data.get('user', instance.user)

        instance.save()
        return instance
    
    def add_comment(self, answer_id, comment_data):
     """
      Add a new comment to an answer.
      - Accepts `answer_id` to link the comment.
      - Supports replies (`parent_comment`).
     """
     try:
            answer = Answer.objects.get(id=answer_id)
            comment_data['answer'] = answer  # Associate comment with the answer
            new_comment = Comment.objects.create(**comment_data)
            return new_comment
     except Answer.DoesNotExist:
            raise serializers.ValidationError({"detail": "Answer not found"})


    def update_comment(self, comment_id, comment_data):
        """
        Update an existing comment.
        - Only allows modifying `content`, `by`, and `rating`.
        """
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.content = comment_data.get('content', comment.content)
            comment.by = comment_data.get('by', comment.by)
            comment.rating = comment_data.get('rating', comment.rating)
            comment.save()
            return comment
        except Comment.DoesNotExist:
            raise serializers.ValidationError({"detail": "Comment not found"})
