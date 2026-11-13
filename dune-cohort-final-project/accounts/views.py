from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render

from .forms import RegisterForm


class DuneLoginView(SuccessMessageMixin, LoginView):
    template_name = "accounts/login.html"
    success_message = "Welcome back, %(username)s!"
    redirect_authenticated_user = True


def register(request):
    if request.user.is_authenticated:
        return redirect("inventory:car_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # sign the new user in straight away
            messages.success(request, f"Account created. Welcome, {user.username}!")
            return redirect("inventory:car_list")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})
