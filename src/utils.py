import mysql.connector

# Connect to server - centralized database connection
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="Bosworth@123",
    database="bos_library"
)

# Get a buffered cursor to avoid unread-result errors when using multiple sequential queries
cursor = db.cursor(buffered=True)


def find_isbn(title, cursor):
    """Find book's ISBN based on the title."""
    cursor.execute("SELECT books.ISBN FROM books WHERE books.Title LIKE %s", (f'%{title}%',))
    book_ISBN = cursor.fetchone()
    
    if not book_ISBN:
        return False
    
    return book_ISBN[0]
