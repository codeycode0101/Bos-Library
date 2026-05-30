from datetime import datetime
from debug import debug_error


def get_active_borrows(cursor):
    """Return active borrow records for the dashboard."""
    # Returns a list of dictionaries with keys: idBorrow, idUser, first_name, last_name, book_copy_ISBN, book_copy_id, Title, borrow_date, due_date, overdue
    active_borrows = []
    try:
        cursor.execute("""
            SELECT b.idBorrow, b.idUser, u.first_name, u.last_name,
                   b.book_copy_ISBN, b.book_copy_id, bk.Title, b.borrow_date, b.due_date
            FROM borrows b
            LEFT JOIN users u ON b.idUser = u.idUser
            LEFT JOIN books bk ON b.book_copy_ISBN = bk.ISBN
            WHERE b.returned IS NULL
            ORDER BY b.borrow_date DESC
        """)
        rows = cursor.fetchall()
        for r in rows:
            due_obj = r[8]
            overdue = False
            try:
                if due_obj and isinstance(due_obj, datetime):
                    due_date_only = due_obj.date()
                else:
                    due_date_only = due_obj
                if due_date_only:
                    overdue = due_date_only < datetime.today().date()
            except Exception:
                overdue = False

            active_borrows.append({
                'idBorrow': r[0],
                'idUser': r[1],
                'first_name': r[2] or '',
                'last_name': r[3] or '',
                'book_copy_ISBN': r[4],
                'book_copy_id': r[5],
                'Title': r[6],
                'borrow_date': r[7].isoformat() if r[7] else None,
                'due_date': r[8].isoformat() if r[8] else None,
                'overdue': overdue
            })
    except Exception as e:
        debug_error(f'Error fetching active borrow data: {e}')
    return active_borrows
