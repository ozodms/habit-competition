from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from habits.models import Habit
from django.contrib.auth import get_user_model

class Challenge(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_challenges", null=True, blank=True,)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.name

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("end_date cannot be before start_date")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def status(self) -> str:
        today = timezone.localdate()
        if self.start_date <= today <= self.end_date:
            return "active"
        if today < self.start_date:
            return "upcoming"
        return "past"

    def get_absolute_url(self):
        return reverse("challenges:detail", kwargs={"slug": self.slug})

class ChallengeHabit(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="challenge_habits")
    habit = models.ForeignKey("habits.Habit", on_delete=models.CASCADE, related_name="habit_challenges")
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=1)

    class Meta:
        unique_together = ("challenge", "habit")

    def __str__(self):
        return f"{self.challenge.name} · {self.habit.title} (w={self.weight})"
