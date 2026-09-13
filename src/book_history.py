from datetime import datetime
from src.debug import debug_error


def _sort_key_for_date(value):
    """Normalize date-like values to a sortable ISO string."""
    if value is None:
        return "0000-00-00"
    if isinstance(value, datetime):
        return value.date().isoformat()
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _latest_activity_date(borrow_date, return_date):
    """Return the newest activity date available for a borrow record."""
    dates = [value for value in (borrow_date, return_date) if value]
    if not dates:
        return None
    return max(dates)


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

            active_borrows.append(
                {
                    "idBorrow": r[0],
                    "idUser": r[1],
                    "first_name": r[2] or "",
                    "last_name": r[3] or "",
                    "book_copy_ISBN": r[4],
                    "book_copy_id": r[5],
                    "Title": r[6],
                    "borrow_date": r[7].isoformat() if r[7] else None,
                    "due_date": r[8].isoformat() if r[8] else None,
                    "overdue": overdue,
                }
            )

        active_borrows.sort(
            key=lambda item: (
                _sort_key_for_date(item["borrow_date"]),
                item["idBorrow"],
            ),
            reverse=True,
        )
    except Exception as e:
        debug_error(f"Error fetching active borrow data: {e}")
    return active_borrows


def get_borrow_history(cursor):
    """Return all borrow and return records for the dashboard history table."""
    history = []
    try:
        cursor.execute("""
            SELECT b.idBorrow, b.idUser, u.first_name, u.last_name,
                   b.book_copy_ISBN, b.book_copy_id, bk.Title,
                   b.borrow_date, b.due_date, b.return_date, b.returned, b.late
            FROM borrows b
            LEFT JOIN users u ON b.idUser = u.idUser
            LEFT JOIN books bk ON b.book_copy_ISBN = bk.ISBN
        """)
        rows = cursor.fetchall()
        today = datetime.today().date()

        for r in rows:
            due_obj = r[8]
            if due_obj and isinstance(due_obj, datetime):
                due_date_only = due_obj.date()
            else:
                due_date_only = due_obj

            returned = bool(r[10])
            late = bool(r[11])
            overdue = bool(not returned and due_date_only and due_date_only < today)
            latest_activity_date = _latest_activity_date(r[7], r[9])

            if returned:
                loan_status = "Returned"
                late_status = "Late" if late else "On time"
            else:
                loan_status = "Borrowed"
                late_status = "Overdue" if overdue else "Not late"

            history.append(
                {
                    "idBorrow": r[0],
                    "idUser": r[1],
                    "first_name": r[2] or "",
                    "last_name": r[3] or "",
                    "book_copy_ISBN": r[4],
                    "book_copy_id": r[5],
                    "Title": r[6],
                    "borrow_date": r[7].isoformat() if r[7] else None,
                    "due_date": r[8].isoformat() if r[8] else None,
                    "return_date": r[9].isoformat() if r[9] else None,
                    "latest_activity_date": latest_activity_date.isoformat()
                    if latest_activity_date
                    else None,
                    "loan_status": loan_status,
                    "late_status": late_status,
                    "overdue": overdue,
                    "late": late,
                }
            )

        history.sort(
            key=lambda item: (
                _sort_key_for_date(item["latest_activity_date"]),
                item["idBorrow"],
            ),
            reverse=True,
        )
    except Exception as e:
        debug_error(f"Error fetching borrow history data: {e}")
    return history
