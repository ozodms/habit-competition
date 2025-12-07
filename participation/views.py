from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from .models import Enrollment
from challenges.models import Challenge

@require_POST
@login_required
def join_challenge(request, slug):
    ch = get_object_or_404(Challenge, slug=slug)
    Enrollment.objects.get_or_create(user=request.user, challenge=ch)
    return redirect("challenges:detail", slug=slug)

@require_POST
@login_required
def leave_challenge(request, slug):
    ch = get_object_or_404(Challenge, slug=slug)
    Enrollment.objects.filter(user=request.user, challenge=ch).delete()
    return redirect("challenges:detail", slug=slug)
