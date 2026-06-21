from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect("home")

def home(request):
    return render(request, "accounts/home.html")


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            if user.role == "ADMIN":
                return redirect("/dashboard/")

            return redirect("/drivers/dashboard/")

        messages.error(
            request,
            "Invalid username or password"
        )

    return render(
        request,
        "accounts/login.html"
    )