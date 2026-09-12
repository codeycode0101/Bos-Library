"""Catalog queries for the public books page."""


def get_catalog_books(cursor):
    """Return every catalog title with its current copy availability."""
    cursor.execute("""
        SELECT b.ISBN,
               b.Title,
               b.Author,
               b.Age_Restricted,
               g.name AS genre,
               COUNT(bc.copy_id) AS total_copies,
               COALESCE(SUM(bc.copy_status = 'Available'), 0) AS available_copies
        FROM books AS b
        LEFT JOIN genres AS g ON g.idGenre = b.idGenre
        LEFT JOIN book_copies AS bc ON bc.copy_ISBN = b.ISBN
        GROUP BY b.ISBN, b.Title, b.Author, b.Age_Restricted, g.name
        ORDER BY b.Title ASC, b.Author ASC
    """)

    catalog = []
    for isbn, title, author, age_restriction, genre, total_copies, available_copies in cursor.fetchall():
        available_copies = int(available_copies or 0)
        total_copies = int(total_copies or 0)
        catalog.append({
            'isbn': isbn,
            'title': title or 'Untitled',
            'author': author or 'Unknown author',
            'genre': genre or 'Uncategorised',
            'age_restriction': age_restriction,
            'available_copies': available_copies,
            'total_copies': total_copies,
            'status': 'Available' if available_copies else 'Unavailable',
        })

    return catalog


def get_catalog_book(cursor, isbn):
    """Return one catalog title and its current copy availability."""
    cursor.execute("""
        SELECT b.ISBN,
               b.Title,
               b.Author,
               b.Age_Restricted,
               g.name AS genre,
               COUNT(bc.copy_id) AS total_copies,
               COALESCE(SUM(bc.copy_status = 'Available'), 0) AS available_copies
        FROM books AS b
        LEFT JOIN genres AS g ON g.idGenre = b.idGenre
        LEFT JOIN book_copies AS bc ON bc.copy_ISBN = b.ISBN
        WHERE b.ISBN = %s
        GROUP BY b.ISBN, b.Title, b.Author, b.Age_Restricted, g.name
    """, (isbn,))
    record = cursor.fetchone()
    if record is None:
        return None

    isbn, title, author, age_restriction, genre, total_copies, available_copies = record
    available_copies = int(available_copies or 0)
    total_copies = int(total_copies or 0)
    return {
        'isbn': isbn,
        'title': title or 'Untitled',
        'author': author or 'Unknown author',
        'genre': genre or 'Uncategorised',
        'age_restriction': age_restriction,
        'available_copies': available_copies,
        'total_copies': total_copies,
        'status': 'Available' if available_copies else 'Unavailable',
    }
