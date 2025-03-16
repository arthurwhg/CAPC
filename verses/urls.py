from django.urls import path, include
from rest_framework import routers
from .VersesViewSet import VersesViewSet


router = routers.DefaultRouter()
router.register(r'', VersesViewSet,basename='topic')

urlpatterns = [
    path('vectors/', VersesViewSet.as_view(actions=({'get': 'get_verses_vectors_by_ids'}), name='Verses_embedding')),
    path('', VersesViewSet.as_view(actions=({'get': 'list'}), name='Verse_list')),
    path('', VersesViewSet.as_view(actions=({'get': 'get__verses_by_ids'}), name='Verses_by_ids')),
    #path('', include(router.urls)),
]

