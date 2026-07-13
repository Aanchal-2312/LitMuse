from django.db import models

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

    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
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
    