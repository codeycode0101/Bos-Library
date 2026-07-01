from flask import flash, redirect, render_template, request, session, url_for


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def is_admin_logged_in():
    """Return whether the current browser session has admin access."""
    return bool(session.get("admin_logged_in"))


def login_admin():
    """Handle admin login form submission."""
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["admin_logged_in"] = True
        session["admin_username"] = username
        flash("Logged in successfully.", "success")
        return redirect(url_for("borrow_return"))

    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)
    flash("Invalid admin username or password.", "error")
    return redirect(url_for("login"))


def logout_admin():
    """Clear admin login state for the current browser session."""
    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))


def require_admin_login():
    """Return an access-denied response when the admin is not logged in."""
    if is_admin_logged_in():
        return None

    flash("Please log in before opening the borrow and return dashboard.", "error")
    return (
        render_template(
            "error.html",
            title="Access denied",
            heading="Access denied",
            message="You need to sign in as an admin before using the borrow and return dashboard.",
        ),
        403,
    )
