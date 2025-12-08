from django.urls import path
from .views import (
    ChallengeList,
    ChallengeDetail,
    ChallengeCreate,
    ChallengeUpdate,
    ChallengeDelete,
    ManageChallengeHabitsView,
)

urlpatterns = [
    path("", ChallengeList.as_view(), name="list"),
    path("create/", ChallengeCreate.as_view(), name="create"),
    path("<slug:slug>/", ChallengeDetail.as_view(), name="detail"),
    path("<slug:slug>/edit/", ChallengeUpdate.as_view(), name="edit"),
    path("<slug:slug>/delete/", ChallengeDelete.as_view(), name="delete"),
    path("<slug:slug>/manage-habits/", ManageChallengeHabitsView.as_view(), name="manage_habits"),
]
