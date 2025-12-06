from django.urls import path
from .views import ChallengeList, ChallengeDetail

urlpatterns = [
    path("", ChallengeList.as_view(), name="list"),
    path("<slug:slug>/", ChallengeDetail.as_view(), name="detail"),
]
