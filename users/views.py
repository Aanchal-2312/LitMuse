from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import LibraryEntry, Book
from users.forms import AddBookForm, LibraryEntryForm


def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 
                "Your account has been created successfully.")
            return redirect("home")

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

            messages.success(request, 
                             f"Welcome back, {user.username}!"
                             )

            return redirect("home")

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

    messages.success(request, "You have been logged out.")

    return redirect("home")


@login_required
def library(request):

    library = LibraryEntry.objects.filter(
        user=request.user
    )

    context = {
        "library": library,
    }

    return render(
        request,
        "users/library.html",
        context,
    )


 

@login_required
def add_book(request):

    if request.method == "POST":

        form = AddBookForm(request.POST)

        if form.is_valid():

            book = form.cleaned_data["book"]

            if LibraryEntry.objects.filter(
                user=request.user,
                book=book,
            ).exists():

                messages.warning(
                    request,
                    "This book is already in your library.",
                )

                return redirect("library")

            LibraryEntry.objects.create(
                user=request.user,
                book=book,
            )

            messages.success(
                request,
                f'"{book.title}" added to your library.',
            )

            return redirect("library")

    else:

        form = AddBookForm()

    return render(
        request,
        "users/add_book.html",
        {
            "form": form,
        },
    )

@login_required
def update_library_entry(request, pk):

    entry = get_object_or_404(
        LibraryEntry,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":

        form = LibraryEntryForm(
            request.POST,
            instance=entry,
        )

        if form.is_valid():

            form.save()

            messages.success(request,
                "Library entry updated successfully."  )

            return redirect("library")

    else:

        form = LibraryEntryForm(instance=entry)

    return render(
        request,
        "users/update_library_entry.html",
        {
            "form": form,
            "entry": entry,
        },
    )

@login_required
def delete_library_entry(request, pk):

    entry = get_object_or_404(
        LibraryEntry,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":

        entry.delete()

        messages.success(request,
            f"{entry.book.title} removed from your library."
        )

        return redirect("library")

    return render(
        request,
        "users/delete_library_entry.html",
        {
            "entry": entry,
        },
    )