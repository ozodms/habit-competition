from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Habit


class HabitList(ListView):
    model = Habit
    template_name = "habits/list.html"
    context_object_name = "habits"
    paginate_by = 20


class HabitDetail(DetailView):
    model = Habit
    template_name = "habits/detail.html"


class HabitCreate(LoginRequiredMixin, CreateView):
    model = Habit
    fields = ["title", "description", "frequency", "max_per_day"]
    template_name = "habits/form.html"
    success_url = reverse_lazy("habits:list")

    def form_valid(self, form):

        obj = form.save(commit=False)
        if not obj.owner:
            obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)


class HabitUpdate(LoginRequiredMixin, UpdateView):
    model = Habit
    fields = ["title", "description", "frequency", "max_per_day"]
    template_name = "habits/form.html"
    success_url = reverse_lazy("habits:list")


class HabitDelete(LoginRequiredMixin, DeleteView):
    model = Habit
    template_name = "habits/confirm_delete.html"
    success_url = reverse_lazy("habits:list")
