from rest_framework import serializers
from lolers_app.models import Players


class GetMatchesSerializer(serializers.Serializer):
    puuid = serializers.CharField(max_length=255)
    queue = serializers.IntegerField()
    count = serializers.IntegerField(min_value=1)

    def validate_puuid(self, value):
        if not Players.objects.filter(puuid=value).exists():
            raise serializers.ValidationError(f"puuid '{value}' does not exist")
        return value


class GetMatchDataSerializer(serializers.Serializer):
    puuid = serializers.CharField(max_length=255)
    match_id = serializers.CharField(max_length=255)

    def validate_puuid(self, value):
        if not Players.objects.filter(puuid=value).exists():
            raise serializers.ValidationError(f"puuid '{value}' does not exist")
        return value


class GetPlayerScoreSerializer(serializers.Serializer):
    puuid = serializers.CharField(max_length=255)

    def validate_puuid(self, value):
        if not Players.objects.filter(puuid=value).exists():
            raise serializers.ValidationError(f"puuid '{value}' does not exist")
        return value


class GetTeamsSerializer(serializers.Serializer):
    players = serializers.ListField(
        child=serializers.ListField(
            child=serializers.JSONField(),
            required=False
        ),
        allow_empty=True
    )
