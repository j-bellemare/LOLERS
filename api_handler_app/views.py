from rest_framework import viewsets

from .models import (
    Players,
    GameData
)

from .serializers import (
    PlayersSerializer,
    GameDataSerializer
)


class PlayersViewSet(viewsets.ModelViewSet):
    queryset = Players.objects.all()
    serializer_class = PlayersSerializer


class GameDataViewSet(viewsets.ModelViewSet):
    queryset = GameData.objects.all()
    serializer_class = GameDataSerializer
