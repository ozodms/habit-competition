from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Habit(models.Model):
    DAILY = "daily"
    WEEKLY = "weekly"
    FREQ_CHOICES = [(DAILY, "Daily"), (WEEKLY, "Weekly")]

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=10, choices=FREQ_CHOICES, default=DAILY)
    max_per_day = models.PositiveSmallIntegerField(default=1)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
