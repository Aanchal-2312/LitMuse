from django.urls import path
from . import views

urlpatterns = [
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
]