from django.urls import path, include
from rest_framework import routers
from .topicsViewSet import TopicsViewSet


router = routers.DefaultRouter()
router.register(r'', TopicsViewSet,basename='Topics')

urlpatterns = [
    path('similar', TopicsViewSet.as_view(actions=({'get': 'get_similar_topics'}), name='Topics')),
    path('byids/', TopicsViewSet.as_view(actions=({'get': 'get_topics_by_ids'}), name='Topics')),
    #path('', include(router.urls)),
]

