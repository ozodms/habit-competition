from django.db import models

class Checkin(models.Model):
    enrollment = models.ForeignKey("participation.Enrollment", on_delete=models.CASCADE, related_name="checkins")
    habit = models.ForeignKey("habits.Habit", on_delete=models.CASCADE, related_name="checkins")
    done_at = models.DateField()
    quantity = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("enrollment", "habit", "done_at")
        indexes = [models.Index(fields=["enrollment", "done_at"])]

    def __str__(self):
        return f"{self.enrollment.user} · {self.habit.title} · {self.done_at} x{self.quantity}"
