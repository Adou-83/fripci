from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {
        "form": form
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "users/login.html",
            {
                "error": "Nom d'utilisateur ou mot de passe incorrect."
            },
        )

    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")