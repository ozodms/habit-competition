from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Challenge
from participation.models import Enrollment
from tracking.models import Checkin


class ChallengeList(ListView):
    model = Challenge
    template_name = "challenges/list.html"
    context_object_name = "challenges"
    paginate_by = 10

    def get_queryset(self):
        qs = Challenge.objects.filter(is_public=True)
        status = self.request.GET.get("status")
        today = timezone.localdate()
        if status == "active":
            qs = qs.filter(start_date__lte=today, end_date__gte=today)
        elif status == "upcoming":
            qs = qs.filter(start_date__gt=today)
        elif status == "past":
            qs = qs.filter(end_date__lt=today)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["selected_status"] = self.request.GET.get("status", "")
        return ctx


class ChallengeDetail(DetailView):
    model = Challenge
    template_name = "challenges/detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        enrollment = None
        if user.is_authenticated:
            enrollment = Enrollment.objects.filter(
                user=user, challenge=self.object
            ).first()
        ctx["enrollment"] = enrollment
        ctx["participants_count"] = self.object.enrollments.count()

        if enrollment:
            today = timezone.localdate()
            qty_map = {
                c.habit_id: c.quantity
                for c in Checkin.objects.filter(enrollment=enrollment, done_at=today)
            }
            for chh in self.object.challenge_habits.select_related("habit"):
                chh.today_qty = qty_map.get(chh.habit_id, 0)

        return ctx
