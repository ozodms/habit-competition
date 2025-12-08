from django.urls import path
from .views import LeaderboardView

urlpatterns = [
    path("<slug:slug>/leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
]
