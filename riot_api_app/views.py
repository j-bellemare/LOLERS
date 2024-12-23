from rest_framework.decorators import api_view
from rest_framework.response import Response
from lolers_app.models import GameData, Players
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import GetMatchesSerializer
from rest_framework import status
import requests
from dotenv import main
import os

riot_base_url = "https://americas.api.riotgames.com/lol/"


@swagger_auto_schema(
    method="post",
    request_body=GetMatchesSerializer,
    responses={
        200: openapi.Response(
            description="Get matchs ids by Player",
        ),
        400: openapi.Response(description="invalid Input"),
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
