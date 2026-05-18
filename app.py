import json
import os

from flask import Flask, render_template

app = Flask(__name__)


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
    return render_template('borrow_return.html')


# Route for the index page, with an optional name parameter.
@app.route('/')
@app.route('/<name>', strict_slashes=False)
# Renders the index.html template, passing the name variable to it (defaulting to "Guest" if no name is provided).
def index(name="Guest"):
    return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
