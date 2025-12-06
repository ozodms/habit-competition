from django.urls import path
from .views import HabitList, HabitDetail, HabitCreate, HabitUpdate, HabitDelete

urlpatterns = [
    path("", HabitList.as_view(), name="list"),
    path("create/", HabitCreate.as_view(), name="create"),
    path("<int:pk>/", HabitDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", HabitUpdate.as_view(), name="edit"),
    path("<int:pk>/delete/", HabitDelete.as_view(), name="delete"),
]
