from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "challenge", "role", "joined_at")
    list_filter = ("role", "challenge")
    search_fields = ("user__username", "challenge__name")
