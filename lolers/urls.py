"""
URL configuration for lolers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view_lolers = get_schema_view(
    openapi.Info(title="API Lolers", default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
    urlconf="lolers_app.urls",
)
schema_view_riot_api_app = get_schema_view(
    openapi.Info(title="Riot API Caller", default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
    urlconf="riot_api_app.urls",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("lolers_app.urls")),
    re_path(
        r"^swagger/lolers/?$",
        schema_view_lolers.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("", include("riot_api_app.urls")),
    re_path(
        r"^swagger/riot_api_app/?$",
        schema_view_riot_api_app.with_ui("swagger", cache_timeout=0),
        name="schema-sagger-ui",
    )
]
