from django import forms
from accounts.models import Book, LibraryEntry


class AddBookForm(forms.Form):

    book = forms.ModelChoiceField(
        queryset=Book.objects.all()
    )



class LibraryEntryForm(forms.ModelForm):

    class Meta:

        model = LibraryEntry

        fields = [
            "status",
            "current_page",
            "personal_rating",
            "is_favorite",
        ]