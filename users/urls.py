from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("library/", views.library, name="library"),
    path("add-book/", views.add_book, name="add_book"),
    
    path(
    "library/<int:pk>/update/",
    views.update_library_entry,
    name="update_library_entry",
    ),
    
    path(
    "library/<int:pk>/delete/",
    views.delete_library_entry,
    name="delete_library_entry",
    ),
    
    path(
        "discover/", 
         views.search_books, 
         name="search_books"
         ),
    
    path(
            "google-book/<str:google_books_id>/",
            views.google_book_detail,
            name="google_book_detail",
        ),
    
    path(
            "import-book/<str:google_books_id>/",
            views.import_book,
            name="import_book",
        ),
]