from django.urls import re_path
from riot_api_app.views import get_matches

urlpatterns = [
    re_path(r"^api/riot_api_app/", get_matches, name="get_matches")
]
