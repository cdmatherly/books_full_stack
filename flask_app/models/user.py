from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class User:
    DB = 'books_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorites = []
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (name) VALUES (%(name)s);"
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def get_author_with_books(cls, user_id):
        query = """SELECT * FROM users
                LEFT JOIN favorites
                ON favorites.user_id = users.id
                LEFT JOIN books
                ON books.id = favorites.book_id
                WHERE users.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, {'id': user_id})
        author = cls(results[0])
        for row in results:
            book_data = {
                'id': row['books.id'],
                'title': row['title'],
                'num_of_pages': row['num_of_pages'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            author.favorites.append(book.Book(book_data))
            # print(author.favorites[0].title, ",", author.name)
        return author
    
    @classmethod
    def add_favorite(cls, data):
        query = """INSERT INTO favorites (book_id, user_id) VALUES ( %(book_id)s, %(user_id)s );"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def filter_favorites(cls, author, books):
        for favorite in author.favorites:
            # print(f'\n~~~~~~~~~~~~~~~~~ NEW OUTER LOOP ~~~~~~~~~~~~~~~~')
            for i in range(len(books)):
                # print(f"\n -----------------NEW INNER LOOP {i+1} -------------------")
                # print(f"\nFAVORITES>>>>>>!!!!! {favorite.title} ID: {favorite.id}")
                # print(f"\n{range(len(books))}, {books}")
                # print(f"\nBOOK[{i}]: {books[i].title} ID: {books[i].id}")
                if books[i].id == favorite.id:
                    # print(f"\n{i}. WHAT AM I???????????? >> {books[i].title} ID: {books[i].id}")
                    books.pop(i)
                    # print(f"\nPOP")
                    break
                    # del books[i]
        # print(f"\nTHESE ARE THE FILTERED BOOKS >>>>>> {books}")
        return books