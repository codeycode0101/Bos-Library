# Bos-Library

Web application to handle typical tasks within a library. (eg., borrow/return books, library history)

## Setup

1. Create and activate the Python virtual environment:
   - PowerShell: `python -m venv venv` then `./venv/Scripts/Activate.ps1`
   - Command Prompt: `python -m venv venv` then `./venv/Scripts/activate.bat`

2. Install dependencies:
   - `pip install -r requirements.txt`

3. Run the app:
   - `python app.py`

## Dependencies

Dependencies are listed in `requirements.txt` so you can install them cleanly without committing the `venv/` folder.

## Git note

Keep `venv/` out of Git by using the `.gitignore` entry added to this repository. Only commit `requirements.txt`.
