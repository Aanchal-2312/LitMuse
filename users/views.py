from django.http import HttpResponse
from django.contrib import messages
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Genre, LibraryEntry, Book, Author
from users.forms import AddBookForm, LibraryEntryForm
from .services import (search_google_books, get_google_book,)


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "users/dashboard.html")



def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 
                "Your account has been created successfully.")
            return redirect("users:dashboard")

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
                             "Happy reading!"
                             )

            return redirect("users:dashboard")

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

                return redirect("users:library")

            LibraryEntry.objects.create(
                user=request.user,
                book=book,
            )

            messages.success(
                request,
                f'"{book.title}" added to your library.',
            )

            return redirect("users:library")

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

            return redirect("users:library")

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

        return redirect("users:library")

    return render(
        request,
        "users/delete_library_entry.html",
        {
            "entry": entry,
        },
    )

@login_required
def search_books(request):

    books = []

    query = request.GET.get("q")

    if query:
        books = search_google_books(query)

    return render(
        request,
        "users/discover_books.html",
        {
            "books": books,
        },
    )


@login_required
def google_book_detail(request, google_books_id):

    book = get_google_book(google_books_id)

    in_library = LibraryEntry.objects.filter(
    user=request.user,
    book__google_books_id=google_books_id,
).exists()

    return render(
        request,
        "users/google_book_detail.html",
        {
            "book": book,
            "google_books_id": google_books_id,
            "in_library": in_library,
        },
    )


@login_required
@require_POST

def import_book(request, google_books_id):
    book_data = get_google_book(google_books_id)

    author_names = book_data.get("authors", [])

    authors = []

    for author_name in author_names:
        author, created = Author.objects.get_or_create(
            name=author_name,
        )
        authors.append(author)

    published_year = None

    published_date = book_data.get("publishedDate")

    if published_date:
        try:
            published_year = int(book_data["publishedDate"][:4])
        except ValueError:
            pass



    isbn_10 = ""
    isbn_13 = ""

    industry_identifiers = book_data.get(
        "industryIdentifiers",
        [],
    )

    for identifier in industry_identifiers:

        if identifier.get("type") == "ISBN_10":
            isbn_10 = identifier.get("identifier", "")

        elif identifier.get("type") == "ISBN_13":
            isbn_13 = identifier.get("identifier", "")



    category_names = book_data.get("categories", [])

    genres = []

    for category_name in category_names:
        genre, created = Genre.objects.get_or_create(
            name=category_name,
            defaults={
                "slug": slugify(category_name),
            },
        )
        genres.append(genre)

    



    book, created = Book.objects.get_or_create(
        google_books_id=google_books_id,
        defaults={
            "title": book_data.get("title", ""),
            "isbn_10": isbn_10,
            "isbn_13": isbn_13,
            "published_year": published_year,
            "publisher": book_data.get("publisher", ""),
            "language": book_data.get("language", ""),
            "pages": book_data.get("pageCount"),
            "description": book_data.get("description", ""),
            "cover_url": book_data.get("imageLinks", {}).get("thumbnail", ""),
            "average_rating": book_data.get("averageRating"),
            "ratings_count": book_data.get("ratingsCount", 0),
        },
    )

    book.authors.set(authors)
    book.genres.set(genres)
    library_entry, created = LibraryEntry.objects.get_or_create(
        user=request.user,
        book=book,
    )

    if created:
        messages.success(request, "Book added to your library!")
    else:
        messages.info(request, "Book is already in your library.")
        
    return redirect(
        "users:google_book_detail",
        google_books_id=google_books_id,
    )