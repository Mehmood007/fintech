import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .forms import UserRegisterForm
from .models import User

logger = logging.getLogger("custom_logger")


# "/user/signup"
class RegistrationView(View):
    template_name = "userauths/signup.html"
    form_class = UserRegisterForm

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> super or redirect:
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> render:
        context = {
            "form": self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> redirect or render:
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
            messages.success(request, "Successfully Signed Up")
            return redirect("account")

        messages.error(request, "Failed to register account")
        logger.error(form.errors)
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)


# "/user/login"
class LogInView(View):
    template_name = "userauths/login.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> render:
        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> redirect or render:
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)
        if user:
            messages.success(request, "Successfully logged in")
            login(request, user)
            return redirect("account")
        else:
            messages.error(request, "Failed to register account")
            return render(request, self.template_name)


# "/user/logout"
class LogoutView(View):
    def get(self, request: HttpRequest) -> render:
        logout(request)
        messages.success(request, "You have been logged out successfully")
        return redirect("home")
