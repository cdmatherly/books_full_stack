from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Book:
    DB = 'books_schema'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites = []
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(cls.DB).query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books

    @classmethod
    def save(cls, data):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def get_book_with_authors(cls, book_id):
        query = """SELECT * FROM books
                LEFT JOIN favorites
                ON favorites.book_id = books.id
                LEFT JOIN users
                ON users.id = favorites.user_id
                WHERE books.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, {'id': book_id})
        print(results)
        book = cls(results[0])
        for row in results:
            author_data = {
                'id': row['id'],
                'name': row['name'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            book.favorites.append(user.User(author_data))
            print(book)
        return book
    
    @classmethod
    def add_favorite(cls, data):
        query = """INSERT INTO favorites (book_id, user_id) VALUES ( %(book_id)s, %(user_id)s );"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results