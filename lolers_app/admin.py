from django.contrib import admin
from .models import Players, GameData


class PlayersAdmin(admin.ModelAdmin):
    list_display = ("puuid", "name", "tag", "score")


class GameDataAdmin(admin.ModelAdmin):
    list_display = ("id", "game_id", "player", "player_game_score")


admin.site.register(Players, PlayersAdmin)
admin.site.register(GameData, GameDataAdmin)
