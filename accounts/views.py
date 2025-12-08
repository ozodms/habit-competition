from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .form import SignUpForm # type: ignore

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        resp = super().form_valid(form)
        messages.success(self.request, "Account created. Please sign in.")
        return resp
