from django.urls import path, include
from rest_framework import routers
from .topicsViewSet import TopicsViewSet


router = routers.DefaultRouter()
router.register(r'', TopicsViewSet,basename='topics')

urlpatterns = [
    #path('similar', TopicsViewSet.as_view(actions=({'get': 'get_similar_topics'}), name='Topic_similar')),
    path('', include(router.urls)),
]

