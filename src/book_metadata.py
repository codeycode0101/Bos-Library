import json
from functools import lru_cache
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def _text_value(value):
    """Extract a displayable string from Open Library's string/dict fields."""
    if isinstance(value, dict):
        return value.get('value') or ''
    return value or ''


def _fetch_json(url):
    request = Request(url, headers={'User-Agent': 'Bosworth-Library/1.0'})
    with urlopen(request, timeout=3) as response:
        return json.load(response)


@lru_cache(maxsize=512)
def get_open_library_details(isbn, title='', author=''):
    """Fetch optional public bibliographic details, without blocking the catalogue on errors."""
    try:
        record = _fetch_json(
            f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data'
        ).get(f'ISBN:{isbn}', {})

        description = _text_value(record.get('notes'))
        work_keys = record.get('works') or []
        search_record = {}
        if title and (not description or not work_keys):
            query = urlencode({'title': title, 'author': author, 'limit': 1})
            search_record = (_fetch_json(f'https://openlibrary.org/search.json?{query}').get('docs') or [{}])[0]
            work_key = search_record.get('key')
            if work_key and not work_keys:
                work_keys = [{'key': work_key}]

        if work_keys and work_keys[0].get('key'):
            work_record = _fetch_json(f"https://openlibrary.org{work_keys[0]['key']}.json")
            description = _text_value(work_record.get('description')) or description

        return {
            'description': description,
            'publish_date': record.get('publish_date') or search_record.get('first_publish_year'),
            'pages': record.get('number_of_pages'),
            'publisher': (record.get('publishers') or [{}])[0].get('name'),
            'subjects': ([subject.get('name') for subject in record.get('subjects', [])[:6] if subject.get('name')]
                         or search_record.get('subject', [])[:6]),
            'url': record.get('url'),
        }
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError):
        return {}


@lru_cache(maxsize=512)
def get_google_books_details(isbn, title='', author=''):
    """Fetch public book metadata from Google Books as a fallback source."""
    try:
        items = _fetch_json(
            f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&maxResults=1&printType=books'
        ).get('items') or []
        if not items and title:
            query = urlencode({'q': f'intitle:{title} inauthor:{author}', 'maxResults': 1, 'printType': 'books'})
            items = _fetch_json(f'https://www.googleapis.com/books/v1/volumes?{query}').get('items') or []
        if not items:
            return {}

        info = items[0].get('volumeInfo') or {}
        return {
            'description': info.get('description'),
            'publish_date': info.get('publishedDate'),
            'pages': info.get('pageCount'),
            'publisher': info.get('publisher'),
            'subjects': info.get('categories') or [],
            'url': info.get('infoLink'),
        }
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError):
        return {}


@lru_cache(maxsize=512)
def get_book_metadata(isbn, title, author, genre):
    """Combine Open Library data with Google Books when data is missing."""
    open_library = get_open_library_details(isbn, title, author)
    google_books = get_google_books_details(isbn, title, author)
    metadata = {}
    sources = []

    if open_library and any(open_library.values()):
        metadata.update(open_library)
        sources.append({'name': 'Open Library', 'url': 'https://openlibrary.org/'})

    if google_books and any(google_books.values()):
        google_used = False
        for key, value in google_books.items():
            if value and not metadata.get(key):
                metadata[key] = value
                google_used = True
        if google_used:
            sources.append({'name': 'Google Books', 'url': 'https://books.google.com/'})

    if not metadata.get('description'):
        metadata['description'] = (
            f'{title} is a {genre.lower()} title by {author}, available in the Bosworth Library collection.'
        )
        metadata['description_source'] = 'Library overview'
    else:
        metadata['description_source'] = 'Book description'

    metadata['sources'] = sources
    return metadata
