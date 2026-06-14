# Bos-Library

Web application to handle typical tasks within a library. (eg., borrow/return books, library history)

## Setup

1. Create and activate the Python virtual environment:
   - PowerShell: `python -m venv venv` then `./venv/Scripts/Activate.ps1`
   - Command Prompt: `python -m venv venv` then `./venv/Scripts/activate.bat`

2. Create a `.env` file in the project root with the database and secret values:
   ```env
   SECRET_KEY=your_secret_key_here
   DB_HOST=
   DB_PORT=
   DB_USER=
   DB_PASSWORD=
   DB_DATABASE=
   ```

3. Install dependencies:
   - `pip install -r requirements.txt`

4. Run the app:
   - `python app.py`

## Dependencies

Dependencies are listed in `requirements.txt` so you can install them cleanly without committing the `venv/` folder.

## Git note

Keep both `venv/` and `.env` out of Git using the `.gitignore` entries in this repository. Only commit `requirements.txt`.
