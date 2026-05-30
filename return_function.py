from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Connect to server
db = mysql.connector.connect(
    host = "127.0.0.1",
    port = 3306,
    user = "root",
    password = "Bosworth@123",
    database = "bos_library"
)

# Get a buffered cursor to avoid unread-result errors when using multiple sequential queries
cursor = db.cursor(buffered=True)

# Find book's ISBN based on the name of the book
def find_isbn(title):
    cursor.execute("SELECT books.ISBN FROM books WHERE books.Title LIKE %s",(f'%{title}%',))

    # Fetches result row from executed query
    book_ISBN = cursor.fetchone()

    if not book_ISBN:
        return False
    
    return book_ISBN[0]

def return_book():
    if request.method != 'POST':
        return None

    user_id = request.form.get('returner-id')
    book_title = request.form.get('return-title')
    return_date_str = request.form.get('return-date')
    copy_id = request.form.get('copy-id')

    # Return book_ISBN
    book_ISBN = find_isbn(book_title)
    if book_ISBN == False:
        flash("Book not found. Please check the title and try again.", "error")
        return redirect(url_for('borrow_return'))

    # Debugging prints
    print("User ID:", user_id)
    print("Book title:", book_title)
    print("Return date:", return_date_str)
    print("Copy ID:", copy_id)

    if not (user_id and book_title and return_date_str):
        flash("Please fill in all fields.", "error")
        return redirect(url_for('borrow_return'))   

    # Check whether the user has borrowed the book
    if copy_id:
        cursor.execute("SELECT idBorrow FROM borrows WHERE idUser = %s AND book_copy_ISBN = %s AND idCopy = %s AND returned IS NULL",(user_id, book_ISBN, copy_id))
    else:
        cursor.execute("SELECT idBorrow FROM borrows WHERE idUser = %s AND book_copy_ISBN = %s AND returned IS NULL",(user_id, book_ISBN))

    row = cursor.fetchone()
    if not row:
        flash("No record of borrowing this book found for this user.", "error")
        return redirect(url_for('borrow_return'))
    borrow_record = row[0]

    # Debugging print
    print("Borrow record found:", borrow_record)

    # Pull the due date from the borrow record  
    cursor.execute("SELECT due_date FROM borrows WHERE idBorrow = %s",(borrow_record,))      
    due_date = cursor.fetchone()[0]

    # Check whether the return date > due date
    return_date = datetime.strptime(return_date_str, '%Y-%m-%d')
    if return_date > due_date:
        cursor.execute("UPDATE borrows SET returned = TRUE, return_date = %s, late = TRUE WHERE idBorrow = %s",(return_date, borrow_record))
        flash("Book returned late.", "error")
    else:
        cursor.execute("UPDATE borrows SET returned = TRUE, return_date = %s, late = FALSE WHERE idBorrow = %s",(return_date, borrow_record))
        flash("Book returned on time. Thank you!", "success")

    # Change the status of the book copy to 'available'
    if copy_id:
        cursor.execute("UPDATE book_copies SET status = 'available' WHERE ISBN = %s AND idCopy = %s AND status = 'borrowed'",(book_ISBN, copy_id))
    else:  
        cursor.execute("UPDATE book_copies SET status = 'available' WHERE ISBN = %s AND status = 'borrowed' LIMIT 1",(book_ISBN,))

    # Commit the changes to the database
    db.commit()
    return redirect(url_for('borrow_return'))
