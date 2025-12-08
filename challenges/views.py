from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from habits.models import Habit
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Challenge, ChallengeHabit
from .permissions import user_can_manage_challenge
from participation.models import Enrollment
from tracking.models import Checkin


class ChallengeList(ListView):
    model = Challenge
    template_name = "challenges/list.html"
    context_object_name = "challenges"
    paginate_by = 10

    def get_queryset(self):
        qs = Challenge.objects.all()
        user = self.request.user
        qs = qs.filter(
            Q(is_public=True)
            | Q(created_by=user if user.is_authenticated else None)
            | Q(enrollments__user=user if user.is_authenticated else None)
        ).distinct()
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

        chh_list = list(self.object.challenge_habits.select_related("habit"))
        if enrollment:
            today = timezone.localdate()
            qty_map = {
                c.habit_id: c.quantity
                for c in Checkin.objects.filter(enrollment=enrollment, done_at=today)
            }
            for chh in chh_list:
                chh.today_qty = qty_map.get(chh.habit_id, 0)
        else:
            for chh in chh_list:
                chh.today_qty = 0

        ctx["challenge_habits"] = chh_list
        return ctx


class ChallengeCreate(LoginRequiredMixin, CreateView):
    model = Challenge
    fields = ["name", "description", "start_date", "end_date", "is_public"]
    template_name = "challenges/form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        from participation.models import Enrollment

        Enrollment.objects.get_or_create(
            user=self.request.user, challenge=obj, defaults={"role": "moderator"}
        )
        return super().form_valid(form)


class OwnerOrStaffRequired(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or (obj.created_by_id == self.request.user.id)


class ChallengeUpdate(LoginRequiredMixin, OwnerOrStaffRequired, UpdateView):
    model = Challenge
    fields = ["name", "description", "start_date", "end_date", "is_public"]
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "challenges/form.html"


class ChallengeDelete(LoginRequiredMixin, OwnerOrStaffRequired, DeleteView):
    model = Challenge
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "challenges/confirm_delete.html"
    success_url = reverse_lazy("challenges:list")


class ManageChallengeHabitsView(View):
    template_name = "challenges/manage_habits.html"

    def get(self, request, slug):
        ch = get_object_or_404(Challenge, slug=slug)
        if not user_can_manage_challenge(request.user, ch):
            messages.error(request, "You don't have permission to manage habits for this challenge.")
            return redirect("challenges:detail", slug=slug)

        eligible = Habit.objects.filter(Q(is_global=True) | Q(owner=request.user)).order_by("title")

        rels = {r.habit_id: r for r in ChallengeHabit.objects.filter(challenge=ch).select_related("habit")}

        rows = []
        for h in eligible:
            r = rels.get(h.id)
            rows.append({
                "habit": h,
                "checked": bool(r),
                "weight": getattr(r, "weight", 1),
            })

        return render(request, self.template_name, {
            "challenge": ch,
            "rows": rows,
        })

    def post(self, request, slug):
        ch = get_object_or_404(Challenge, slug=slug)
        if not user_can_manage_challenge(request.user, ch):
            messages.error(request, "You don't have permission to manage habits for this challenge.")
            return redirect("challenges:detail", slug=slug)

        eligible_ids = set(
            Habit.objects.filter(Q(is_global=True) | Q(owner=request.user)).values_list("id", flat=True)
        )
        selected_ids = {int(x) for x in request.POST.getlist("habits") if x.isdigit()}
        selected_ids &= eligible_ids

        existing = {r.habit_id: r for r in ChallengeHabit.objects.filter(challenge=ch)}

        added, updated = 0, 0

        for hid in selected_ids:
            raw = request.POST.get(f"weight_{hid}", "1").strip()
            try:
                weight = float(raw)
            except ValueError:
                weight = 1.0
            weight = max(0.1, min(weight, 100.0))

            rel = existing.get(hid)
            if rel:
                if rel.weight != weight:
                    rel.weight = weight
                    rel.save()
                    updated += 1
            else:
                ChallengeHabit.objects.create(challenge=ch, habit_id=hid, weight=weight)
                added += 1

        removed = 0
        for hid, rel in existing.items():
            if hid not in selected_ids:
                rel.delete()
                removed += 1

        messages.success(request, f"Saved: +{added}, updated {updated}, removed {removed}.")
        return redirect("challenges:manage_habits", slug=slug)
