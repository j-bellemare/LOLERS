from django.urls import re_path
from riot_api_app.views import get_matches, get_match_data, get_player_score, get_teams

urlpatterns = [
    re_path(r"^api/riot_api_app/get_matches", get_matches, name="get_matches"),
    re_path(r"^api/riot_api_app/get_match_data", get_match_data, name="get_match_data"),
    re_path(r"^api/riot_api_app/get_player_score", get_player_score, name="get_player_score"),
    re_path(r"^api/riot_api_app/get_teams", get_teams, name="get_teams"),
]
