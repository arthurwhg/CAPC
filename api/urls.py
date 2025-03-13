from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .aboutViewSet import AboutViewSet, AboutViewSet2
from .questionsViewSet import QuestionsViewSet
from .questionCommentsViewSet import QuestionCommentsViewSet
from .questionAnswersViewSet import QuestionAnswersViewSet
from .questionViewSet import QuestionViewSet 
from .answerViewSet import AnswerViewSet
from .questionViewSet import QuestionViewSet
from .commentViewSet import CommentViewSet 
from .answerCommentsViewSet import AnswerCommentsViewSet
from .askViewSet import AskViewSet
from . import apiview

# URL Configuration using routers
router = DefaultRouter()
router.register(r'questions', QuestionsViewSet, basename='Questions')
#router.register(r'question/?<question_pk>/answers/', QuestionAnswersViewSet, basename='Question/answers')
#router.register(r'question/?<question_pk>/comments', QuestionCommentsViewSet, basename='comments')
router.register(r'question', QuestionViewSet, basename='question')
#router.register(r'question/?<question_pk>/answers/', QuestionAnswersViewSet, basename='answers')
router.register(r'answer', AnswerViewSet, basename='answer')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'ask', AskViewSet, basename='ask')
#router.register(r'answer/?<answer_pk>/comments', AnswerCommentsViewSet, basename='Answer/comment')
#router.register(r'question/?<question_pk>/comments', QuestionCommentsViewSet, basename='Questin/comments')
#router.register(r'comment/?<comment_pk>', CommentViewSet, basename='/comment')
router.register(r'abouts', AboutViewSet, basename='abouts')
router.register(r'about2', AboutViewSet2, basename='about2')
# router.register(r'ask', AskViewSet, basename='ask')

urlpatterns = [
    path('', apiview.index, name="index"),
    path('question/<int:pk>/answers/', QuestionAnswersViewSet.as_view(actions=({'get': 'list', 'post': 'create'})), name='question-answers'),
    path('answer/<int:pk>/comments/', AnswerCommentsViewSet.as_view(actions=({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='answer-comments')),
    path('question/<int:pk>/comments/', QuestionCommentsViewSet.as_view(actions=({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='answer-comments')),
    #path('question/?<question_pk>/rating/', QuestionOpsViewSet.as_view(actions={'post':"updateRating"})),
    # path('about/', AboutViewSet.as_view(actions={'get':'retrieve'}, name='about', description='About the API')),
    # path('ask/', AskViewSet.as_view(actions={'post':'ask'},name='ask', description='Ask a question')),
    path('', include(router.get_urls()))
]

#for url in router.urls:
#    print(url)
                                                                                                                                                                                                                                                                                                                                                                                    

