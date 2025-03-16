from django.urls import path, include
from rest_framework import routers
from .topicViewSet import TopicViewSet


router = routers.DefaultRouter()
router.register(r'', TopicViewSet,basename='topic')

urlpatterns = [
    path('<int:id>/vector/', TopicViewSet.as_view(actions=({'get': 'get_embedding'}), name='Topic_embedding')),
    #path('<int:id>/', TopicViewSet.as_view(actions=({'put': 'update'}), name='Topic_updating')),
    #path('similar', TopicViewSet.as_view(actions=({'get': 'get_similar_topics'}), name='Topic_similar')),
    path('', include(router.urls)),
]

