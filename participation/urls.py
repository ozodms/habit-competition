from django.urls import path
from .views import join_challenge, leave_challenge

urlpatterns = [
    path("<slug:slug>/join/", join_challenge, name="join"),
    path("<slug:slug>/leave/", leave_challenge, name="leave"),
]
