import os

import requests
from dotenv import main
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
import time

from lolers_app.models import GameData

from .serializers import GetMatchesSerializer, GetMatchDataSerializer, GetPlayerScoreSerializer, GetTeamsSerializer
from .utils import calculate_score

riot_base_url = "https://americas.api.riotgames.com/lol/"


@swagger_auto_schema(
    method="post",
    request_body=GetMatchesSerializer,
    responses={
        200: openapi.Response(
            description="Get matchs ids by Player",
        ),
        400: openapi.Response(description="Invalid Input"),
    },
)
@api_view(["POST"])
def get_matches(request):
    """
    Get Matches
    ---
    parameters:
        - name: puuid
          in: body
          type: string
          required: true
        - name: queue
          in: body
          type: int
          required: true
        - name: count
          in: body
          type: int
          required: true
    """
    if request.method == "POST":
        serializer = GetMatchesSerializer(data=request.data)

        if serializer.is_valid():
            puuid = serializer.validated_data["puuid"]
            queue = serializer.validated_data["queue"]
            count = serializer.validated_data["count"]
            _ = main.load_dotenv(override=True)
            api_key = os.getenv("api_key")
            response = requests.get(
                f"{riot_base_url}match/v5/matches/by-puuid/{puuid}/ids?queue={queue}&start=0&count={count}&api_key={api_key}",
            )
            if response.status_code == 200:
                return Response(response.json())
            else:
                return Response("did not work")

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Error: Not a POST Request", status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    request_body=GetMatchDataSerializer,
    responses={
        200: openapi.Response(
            description="Get match data",
        ),
        400: openapi.Response(description="Invalid Input"),
    },
)
@api_view(["POST"])
def get_match_data(request):
    """
    Get Match Data
    ---
    parameters:
        - name: puuid
          in: body
          type: string
          required: true
        - name: matchId
          in: body
          type: string
    """
    if request.method == "POST":
        serializer = GetMatchDataSerializer(data=request.data)

        if serializer.is_valid():
            puuid = serializer.validated_data["puuid"]
            match_id = serializer.validated_data["match_id"]
            _ = main.load_dotenv(override=True)
            api_key = os.getenv("api_key")
            response = requests.get(
                f"{riot_base_url}match/v5/matches/{match_id}?api_key={api_key}",
            )
            if response.status_code == 200:
                all_game_data = response.json()
                player_data = {}
                all_data = []
                for player in all_game_data["info"]["participants"]:
                    if player["puuid"] == puuid:
                        player_data.update({
                            "assists": player["assists"],
                            "damageSelfMitigated": player["damageSelfMitigated"],
                            "deaths": player["deaths"],
                            "goldEarned": player["goldEarned"],
                            "kills": player["kills"],
                            "totalDamageDealtToChampions": player["totalDamageDealtToChampions"],
                            "totalDamageShieldedOnTeammates": player["totalDamageShieldedOnTeammates"],
                            "totalDamageTaken": player["totalDamageTaken"],
                            "totalHeal": player["totalHeal"],
                            "totalHealsOnTeammates": player["totalHealsOnTeammates"],
                            "timeCCingOthers": player["timeCCingOthers"],
                            "win": player["win"]
                        }),
                    else:
                        data = {}
                        data["assists"] = player["assists"]
                        data["damageSelfMitigated"] = player["damageSelfMitigated"]
                        data["deaths"] = player["deaths"]
                        data["goldEarned"] = player["goldEarned"]
                        data["kills"] = player["kills"]
                        data["totalDamageDealtToChampions"] = player["totalDamageDealtToChampions"]
                        data["totalDamageShieldedOnTeammates"] = player["totalDamageShieldedOnTeammates"]
                        data["totalDamageTaken"] = player["totalDamageTaken"]
                        data["totalHeal"] = player["totalHeal"]
                        data["totalHealsOnTeammates"] = player["totalHealsOnTeammates"]
                        data["timeCCingOthers"] = player["timeCCingOthers"]
                        all_data.append(data)

                score = calculate_score(player_data, all_data)

                return Response(score)
            else:
                return Response("did not work", status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Error: Not a POST Request", status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    request_body=GetPlayerScoreSerializer,
    responses={
        200: openapi.Response(
            description="Get match data",
        ),
        400: openapi.Response(description="Invalid Input"),
    },
)
@api_view(["POST"])
def get_player_score(request):
    if request.method == "POST":
        serializer = GetPlayerScoreSerializer(data=request.data)

        if serializer.is_valid():
            puuid = serializer.validated_data["puuid"]
            game_ids = GameData.objects.filter(player=puuid).order_by('id').values_list('game_id', flat=True)

            url = "http://127.0.0.1:8000/api/riot_api_app/get_matches"
            data = {
                "puuid": puuid,
                "queue": 450,
                "count": 30
            }
            response = requests.post(url, json=data)

            games = []
            for game in response.json():
                if game not in game_ids:
                    games.append(game)
            num_new_games = len(games)

            if GameData.objects.filter(player=puuid).count() > 30:
                games_to_delete = GameData.objects.filter(player=puuid).order_by('id')[:num_new_games]
                games_to_delete.delete()

            new_entires = []
            for game in games:
                url = "http://127.0.0.1:8000/api/riot_api_app/get_match_data"
                data = {
                    "puuid": puuid,
                    "match_id": game
                }
                response = requests.post(url, json=data)
                new_entires.append(GameData(player_id=puuid, game_id=game, player_game_score=response.json()))

            GameData.objects.bulk_create(new_entires)

            player_score = GameData.objects.filter(player=puuid).aggregate(
                total_score=Sum('player_game_score')
            )['total_score'] or 0

            return Response(player_score)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Error: Not a POST Request", status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(
    method="post",
    request_body=GetTeamsSerializer,
    responses={
        200: openapi.Response(
            description="Get teams",
        ),
        400: openapi.Response(description="Invalid Input"),
    },
)
@api_view(["POST"])
def get_teams(request):
    if request.method == "POST":
        serializer = GetTeamsSerializer(data=request.data)

        if serializer.is_valid():
            players = serializer.validated_data["players"][0]
            avg_player_score = 0
            count = len(players)
            for player in players:
                avg_player_score += player[1]

            avg_player_score = avg_player_score/count
            player_advantage = avg_player_score * .1
            
            players_sorted = sorted(players, key=lambda x: x[1], reverse=True)
            team1, team2 = [], []
            score1, score2 = 0, 0

            for player, score in players_sorted:
                strength1 = score1 + len(team1) * player_advantage
                strength2 = score2 + len(team2) * player_advantage

                if strength1 <= strength2:
                    team1.append(player)
                    score1 += score
                else:
                    team2.append(player)
                    score2 += score

            teams = {
                "Crugs": {"players": team1, "total_score": score1},
                "Raptors": {"players": team2, "total_score": score2}
            }

            return Response(teams)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Error: Not a POST Request", status=status.HTTP_400_BAD_REQUEST)
