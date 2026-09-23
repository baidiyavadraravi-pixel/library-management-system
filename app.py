from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'library_secret_key_2026'

DB_NAME = 'library.db'


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT,
            category TEXT,
            quantity INTEGER DEFAULT 1,
            available INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')

        conn = get_db_connection()
        existing = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            conn.close()
            flash('Username already taken, choose another', 'error')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['logged_in'] = True
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    search_query = request.args.get('q', '').strip()
    conn = get_db_connection()
    if search_query:
        books = conn.execute(
            'SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY id DESC',
            (f'%{search_query}%', f'%{search_query}%')
        ).fetchall()
    else:
        books = conn.execute('SELECT * FROM books ORDER BY id DESC').fetchall()
    total_books = len(books)
    total_quantity = sum(b['quantity'] for b in books)
    conn.close()
    return render_template(
        'dashboard.html',
        books=books,
        total_books=total_books,
        total_quantity=total_quantity,
        search_query=search_query
    )


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        category = request.form['category']
        quantity = int(request.form['quantity'] or 1)
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO books (title, author, isbn, category, quantity, available) VALUES (?, ?, ?, ?, ?, ?)',
            (title, author, isbn, category, quantity, quantity)
        )
        conn.commit()
        conn.close()
        flash('Book added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_book.html')


@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    if book is None:
        conn.close()
        flash('Book not found', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        category = request.form['category']
        quantity = int(request.form['quantity'] or 1)
        available = int(request.form['available'] or 0)
        conn.execute(
            'UPDATE books SET title=?, author=?, isbn=?, category=?, quantity=?, available=? WHERE id=?',
            (title, author, isbn, category, quantity, available, book_id)
        )
        conn.commit()
        conn.close()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('edit_book.html', book=book)


@app.route('/delete/<int:book_id>')
@login_required
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
