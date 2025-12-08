from django.db import models

class ScoreEvent(models.Model):
    enrollment = models.ForeignKey(
        "participation.Enrollment",
        on_delete=models.CASCADE,
        related_name="score_events",
    )
    checkin = models.ForeignKey(
        "tracking.Checkin",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="score_events",
    )
    points = models.IntegerField()
    reason = models.CharField(max_length=80, default="checkin")
    created_at = models.DateTimeField(auto_now_add=True)


class LeaderboardSnapshot(models.Model):
    challenge = models.ForeignKey("challenges.Challenge", on_delete=models.CASCADE)
    period = models.DateField()
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("challenge", "period")
