import requests

from django.conf import settings


LANGUAGES = {
        "en": "English",
        "fr": "French",
        "es": "Spanish",
        "de": "German",
        "it": "Italian",
        "hi": "Hindi",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
    }



def search_google_books(query):
    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes",
        params={
            "q": query,
            "key": settings.GOOGLE_BOOKS_API_KEY,
            "maxResults": 20,
        },
    )

    data = response.json()

    return data.get("items", [])



def get_google_book(google_books_id):
    response = requests.get(
        f"https://www.googleapis.com/books/v1/volumes/{google_books_id}",
        params={
            "key": settings.GOOGLE_BOOKS_API_KEY,
        },
    )

    data = response.json()

    volume = data.get("volumeInfo", {})


    volume["language_name"] = LANGUAGES.get(
        volume.get("language"),
        volume.get("language"),
    )

    return volume