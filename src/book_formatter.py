def data_search(book):
    book["search_text"] = f"{book['isbn']} {book['title']} {book['author']} {book['genre']} {book['status']}"
    return book["search_text"]

def check_book_availability(book):
    book_status = ""
    if not book['total_copies'] or not book['available_copies']:
        book_status = "is-unavailable"
    elif book['available_copies'] / book['total_copies'] >= 0.75:
        book_status = "is-plentiful"
    elif book['available_copies'] / book['total_copies'] >= 0.5:
        book_status = "is-moderate"
    else:
        book_status = "is-low"
    book["availability_status"] = book_status
    return book_status

def calculate_bar_width(book):
    if book['total_copies'] == 0:
        return 0
    return round((book['available_copies'] / book['total_copies']) * 100)