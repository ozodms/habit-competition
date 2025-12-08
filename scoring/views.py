from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from challenges.models import Challenge
from .models import ScoreEvent

class LeaderboardView(TemplateView):
    template_name = "scoring/leaderboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]
        ch = get_object_or_404(Challenge, slug=slug)
        ctx["challenge"] = ch

        qs = (
            ScoreEvent.objects
            .filter(
                enrollment__challenge=ch,
                checkin__done_at__gte=ch.start_date,
                checkin__done_at__lte=ch.end_date,
                reason="checkin",
            )
            .values("enrollment__user__username", "enrollment_id")
            .annotate(total_points=Sum("points"))
            .order_by("-total_points")
        )

        ctx["rows"] = qs
        return ctx
