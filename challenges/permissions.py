from participation.models import Enrollment


def user_can_manage_challenge(user, challenge) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_staff or challenge.created_by_id == user.id:
        return True
    return Enrollment.objects.filter(
        user=user, challenge=challenge, role="moderator"
    ).exists()
