from django.contrib import admin
from .models import Challenge, ChallengeHabit

class ChallengeHabitInline(admin.TabularInline):
    model = ChallengeHabit
    extra = 1

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "is_public", "created_by")
    list_filter = ("is_public",)
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ChallengeHabitInline]

    def status_badge(self, obj):
        return obj.status
    status_badge.short_description = "status"

@admin.register(ChallengeHabit)
class ChallengeHabitAdmin(admin.ModelAdmin):
    list_display = ("challenge", "habit", "weight")
    list_filter = ("challenge",)
    search_fields = ("challenge__name", "habit__title")
