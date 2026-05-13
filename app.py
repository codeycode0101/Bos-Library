from flask import Flask, render_template

app = Flask(__name__)

# Route for the about page
@app.route('/about', strict_slashes=False)
def about():
    return render_template('about.html')

# Route for the index page, with an optional name parameter.
@app.route('/')
@app.route('/<name>', strict_slashes=False)

# Renders the index.html template, passing the name variable to it (defaulting to "Guest" if no name is provided).
def index(name="Guest"):
    return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)