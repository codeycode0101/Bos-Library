from flask import request, flash, redirect, url_for
from src.utils import db, cursor, find_isbn
from src.debug import debug_info, debug_warning
from datetime import datetime


def return_book():
    """Handle book return operation."""
    if request.method != 'POST':
        return None

    user_id = request.form.get('returner-id')
    book_title = request.form.get('return-title')
    return_date_str = request.form.get('return-date')
    copy_id = request.form.get('copy-id')

    # Debugging prints
    debug_info(f"User ID: {user_id}")
    debug_info(f"Book title: {book_title}")
    debug_info(f"Return date: {return_date_str}")
    debug_info(f"Copy ID: {copy_id}")

    # Check that all fields are filled
    if not (user_id and book_title and return_date_str):
        flash("Please fill in all fields.", "error")
        return redirect(url_for('borrow_return'))   

    # Fetch book_ISBN from database
    book_ISBN = find_isbn(book_title, cursor)
    if not book_ISBN:
        flash("Book not found. Please check the title and try again.", "error")
        return redirect(url_for('borrow_return'))

    # Debugging print
    debug_info(f"Book ISBN: {book_ISBN}")

    # Request the borrow id(s) depending on whether copy_id was given or not
    if copy_id:
        cursor.execute("SELECT idBorrow FROM borrows WHERE idUser = %s AND book_copy_ISBN = %s AND book_copy_id = %s AND returned IS NULL", (user_id, book_ISBN, copy_id))
    else:
        cursor.execute("SELECT idBorrow, book_copy_id FROM borrows WHERE idUser = %s AND book_copy_ISBN = %s AND returned IS NULL", (user_id, book_ISBN))

    # Retrieve the 1st borrow id in the array of borrow id(s)
    raw_borrow_id = cursor.fetchone()
    

    debug_warning(f"Borrow id(s) query result: {raw_borrow_id}")

    if not raw_borrow_id:
        flash("No record of borrowing this book found for this user.", "error")
        return redirect(url_for('borrow_return'))
    
    
    borrow_id = raw_borrow_id[0]  # Extracting borrow_id from the tuple returned by fetchone()

    # Debugging print
    debug_info(f"Borrow record found: {borrow_id}")

    if not copy_id and len(raw_borrow_id) > 1:
        copy_id = raw_borrow_id[1]  # Extracting copy_id from the tuple returned by fetchone()
        debug_info(f"Copy ID retrieved (Linked to idborrow): {copy_id}")
    
    # Pull the due date from the borrow record  
    cursor.execute("SELECT due_date FROM borrows WHERE idBorrow = %s", (borrow_id,))      
    due_date = cursor.fetchone()[0]

    # Check whether the return date > due date
    return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
    if return_date > due_date:
        cursor.execute("UPDATE borrows SET returned = TRUE, return_date = %s, late = TRUE WHERE idBorrow = %s", (return_date, borrow_id))
        flash("Book returned late.", "error")
    else:
        cursor.execute("UPDATE borrows SET returned = TRUE, return_date = %s, late = FALSE WHERE idBorrow = %s", (return_date, borrow_id))
        flash("Book returned on time. Thank you!", "success")

    # Change the status of the book copy to 'available'
    cursor.execute("UPDATE book_copies SET copy_status = 'Available' WHERE copy_ISBN = %s AND copy_id = %s AND copy_status = 'Borrowed'", (book_ISBN, copy_id))

    # Commit the changes to the database
    db.commit()
    return redirect(url_for('borrow_return'))
