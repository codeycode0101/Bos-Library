import os
from dotenv import load_dotenv
from flask import Flask, abort, render_template, request
from src.book_formatter import (
    data_search,
    check_book_availability,
    calculate_bar_width,
)
from src.book_history import get_active_borrows
from src.book_metadata import get_book_metadata
from src.borrow_book import borrow_book
from src.catalog import get_catalog_book, get_catalog_books
from src.debug import debug, debug_error, debug_warning, debug_success
from src.login_system import login_admin, logout_admin, require_admin_login
from src.return_book import return_book
from src.utils import cursor

load_dotenv()
app = Flask(__name__)
secret_key = os.getenv("SECRET_KEY")
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    debug_error("Missing SECRET_KEY environment variable")
    raise RuntimeError("Missing SECRET_KEY environment variable")
    debug_error("Missing SECRET_KEY environment variable")
    raise RuntimeError("Missing SECRET_KEY environment variable")
app.secret_key = secret_key

# Route for the about page
# TODO: Disabled for now, but can be enabled if needed in the future.
# @app.route('/about', strict_slashes=False)
# def about():
#     return render_template('about.html')


# Route for the available books page
@app.route("/books", strict_slashes=False)
@app.route("/books", strict_slashes=False)
def books():
    books = get_catalog_books(cursor)
    return render_template(
        "books.html",
        books=books,
        data_search=data_search,
        check_book_availability=check_book_availability,
        calculate_bar_width=calculate_bar_width,
    )


@app.route("/books/<isbn>", strict_slashes=False)
@app.route("/books/<isbn>", strict_slashes=False)
def book_detail(isbn):
    book = get_catalog_book(cursor, isbn)
    if book is None:
        abort(404)
    metadata = get_book_metadata(isbn, book["title"], book["author"], book["genre"])
    check_book_availability(book)
    return render_template(
        "book_detail.html",
        "book_detail.html",
        book=book,
        metadata=metadata,
        calculate_bar_width=calculate_bar_width,
    )


# Route for the login page
@app.route("/login", strict_slashes=False, methods=["GET", "POST"])
@app.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    if request.method == "POST":
    if request.method == "POST":
        return login_admin()

    return render_template("login.html")
    return render_template("login.html")


@app.route("/logout", strict_slashes=False)
@app.route("/logout", strict_slashes=False)
def logout():
    return logout_admin()


# Route for the borrow and return page
@app.route("/borrow-return", strict_slashes=False, methods=["GET", "POST"])
@app.route("/borrow-return", strict_slashes=False, methods=["GET", "POST"])
def borrow_return():
    auth_response = require_admin_login()
    if auth_response is not None:
        return auth_response

    if request.method == "POST":
        action = request.form.get("action")
        debug("borrow_return route received POST", color="yellow")
        debug(f"form action: {action}", color="cyan")
    if request.method == "POST":
        action = request.form.get("action")
        debug("borrow_return route received POST", color="yellow")
        debug(f"form action: {action}", color="cyan")

        if action == "borrow":
            if resp := borrow_book():
                return resp
            debug_warning("Borrowing failed. Check the form data and try again.")
        elif action == "return":
            if resp := return_book():
                return resp
            debug_warning("Returning failed. Check the form data and try again.")

    # Query active borrows to populate dashboard tab
    active_borrows = get_active_borrows(cursor)
    debug_success(f"Active borrows fetched: {active_borrows}")

    return render_template("borrow_return.html", active_borrows=active_borrows)


# Route for the index page, with an optional name parameter.
@app.route("/")
@app.route("/<name>", strict_slashes=False)
@app.route("/")
@app.route("/<name>", strict_slashes=False)
# Renders the index.html template, passing the name variable to it (defaulting to "Guest" if no name is provided).
def index(name="Guest"):
    return render_template("index.html", name=name)
    return render_template("index.html", name=name)


if __name__ == "__main__":
if __name__ == "__main__":
    app.run(debug=True)
