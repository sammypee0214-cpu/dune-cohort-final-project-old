from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.DuneLoginView.as_view(), name="login"),
    # Django 5 requires logout to be a POST request (the navbar uses a form).
    path("logout/", LogoutView.as_view(), name="logout"),
]
