from flask import Flask, render_template, request
from src.borrow_book import borrow_book
from src.return_book import return_book
from src.book_history import get_active_borrows
from src.debug import debug, debug_error, debug_warning, debug_info, debug_success
from src.utils import db, cursor
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Required for flash messages

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
        action = request.form.get('action')
        debug("borrow_return route received POST", color='yellow')
        debug(f"form action: {action}", color='cyan')

        if action == 'borrow':
            resp = borrow_book()
            if resp:
                return resp
            else:
                debug_warning("Borrowing failed. Check the form data and try again.")
        elif action == 'return':
            resp = return_book()
            if resp:
                return resp
            else:
                debug_warning("Returning failed. Check the form data and try again.")

    # Query active borrows to populate dashboard tab
    # TODO: Update the table every POST request so the dashboard is always up to date.
    active_borrows = get_active_borrows(cursor)
    debug_success(f"Active borrows fetched: {active_borrows}")

    return render_template('borrow_return.html', active_borrows=active_borrows)


# Route for the index page, with an optional name parameter.
@app.route('/')
@app.route('/<name>', strict_slashes=False)
# Renders the index.html template, passing the name variable to it (defaulting to "Guest" if no name is provided).
def index(name="Guest"):
    return render_template('index.html', name=name)



if __name__ == '__main__':
    app.run(debug=True)
