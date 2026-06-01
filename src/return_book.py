from flask import request, flash, redirect, url_for
from src.utils import db, cursor, find_isbn
from src.debug import debug_info
from datetime import datetime


def return_book():
    """Handle book return operation."""
    if request.method != 'POST':
        return None

    user_id = request.form.get('returner-id')
    book_title = request.form.get('return-title')
    return_date_str = request.form.get('return-date')
    copy_id = request.form.get('copy-id')

    # Return book_ISBN
    book_ISBN = find_isbn(book_title, cursor)
    if book_ISBN == False:
        flash("Book not found. Please check the title and try again.", "error")
        return redirect(url_for('borrow_return'))

    # Debugging prints
    debug_info(f"User ID: {user_id}")
    debug_info(f"Book title: {book_title}")
    debug_info(f"Return date: {return_date_str}")
    debug_info(f"Copy ID: {copy_id}")

    if not (user_id and book_title and return_date_str):
        flash("Please fill in all fields.", "error")
        return redirect(url_for('borrow_return'))   

    # Check whether the user has borrowed the book
    if copy_id:
        cursor.execute("SELECT idBorrow FROM borrows WHERE idUser = %s AND book_copy_ISBN = %s AND book_copy_id = %s AND returned IS NULL", (user_id, book_ISBN, copy_id))
    else:
        cursor.execute("SELECT idBorrow FROM borrows WHERE idUser = %s AND book_copy_ISBN = %s AND returned IS NULL", (user_id, book_ISBN))

    row = cursor.fetchone()
    if not row:
        flash("No record of borrowing this book found for this user.", "error")
        return redirect(url_for('borrow_return'))
    borrow_record = row[0]

    # Debugging print
    debug_info(f"Borrow record found: {borrow_record}")

    # Pull the due date from the borrow record  
    cursor.execute("SELECT due_date FROM borrows WHERE idBorrow = %s", (borrow_record,))      
    due_date = cursor.fetchone()[0]

    # Check whether the return date > due date
    return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
    if return_date > due_date:
        cursor.execute("UPDATE borrows SET returned = TRUE, return_date = %s, late = TRUE WHERE idBorrow = %s", (return_date, borrow_record))
        flash("Book returned late.", "error")
    else:
        cursor.execute("UPDATE borrows SET returned = TRUE, return_date = %s, late = FALSE WHERE idBorrow = %s", (return_date, borrow_record))
        flash("Book returned on time. Thank you!", "success")

    # Change the status of the book copy to 'available' (Check for copy_id first as it is given optional, if not given, just update the first copy with the same ISBN)
    if copy_id:
        cursor.execute("UPDATE book_copies SET copy_status = 'Available' WHERE copy_ISBN = %s AND copy_id = %s AND copy_status = 'Borrowed'", (book_ISBN, copy_id))
    else:  
        cursor.execute("UPDATE book_copies SET copy_status = 'Available' WHERE copy_ISBN = %s AND copy_status = 'Borrowed' LIMIT 1", (book_ISBN,))

    # Commit the changes to the database
    db.commit()
    return redirect(url_for('borrow_return'))
