from django.db import models
from django.contrib.auth.models import User

class CommonQuestions(models.Model):
    id = models.AutoField(primary_key=True) 
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    language = models.CharField(
        choices=(
            ('English', 'English'), 
            ('CN', 'Simplified-Chinese'), 
            ('ZH', 'Traditional-Chinese'), 
            ('French', 'French')
        ),
        default = 'ZH',
        max_length=10,
        blank=True,
        null=True
    )
    bible = models.TextField(blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    rating = models.IntegerField(default=0, null=True)
    agent = models.CharField(
        choices=(
            ('Pastor','Pastor'),
            ('Priest','Priest')
        ),
        default = 'Priest',
        max_length=255,
    )
    status = models.CharField(
        choices=(
            ('asked','asked'),
            ('published','published')
        ),
        default = 'asked',
        max_length=64,
    )


    def __str__(self):
        return self.title

    def get_answers(self):
        return self.answers.all()

    def get_comments(self):
        return self.comments.all()

    # addAnswer, removeAnswer, updateAnswer, UpdateQuestion, DeleteQuestion are handled by Django ORM


class Answer(models.Model):
    id = models.AutoField(primary_key=True) 
    question = models.ForeignKey('CommonQuestions', related_name='answers', on_delete=models.CASCADE,null=True)
    content = models.JSONField()
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    rating = models.IntegerField(default=0, blank=True, null=True)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, null=True) # Consider a ForeignKey to a User model if you have authentication.

    def __str__(self):
        return f"Answer to {self.question.title}"

    def get_comments(self):
        return self.comments.all()   
    

    # addComment, removeComment, updateComment, UpdateAnswer are handled by Django ORM



class Comment(models.Model):
    id = models.AutoField(primary_key=True) 
    answer = models.ForeignKey(Answer, related_name='comments', on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(CommonQuestions, related_name='comments', on_delete=models.CASCADE, null=True)    
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    by = models.CharField(max_length=255,blank=True, null=True) # Consider a ForeignKey to a User model if you have authentication.
    parent_comment = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)  # Self-referential relationship for nested comments
    rating = models.IntegerField(default=0, null=True)


    def __str__(self):
        if self.parent_comment is not None:
            return f"Comment on comment {self.parent_comment.id}"
        elif self.answer is not None:
            return f"Comment on answer {self.answer.id}"
        #elif self.answeris is not None:
        #    return f"Coment on question {self.answer.question.id}"
            

    def get_comments(self):
        #return self.child_comments.all()
        return self.children.all()


    # updateComment, deleteComment are handled by Django ORM

class test (models.Model):
    id = models.AutoField(primary_key=True) 
    desc = models.TextField(max_length=255)
