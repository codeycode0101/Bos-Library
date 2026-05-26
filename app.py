from flask import Flask, render_template, request
from datetime import timedelta, datetime
from borrow_function import borrow
from return_function import return_book
import mysql.connector
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Required for flash messages

# I still leave the database connection here because I need to use the cursor in other functions (AI Generated code haha)
# I can move it to a separate file later if needed.

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

    # TODO FOR QUANG: Create an if statement to differentiate between borrow and return form submissions.

    borrow()
    return_book()
    return render_template('borrow_return.html')


# Route for the index page, with an optional name parameter.
@app.route('/')
@app.route('/<name>', strict_slashes=False)
# Renders the index.html template, passing the name variable to it (defaulting to "Guest" if no name is provided).
def index(name="Guest"):
    return render_template('index.html', name=name)



if __name__ == '__main__':
    app.run(debug=True)
