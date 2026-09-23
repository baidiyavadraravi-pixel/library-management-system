# Library Management System

A simple **Library Management System** web application built with **Python (Flask)** and **SQLite**, featuring a login page and full **CRUD** (Create, Read, Update, Delete) operations on books.

## Features

- Login page (username: `admin`, password: `admin123`)
- Add new books
- View all books in a dashboard (with total titles / total copies stats)
- Search books by title or author
- Edit / update book details
- Delete books
- Data stored in a local SQLite database (`library.db`), created automatically on first run

## Tech Stack

- Python 3
- Flask
- SQLite3
- HTML, CSS (Jinja2 templates)

## Project Structure

```
library_management_system/
│
├── app.py                 # Main Flask application (routes + CRUD logic)
├── requirements.txt        # Python dependencies
├── library.db              # SQLite database (auto-created on first run)
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── add_book.html
│   └── edit_book.html
└── static/
    └── style.css
```

## How to Run (in VS Code)

1. Install **Python 3** (if not already installed) and **VS Code**.
2. Open the project folder in VS Code: `File > Open Folder...`
3. Open a terminal in VS Code: `Terminal > New Terminal`
4. (Recommended) Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
   ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Run the application:
   ```
   python app.py
   ```
7. Open your browser and go to: `http://127.0.0.1:5000`
8. Login with:
   - Username: `admin`
   - Password: `admin123`

## Notes

- The database file `library.db` is created automatically the first time you run the app.
- To reset all data, simply delete `library.db` and restart the app.
