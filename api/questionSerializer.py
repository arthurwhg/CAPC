from rest_framework import serializers
from .answerSerializer import AnswerSerializer
from llm.models import CommonQuestions, Answer, Comment
import datetime
from .commentSerializer import CommentSerializer

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(
        many=True, 
        read_only=False,
    )
    date = serializers.DateTimeField(format="%d/%m/%Y", required=False)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = CommonQuestions
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},  # Allow `id` to be writable for update operations.
            'answers': {'read_only': False},
            'comments': {'read_only': False}
        }


    # override create method 
    # handling child Answers creation                                                                                                                                                                                                                                                                                                                                                                                                             
    def create(self, validated_data):
        print("creating records ...")
        #print("Validated Data:", validated_data)  # Debug validated data
        #print(type(validated_data))
        #print("keys: ", validated_data.keys())
        #print("Answers:", validated_data['answers'])
        #answers_list = validated_data['answers']
        answers_list = validated_data.pop('answers', [])
        comments_list = validated_data.pop('comments',[])
        #print("Answers Data:", answers_data)  # Debug nested answers data
        #print(type(validated_data))
        #print(validated_data)
        
        print("creating records ...1")
        question_tp = CommonQuestions.objects.create(**validated_data)
        print("Question Created:", question_tp)  # Confirm question creation

        # Create the question instance
        question_created = CommonQuestions.objects.create(**validated_data)
        
        # Create associated answers
        if answers_list is not None:
            for answer_data in answers_list:
                answer_created=Answer.objects.create(question=question_created, **answer_data)
        
        # Create comments associated
        if comments_list is not None:
            for comment_data in comments_list:
                comment_created = Comment.objects.create(question=question_created, **comment_data)

        return question_created

    # Overrided default update method to handle relationship of Answers
    def update(self, instance, validated_data):
        #print("Updating Question...")

        # Extract nested answers data before updating the question
        answers_data = validated_data.pop('answers', None)

        comments_data = validated_data.pop('comments',None)

        # Update the `CommonQuestions` instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        setattr(instance, 'date', datetime.datetime.now())
        instance.save()
        print("Updated Question:", instance)

        if answers_data is not None:
            self.update_answers(instance, answers_data)

        if comments_data is not None:
            print(f"updating comments {len(comments_data)}")
            self.update_comments(instance, comments_data)

        return instance

    def update_answers(self, instance, answers_data):
        """
        Manages updates to the Answer model.
        - Updates existing answers
        - Creates new answers
        - Deletes answers that were removed
        """
        existing_answers = {answer.id: answer for answer in instance.answers.all()}
        new_answers = []

        for answer_data in answers_data:
            answer_id = answer_data.get('id', None)

            if answer_id and answer_id in existing_answers:
                # Update existing answer
                answer_instance = existing_answers.pop(answer_id)
                for key, value in answer_data.items():
                    setattr(answer_instance, key, value)
                setattr(answer_instance, 'date', datetime.datetime.now())
                answer_instance.save()
                #print(f"Updated Answer: {answer_instance}")
            else:
                # Create new answer
                answer_data.pop('id', None)  # Ensure no ID conflicts
                new_answers.append(Answer(question=instance, **answer_data))

        # Bulk create new answers for efficiency
        if new_answers:
            Answer.objects.bulk_create(new_answers)
            #print(f"Created {len(new_answers)} new answers.")

        # Delete answers that were not included in the update request
        for answer in existing_answers.values():
            answer.delete()
            print(f"Deleted Answer: {answer}")

        #print("Answers update completed.")
   
    def update_comments(self, instance, comments_data):
        """
        Manages updates to the Comment model.
        - Updates existing coments
        - Creates new comments
        - Deletes comments that were removed
        """
        existing_comments = {comment.id: comment for comment in instance.get_comments()}
        new_comments = []

        for comment_data in comments_data:
            # print(type(comment_data))
            # print(comment_data)
            # print(comment_data.get('id', None))
            comment_id = comment_data.get('id', None)
            if comment_id and comment_id in existing_comments:
                # Update existing answer
                comment_instance = existing_comments.pop(comment_id)
                print(f"updating comment {comment_instance.id}")
                for key, value in comment_data.items():
                    setattr(comment_instance, key, value)
                setattr(comment_instance, 'date', datetime.datetime.now())
                comment_instance.save()
                #print(f"Updated Answer: {answer_instance}")
            else:
                # Create new comment
                print(f"create new comment")
                comment_data.pop('id', None)  # Ensure no ID conflicts
                new_comments.append(Comment(question=instance, **comment_data))

        # Bulk create new answers for efficiency
        #print(f"create new comments {len(new_comments)}")
        if new_comments:
            Comment.objects.bulk_create(new_comments)
            #print(f"Created {len(new_answers)} new answers.")

        # Delete answers that were not included in the update request
        if existing_comments is not None:
            for comment in existing_comments.values():
                comment.delete()
                #print(f"Deleting Coments: {comment.id}")

        #print("Answers update completed.")

   
    # update rating of a question ****************
    def update_question_rating(self, question_id, new_rating):
        """
        Updates the rating of a question.
        - `question_id`: ID of the `CommonQuestions` instance.
        - `new_rating`: New rating value.
        """
        try:
            question = CommonQuestions.objects.get(id=question_id)
            question.rating = new_rating
            question.save()
            return question
        except CommonQuestions.DoesNotExist:
            raise serializers.ValidationError({"detail": "Question not found"})
        
