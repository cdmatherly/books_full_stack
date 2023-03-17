from flask import redirect, render_template, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.book import Book

@app.route('/authors')
def show_authors():
    users = User.get_all()
    return render_template('authors.html', authors = users)

@app.route('/authors/create', methods=['POST'])
def create_author():
    User.save(request.form)
    return redirect('/authors')

@app.route('/authors/<int:author_id>')
def one_author(author_id):
    user = User.get_author_with_books(author_id)
    books = Book.get_all()
    # print(f"ALL BOOKS >>>>> {books}")
    return render_template('one_author.html', author = user, books=books)

@app.route('/authors/favorite', methods=['POST'])
def favorite_author():
    User.add_favorite(request.form)
    print(f"REQUEST FORM !!!!!!!!!!!!!!!!!!!!! {request.form}")
    return redirect(f"/authors/{request.form['user_id']}")