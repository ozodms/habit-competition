from django.db.models import Q
from .models import Challenge
from participation.models import Enrollment


def visible_challenges_qs(user):
    qs = Challenge.objects.all()
    if not user.is_authenticated:
        return qs.filter(is_public=True)
    return qs.filter(
        Q(is_public=True) | Q(created_by=user) | Q(enrollments__user=user)
    ).distinct()


def user_can_manage_challenge(user, challenge) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_staff or challenge.created_by_id == user.id:
        return True
    return Enrollment.objects.filter(
        user=user, challenge=challenge, role="moderator"
    ).exists()
