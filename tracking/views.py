from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from participation.models import Enrollment
from challenges.models import Challenge, ChallengeHabit
from habits.models import Habit
from .models import Checkin


def _ensure_in_bounds(challenge: Challenge) -> bool:
    today = timezone.localdate()
    return challenge.start_date <= today <= challenge.end_date


def _habit_in_challenge(challenge: Challenge, habit: Habit) -> bool:
    return ChallengeHabit.objects.filter(challenge=challenge, habit=habit).exists()


@login_required
@require_POST
def checkin_plus(request, slug, habit_id):
    ch = get_object_or_404(Challenge, slug=slug)
    enr = get_object_or_404(Enrollment, user=request.user, challenge=ch)
    habit = get_object_or_404(Habit, id=habit_id)

    if not _habit_in_challenge(ch, habit):
        messages.error(request, "This habit is not part of the challenge.")
        return redirect("challenges:detail", slug=slug)

    if not _ensure_in_bounds(ch):
        messages.error(request, "Check-ins are allowed only within challenge dates.")
        return redirect("challenges:detail", slug=slug)

    today = timezone.localdate()
    chk, _ = Checkin.objects.get_or_create(
        enrollment=enr, habit=habit, done_at=today, defaults={"quantity": 0}
    )

    if chk.quantity >= habit.max_per_day:
        messages.warning(request, "You've reached today's limit for this habit.")
    else:
        chk.quantity += 1
        chk.save()
        messages.success(request, "Recorded.")

    return redirect("challenges:detail", slug=slug)


@login_required
@require_POST
def checkin_minus(request, slug, habit_id):
    ch = get_object_or_404(Challenge, slug=slug)
    enr = get_object_or_404(Enrollment, user=request.user, challenge=ch)
    habit = get_object_or_404(Habit, id=habit_id)

    if not _habit_in_challenge(ch, habit):
        messages.error(request, "This habit is not part of the challenge.")
        return redirect("challenges:detail", slug=slug)

    today = timezone.localdate()
    chk = Checkin.objects.filter(
        enrollment=enr, habit=habit, done_at=today
    ).first()

    if not chk:
        messages.info(request, "Nothing to undo.")
        return redirect("challenges:detail", slug=slug)

    if chk.quantity <= 1:
        chk.delete()
        messages.success(request, "Undone.")
    else:
        chk.quantity -= 1
        chk.save()
        messages.success(request, "Updated.")

    return redirect("challenges:detail", slug=slug)
