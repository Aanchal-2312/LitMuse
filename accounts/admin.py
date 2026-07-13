from django.contrib import admin

from .models import Author, Genre, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'author', 
        'published_year',
        'pages',
        'average_rating'
    )

    search_fields = (
        'title', 
        'author__name', 
        )
    
    list_filter = (
        'genres', 
        'language',
        'published_year', 
        )
    
    filter_horizontal = ('genres',)
    
