from flask import Flask, render_template, request
from datetime import timedelta
import mysql.connector
import json
import os

from flask import Flask, render_template

app = Flask(__name__)

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

# Fetch result
data = cursor.fetchall()
print(data)



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
@app.route('/borrow-return', strict_slashes=False)
def borrow_return():
    # TODO: For borrowing and returning books, use an NFC reader to read student card data
    # and a barcode scanner to scan ISBN barcodes so the system can store the book information.
    user_id= request.form['borrower-id']
    book_title = request.form['borrow-title']
    book_ISBN = find_book(book_title)

    # Find available copy
    cursor.execute("""
    SELECT copy_id FROM book_copies 
    WHERE copy_ISBN = %s AND copy_status = 'Available' 
    LIMIT 1""", (book_ISBN))

    # Assign the id of the copy 
    copy_id = cursor.fetchall()

    # If there is no copy available:
    if not copy_id:
        return "No available option."
    
    # Check how many books does the user borrow:
    if count(user_id) == False:
        return 'You have borrowed more than 3 books. Please return before borrowing.'
        
    # Set the borrow_date
    borrow_date = request.form['borrow_date']

    # Calculate the due_date
    due_date = borrow_date + timedelta(14)

    # Add the borrow action into borrows_table
    parameters_borrow= [borrow_date, due_date, user_id, copy_id, book_ISBN]
    cursor.execute("""
    INSERT INTO borrows(borrow_date, due_date, idUser, book_copy_id, book_copy_ISBN) 
    VALUES (%s, %s, %s, %s, %s)""",
    (parameters_borrow))

    # Change the copy_status
    parameters_copy_status = [copy_id, book_ISBN]
    cursor.execute("""
    UPDATE book_copies 
    SET copy_status = "Borrowed"
    WHERE (copy_id = %s) AND (copy_ISBN = %s)""",
    (parameters_copy_status))

    db.commit()


    return render_template('borrow_return.html')


# Route for the index page, with an optional name parameter.
@app.route('/')
@app.route('/<name>', strict_slashes=False)
# Renders the index.html template, passing the name variable to it (defaulting to "Guest" if no name is provided).
def index(name="Guest"):
    return render_template('index.html', name=name)

# Find user_id based on their name

# Find book's ISBN based on the name of the book
def find_book(title):
    cursor.execute("""
    SELECT * FROM books 
    WHERE books.Title LIKE '%s'""",(f'%{title}%'))

    book_ISBN = cursor.fetchall()
    
    if not book_ISBN:
        return "Sorry, we don't have this book."
    
    return book_ISBN

# Check how many books does the user borrow
def count(user_id):
    cursor.execute("""
    SELECT count(idBorrow) FROM borrows
    WHERE idUser = %s"""
    ,(user_id))

    count = cursor.fetchall()[0]

    if count > 3:
        return False
    return True


if __name__ == '__main__':
    app.run(debug=True)
