from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Challenge


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
        # default ordering from Meta
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
