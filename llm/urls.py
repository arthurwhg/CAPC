"""
URL configuration for llm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
#from api import views
import api.urls as api_urls
import topics.topicurls as topic_urls
import topics.topicsurls as topics_urls
import verses.urls as verses_urls
import topics.topicAnswerurls as TopicAnswerurls

swagger_info = openapi.Info(
    title="llm API Documentation",
    default_version='v1',
    description="API documentation for LLM service",
    contact=openapi.Contact(email="arthur@m4christ.com"),
)
# Define API metadata
schema_view = get_schema_view(                                                                                                                                                                                                                                                                                                                                                                                                       
    swagger_info,
    public=True,
    permission_classes=(permissions.AllowAny,),  # Publicly accessible API documentation
)

urlpatterns = [
    path("llm/api/v1/", include(api_urls)), # include api urls
    path("llm/api/v1/topic/", include(topic_urls)), # include topic urls
    path("llm/api/v1/topics/", include(topics_urls)), # include topics urls
    path("llm/api/v1/verses/", include(verses_urls)), # include
    path("llm/api/v1/topicanswer/", include(TopicAnswerurls)), # include
    path("admin/", admin.site.urls),
    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
