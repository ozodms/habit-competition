from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include(("accounts.urls", "accounts"))),
    path("habits/", include(("habits.urls", "habits"))),
    path("challenges/", include(("challenges.urls", "challenges"))),
    path("participation/", include(("participation.urls", "participation"))),
    path("tracking/", include(("tracking.urls", "tracking"))),
    path("scoring/", include(("scoring.urls", "scoring"))),
]
