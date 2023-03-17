from flask import redirect, render_template, request
from flask_app import app
from flask_app.models.book import Book
from flask_app.models.user import User

@app.route('/')
def index():
    return redirect('/authors')

@app.route('/books')
def show_books():
    books = Book.get_all()
    return render_template('books.html', books = books)

@app.route('/books/create', methods=['POST'])
def create_book():
    Book.save(request.form)
    return redirect('/books')

@app.route('/books/<int:book_id>')
def one_book(book_id):
    book = Book.get_book_with_authors(book_id)
    all_authors = User.get_all()
    authors = Book.filter_favorites(book, all_authors)
    return render_template('one_book.html', authors = authors, book = book)

@app.route('/books/favorite', methods=['POST'])
def favorite_book():
    Book.add_favorite(request.form)
    # print(f"REQUEST FORM !!!!!!!!!!!!!!!!!!!!! {request.form}")
    return redirect(f"/books/{request.form['book_id']}")