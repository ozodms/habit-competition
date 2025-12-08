from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Habit
from django.db import models


class HabitList(LoginRequiredMixin, ListView):
    model = Habit
    template_name = "habits/list.html"
    context_object_name = "habits"
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(models.Q(is_global=True) | models.Q(owner=user)).order_by("title")

class HabitDetail(DetailView):
    model = Habit
    template_name = "habits/detail.html"

class HabitCreate(LoginRequiredMixin, CreateView):
    model = Habit
    fields = ["title", "description", "frequency", "max_per_day", "is_global"]
    template_name = "habits/form.html"
    success_url = reverse_lazy("habits:list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        if not self.request.user.is_staff:
            obj.is_global = False
        obj.save()
        return super().form_valid(form)

class OwnerOrStaffRequired(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or (getattr(obj, "owner_id", None) == self.request.user.id)

class HabitUpdate(LoginRequiredMixin, OwnerOrStaffRequired, UpdateView):
    model = Habit
    fields = ["title", "description", "frequency", "max_per_day", "is_global"]
    template_name = "habits/form.html"
    success_url = reverse_lazy("habits:list")

    def form_valid(self, form):
        if not self.request.user.is_staff:
            form.instance.is_global = False
        return super().form_valid(form)


class HabitDelete(LoginRequiredMixin, DeleteView):
    model = Habit
    template_name = "habits/confirm_delete.html"
    success_url = reverse_lazy("habits:list")
