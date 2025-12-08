from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta, date

from challenges.models import Challenge
from .models import ScoreEvent


def _period_bounds(ch: Challenge, period: str) -> tuple[date, date]:
    today = timezone.localdate()

    if period == "today":
        date_from = date_to = today
    elif period == "week":
        iso_weekday = today.isoweekday()
        monday = today - timedelta(days=iso_weekday - 1)
        sunday = monday + timedelta(days=6)
        date_from, date_to = monday, sunday
    else:
        date_from, date_to = ch.start_date, ch.end_date

    date_from = max(date_from, ch.start_date)
    date_to = min(date_to, ch.end_date)
    return (date_from, date_to)


class LeaderboardView(TemplateView):
    template_name = "scoring/leaderboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]
        ch = get_object_or_404(Challenge, slug=slug)
        period = self.request.GET.get("period", "challenge")

        date_from, date_to = _period_bounds(ch, period)

        rows = (
            ScoreEvent.objects.filter(
                enrollment__challenge=ch,
                checkin__done_at__gte=date_from,
                checkin__done_at__lte=date_to,
                reason="checkin",
            )
            .values("enrollment__user__username", "enrollment_id")
            .annotate(total_points=Sum("points"))
            .order_by("-total_points")
        )

        ctx.update(
            {
                "challenge": ch,
                "rows": rows,
                "period": period,
                "date_from": date_from,
                "date_to": date_to,
            }
        )
        return ctx
