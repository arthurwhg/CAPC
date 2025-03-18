from django.urls import path, include
from rest_framework import routers
from .VersesViewSet import VersesViewSet


router = routers.DefaultRouter()
router.register(r'', VersesViewSet,basename='Verses')

urlpatterns = [
    path('vectors/', VersesViewSet.as_view(actions=({'get': 'get_verses_vectors_by_ids'}), name='Verses_embedding')),
    path('', VersesViewSet.as_view(actions=({'get': 'list'}), name='Verse_list')),
    path('byids/', VersesViewSet.as_view(actions=({'get': 'get_verses_by_ids'}), name='Verses_by_ids')),
    path('bytopics/', VersesViewSet.as_view(actions=({'get': 'get_verses_by_topics'}), name='Verses_by_topics')),
    #path('', include(router.urls)),
]

