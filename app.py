from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import timedelta, datetime
import mysql.connector
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Find user_id based on their name

# Find book's ISBN based on the name of the book
def find_isbn(title):
    cursor.execute("SELECT books.ISBN FROM books WHERE books.Title LIKE %s",(f'%{title}%',))

    # Fetches result row from executed query
    book_ISBN = cursor.fetchone()

    if not book_ISBN:
        return False
    
    return book_ISBN[0]

# Check how many books does the user borrow
def allow_borrow(user_id):
    cursor.execute("SELECT COUNT(idBorrow) FROM borrows WHERE idUser = %s",(user_id,))

    count = cursor.fetchone()

    # TODO: Later implement a portal to change such parameters on the web app. Not in the code directly.
    print("Amount of books borrowed:", count[0])
    if count[0] > 4:
        return False
    return True

# Connect to server
db = mysql.connector.connect(
    host = "127.0.0.1",
    port = 3306,
    user = "root",
    password = "Bosworth@123",
    database = "bos_library"
)

# Get a cursor
cursor = db.cursor()

# Function to load book data from a JSON file
def load_books():
    data_path = os.path.join(app.root_path, 'data', 'books.json')
    with open(data_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# Route for the about page
@app.route('/about', strict_slashes=False)
def about():
    return render_template('about.html')


# Route for the available books page
@app.route('/books', strict_slashes=False)
def books():
    books = load_books()
    return render_template('books.html', books=books)


# Route for the borrow and return page
@app.route('/borrow-return', strict_slashes=False, methods=['GET', 'POST'])
def borrow_return():
    # TODO: For borrowing and returning books, use an NFC reader to read student card data.
    # and a barcode scanner to scan ISBN barcodes so the system can store the book information.

    
    if request.method == 'POST':
        #TODO: Create alert boxes instead of returning text.
        user_id = request.form.get('borrower-id')
        book_title = request.form.get('borrow-title')
        borrow_date_str = request.form.get('borrow-date')

        # Debugging prints
        print("User ID:", user_id)
        print("Book title:", book_title)
        print("Borrow date:", borrow_date_str)

        if not (user_id and book_title and borrow_date_str):
            flash("Please fill in all fields.", "error")
            return redirect(url_for('borrow_return'))
       
        book_title = request.form['borrow-title']
        book_ISBN = find_isbn(book_title)
        if not book_ISBN:
            flash("Sorry we don't have this book.", "error")
            return redirect(url_for('borrow_return'))
        
        print("book ISBN:", book_ISBN)

        # Find available copy
        cursor.execute("SELECT copy_id FROM book_copies WHERE copy_ISBN = %s AND copy_status = 'Available'", (book_ISBN,))

        # Retrieve the id of the copy
        copy_id = cursor.fetchone()

        # If there is no copy available:
        if not copy_id:
            flash("No available copy.", "error")
            return redirect(url_for('borrow_return'))

        copy_id = copy_id[0]
        print("Copy ID:", copy_id)
        
        # Check how many books does the user borrow:
        if not allow_borrow(user_id):
            flash("You have borrowed more than 3 books. Please return before borrowing.", "error")
            return redirect(url_for('borrow_return'))

        # Convert the borrow date string to a date object
        borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d').date()
        
        # Calculate the due_date (current date + 14 days)
        due_date = borrow_date + timedelta(days=14)
        print("Due date:", due_date)

        # Add the borrow action into borrows_table
        parameters_borrow = (borrow_date, due_date, user_id, copy_id, book_ISBN)
        cursor.execute("INSERT INTO borrows(borrow_date, due_date, idUser, book_copy_id, book_copy_ISBN) VALUES (%s, %s, %s, %s, %s)",
        parameters_borrow)

        # Change the copy_status
        parameters_copy_status = (copy_id, book_ISBN)
        cursor.execute("""
        UPDATE book_copies 
        SET copy_status = "Borrowed"
        WHERE (copy_id = %s) AND (copy_ISBN = %s)""",
        parameters_copy_status)

        db.commit()

        flash("Book borrowed successfully.", "success")
        return redirect(url_for('borrow_return'))
    return render_template('borrow_return.html')


# Route for the index page, with an optional name parameter.
@app.route('/')
@app.route('/<name>', strict_slashes=False)
# Renders the index.html template, passing the name variable to it (defaulting to "Guest" if no name is provided).
def index(name="Guest"):
    return render_template('index.html', name=name)



if __name__ == '__main__':
    app.run(debug=True)
