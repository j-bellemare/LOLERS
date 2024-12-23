from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lolers_app.views import (
    PlayersViewSet,
    GameDataViewSet,
)

router = DefaultRouter()
router.register(r"players", PlayersViewSet, basename="players")
router.register(r"gamedata", GameDataViewSet, basename="gamedata")

urlpatterns = [
    path("api/lolers/", include(router.urls)),
]
