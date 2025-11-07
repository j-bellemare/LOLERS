from django.db import models

# this file is where the data model for our DB is generated


class Players(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, serialize=False)
    puuid = models.CharField( max_length=255)
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    score = models.FloatField()


class GameData(models.Model):
    id = models.AutoField(primary_key=True)
    game_id = models.CharField(max_length=255)
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    player_game_score = models.FloatField()
