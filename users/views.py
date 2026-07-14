from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect

def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")

    else:
        form = UserCreationForm()

    return render(
        request,
        "users/register.html",
        {"form": form}
    )


def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()
            login(request, user)

            return redirect("/")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "users/login.html",
        {
            "form": form,
        },
    )


def logout_view(request):

    logout(request)

    return redirect("/")