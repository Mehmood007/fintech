from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View


# "/"
class HomeView(View):
    template_name = "home.html"

    def get(self, request: HttpRequest) -> render:
        return render(request, self.template_name)
