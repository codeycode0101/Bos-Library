"""User lookup helpers for borrower-facing workflows."""


def _full_name(first_name, last_name):
    return f"{first_name or ''} {last_name or ''}".strip()


def get_user_directory(cursor):
    """Return users formatted for dashboard smart-search suggestions."""
    cursor.execute("""
        SELECT idUser, first_name, last_name, user_role
        FROM users
        ORDER BY first_name ASC, last_name ASC, idUser ASC
    """)

    users = []
    for user_id, first_name, last_name, user_role in cursor.fetchall():
        role = (user_role or "").strip()
        name = _full_name(first_name, last_name)
        users.append({
            "id": user_id,
            "name": name,
            "role": role,
            "search": f"{user_id} {name} {role}".strip(),
        })
    return users


def resolve_user_id(cursor, user_id=None, user_name=None):
    """Resolve a selected or typed borrower name to a single user ID."""
    if user_id:
        cursor.execute("SELECT idUser FROM users WHERE idUser = %s", (user_id,))
        row = cursor.fetchone()
        if row:
            return row[0], None

    clean_name = (user_name or "").strip()
    if not clean_name:
        return None, "Please choose a borrower."

    cursor.execute("""
        SELECT idUser
        FROM users
        WHERE LOWER(TRIM(CONCAT_WS(' ', first_name, last_name))) = LOWER(%s)
    """, (clean_name,))
    rows = cursor.fetchall()

    if len(rows) == 1:
        return rows[0][0], None

    if len(rows) > 1:
        return None, "Multiple borrowers match that name. Please choose one from the suggestions."

    return None, "Borrower not found. Please choose a borrower from the suggestions."
