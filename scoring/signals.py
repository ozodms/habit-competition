from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tracking.models import Checkin
from .models import ScoreEvent
from challenges.models import ChallengeHabit

POINTS_PER_UNIT = 10


def compute_points(checkin: Checkin) -> int:
    enrollment = checkin.enrollment
    challenge = enrollment.challenge
    habit = checkin.habit

    try:
        ch_rel = ChallengeHabit.objects.get(challenge=challenge, habit=habit)
        weight = float(ch_rel.weight)
    except ChallengeHabit.DoesNotExist:
        weight = 0.0

    return int(round(checkin.quantity * POINTS_PER_UNIT * weight))


def upsert_score_event(checkin: Checkin):
    ScoreEvent.objects.filter(checkin=checkin).delete()

    pts = compute_points(checkin)
    if pts > 0:
        ScoreEvent.objects.create(
            enrollment=checkin.enrollment, checkin=checkin, points=pts, reason="checkin"
        )


@receiver(post_save, sender=Checkin)
def on_checkin_save(sender, instance: Checkin, created, **kwargs):
    upsert_score_event(instance)


@receiver(post_delete, sender=Checkin)
def on_checkin_delete(sender, instance: Checkin, **kwargs):
    ScoreEvent.objects.filter(checkin=instance).delete()
