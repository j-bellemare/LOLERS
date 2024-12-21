from django.contrib import admin
from .models import Players, GameData


class PlayersAdmin(admin.ModelAdmin):
    list_display = ("puuid", "name", "tag", "rank")


class GameDataAdmin(admin.ModelAdmin):
    list_display = ("id", "game_id", "game_mode", "player", "player_data")


admin.site.register(Players, PlayersAdmin)
admin.site.register(GameData, GameDataAdmin)
