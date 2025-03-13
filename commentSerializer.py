from rest_framework import serializers
from django.apps import apps
from llm.models import Comment

class ChildCommentSerializer(serializers.ModelSerializer):
    """ ✅ Serializer for child (nested) comments """
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'date', 'by', 'children', 'rating']
        read_only_fields = ['id', 'children']  # ✅ Prevents modification of children

    
class CommentSerializer(serializers.ModelSerializer):
    """ ✅ Serializer for parent comments including nested replies """

    children = ChildCommentSerializer(many=True, read_only=True, required=False)  # ✅ Properly references nested comments
    #answer = AnswerSerializer(many=False, read_only=True, required=False)
    #question = QuestionSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'answer_id', 'question_id', 'content', 'date', 'by', 'children', 'rating']
        read_only_fields = ['id', 'children']  # ✅ Prevents modification of children

    def create(self, validated_data):
        """
        ✅ Handles nested comment creation
        - If `parent_comment` is provided, it's a reply (child comment).
        - Otherwise, it's a top-level comment.
        """
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        ✅ Updates an existing comment.
        - Only allows modification of `content`, `by`, and `rating`.
        """
        instance.content = validated_data.get('content', instance.content)
        instance.by = validated_data.get('by', instance.by)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance