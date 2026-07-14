from django.contrib import admin

from .models import (Author, Genre, Book, LibraryEntry, JournalEntry, Annotation, Bookmark, FavoriteQuote,)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

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

@admin.register(LibraryEntry)
class LibraryEntryAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'book', 
        'status',
        'current_page',
        'personal_rating',
        'is_favorite',
        'date_added'
    )

    search_fields = (
        'user__username', 
        'book__title', 
        )
    
    list_filter = (
        'status',
        'is_favorite',
        'date_added',
        )
    
@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'library_entry',
        'mood',
        'created_at',
    )

    search_fields = (
        'title', 
        'library_entry__book__title', 
        )
    
    list_filter = (
        'mood',
        
        )
    
@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = (
        'library_entry',
        'page_number',
        'highlight_color',
        'created_at',
    )

    search_fields = (
        'selected_text',
        'library_entry__book__title', 
        
        )
    
    list_filter = (
        
        'highlight_color',
        )
    
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = (
        'library_entry',
        'page_number',
        'chapter_name',
        'created_at',
    )

    search_fields = (
        'chapter_name',
        'library_entry__book__title', 
        )
    
@admin.register(FavoriteQuote)
class FavoriteQuoteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author_name',
        'book',
        'created_at',
    )

    search_fields = (
        'quote',
        'author_name', 
        'book__title',
        )
    
    list_filter = (
        'created_at',
        )