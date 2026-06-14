import os
from dotenv import load_dotenv
from src.debug import debug_error
import mysql.connector

load_dotenv()

# Connect to server - centralized database connection
# Use environment variables to keep secrets out of source control.
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_database = os.getenv('DB_DATABASE')

missing = [name for name, value in [
    ('DB_HOST', db_host),
    ('DB_PORT', db_port),
    ('DB_USER', db_user),
    ('DB_PASSWORD', db_password),
    ('DB_DATABASE', db_database),
] if not value]
if missing:
    debug_error(f"Missing environment variables: {', '.join(missing)}")
    raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

# Connect to server - centralized database connection
# Use environment variables to keep secrets out of source control.
db = mysql.connector.connect(
    host=db_host,
    port=int(db_port),
    user=db_user,
    password=db_password,
    database=db_database
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
