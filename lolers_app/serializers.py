from rest_framework import serializers

from lolers_app.models import Players, GameData


class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = "__all__"


class GameDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameData
        fields = "__all__"
