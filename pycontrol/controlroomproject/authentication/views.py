from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import RegisterUserForm


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return redirect("login_user")
    else:
        return render(request, "authenticate/login_user.html", {})


def logout_user(request):
    logout(request)
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()

    # Add placeholders to form fields
    form.fields["username"].widget.attrs["placeholder"] = "Enter your username"
    form.fields["password1"].widget.attrs["placeholder"] = "Enter your password"
    form.fields["password2"].widget.attrs["placeholder"] = "Confirm your password"

    return render(request, "authenticate/register_user.html", {"form": form})
