from django.db import models
from django.contrib.auth.models import User



class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    photo_url = models.URLField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)

    authors = models.ManyToManyField(
        Author, 
        
        related_name='books'
    )

    genres = models.ManyToManyField(
        Genre, 
        related_name='books'
    )

    isbn_10 = models.CharField(max_length=10, blank=True)
    isbn_13 = models.CharField(max_length=13, blank=True)
    
    published_year = models.PositiveIntegerField(
        null=True, 
        blank=True
        )
    
    publisher = models.CharField(
        max_length=255, 
        blank=True
        )
    
    language = models.CharField(
        max_length=50, 
        blank=True
        )
    
    pages = models.PositiveIntegerField(
        null=True, 
        blank=True
        )
    
    description = models.TextField(blank=True)
    
    cover_url = models.URLField(blank=True)

    average_rating = models.FloatField(
        null=True, 
        blank=True
        )
    
    ratings_count = models.PositiveIntegerField(default=0)

    google_books_id = models.CharField(
        max_length=100, 
        blank=True, 
        unique=True,
        null=True
        )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
class LibraryEntry(models.Model):

    class ReadingStatus(models.TextChoices):
        WANT_TO_READ = "WTR", "Want to Read"
        READING = "RDG", "Reading"
        COMPLETED = "CMP", "Completed"
        PAUSED = "PSE", "Paused"
        DROPPED = "DRP", "Dropped"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="library"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="library_entries"
    )

    status = models.CharField(
        max_length=3,
        choices=ReadingStatus.choices,
        default=ReadingStatus.WANT_TO_READ
    )

    current_page = models.PositiveIntegerField(
        default=0
    )

    personal_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True
    )

    is_favorite = models.BooleanField(default=False)

    uploaded_file = models.FileField(
        upload_to="books/",
        blank=True,
        null=True
    )

    date_added = models.DateTimeField(auto_now_add=True)

    started_reading = models.DateField(
        null=True,
        blank=True
    )

    finished_reading = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-date_added"]

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'], 
                name='unique_user_book'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    

class JournalEntry(models.Model):

    class Mood(models.TextChoices):
        INSPIRED = "INS", "Inspired"
        HAPPY = "HAP", "Happy"
        THOUGHTFUL = "THO", "Thoughtful"
        PEACEFUL = "PEA", "Peaceful"
        EXCITED = "EXC", "Excited"
        EMOTIONAL = "EMO", "Emotional"
        CONFUSED = "CON", "Confused"
        SAD = "SAD", "Sad"

    library_entry = models.ForeignKey(
        LibraryEntry,
        on_delete=models.CASCADE,
        related_name="journal_entries"
    )

    title = models.CharField(max_length=255)

    reflection = models.TextField()

    mood = models.CharField(
        max_length=3,
        choices=Mood.choices,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    

class Annotation(models.Model):

    class HighlightColor(models.TextChoices):
        YELLOW = "YEL", "Yellow"
        GREEN = "GRN", "Green"
        BLUE = "BLU", "Blue"
        PINK = "PNK", "Pink"
        PURPLE = "PUR", "Purple"

    library_entry = models.ForeignKey(
        LibraryEntry,
        on_delete=models.CASCADE,
        related_name="annotations"
    )

    selected_text = models.TextField()

    note = models.TextField(blank=True)

    page_number = models.PositiveIntegerField()

    highlight_color = models.CharField(
        max_length=3,
        choices=HighlightColor.choices,
        default=HighlightColor.YELLOW
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["page_number"]

    def __str__(self):
        return f"Page {self.page_number}"
    

class Bookmark(models.Model):

    library_entry = models.ForeignKey(
        LibraryEntry,
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )

    page_number = models.PositiveIntegerField()

    chapter_name = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["page_number"]

    def __str__(self):
        return f"Bookmark - Page {self.page_number}"
    

class FavoriteQuote(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_quotes"
    )

    quote = models.TextField()

    author_name = models.CharField(
        max_length=255,
        blank=True
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="favorite_quotes"
    )

    library_entry = models.ForeignKey(
        LibraryEntry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="favorite_quotes"
    )

    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.quote[:50]
    
