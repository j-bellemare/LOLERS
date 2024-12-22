from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_handler_app.views import (
    PlayersViewSet,
    GameDataViewSet,
)

router = DefaultRouter()
router.register(r"players", PlayersViewSet, basename="players")
router.register(r"gamedata", GameDataViewSet, basename="gamedata")

urlpatterns = [
    path("api/handler/", include(router.urls)),
]
