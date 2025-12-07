from django.db import models
from django.contrib.auth import get_user_model
from challenges.models import Challenge

User = get_user_model()

class Enrollment(models.Model):
    PARTICIPANT = "participant"
    MODERATOR = "moderator"
    ROLE_CHOICES = [(PARTICIPANT, "Participant"), (MODERATOR, "Moderator")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="enrollments")
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default=PARTICIPANT)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "challenge")

    def __str__(self):
        return f"{self.user} -> {self.challenge} ({self.role})"
