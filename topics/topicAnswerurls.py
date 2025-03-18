from django.urls import path, include
from rest_framework import routers
from .TopicAnswerView import TopicAnswerView


router = routers.DefaultRouter()
router.register(r'', TopicAnswerView,basename='aswers')

urlpatterns = [
    path('question/', TopicAnswerView.as_view(), name='TopicAnswer'),
    #path('', include(router.urls)),
]

