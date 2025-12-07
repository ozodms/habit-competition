from django.urls import path
from .views import checkin_plus, checkin_minus

urlpatterns = [
    path("<slug:slug>/checkin/<int:habit_id>/plus/", checkin_plus, name="plus"),
    path("<slug:slug>/checkin/<int:habit_id>/minus/", checkin_minus, name="minus"),
]
