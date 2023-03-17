from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user,book

class Favorite:
    DB = 'books_schema'
    def __init__(self, data):
        self.user_id = data['user_id']
        self.book_id = data['book_id']