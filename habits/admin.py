from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("title", "frequency", "max_per_day", "owner")
    list_filter = ("frequency",)
    search_fields = ("title", "description")
