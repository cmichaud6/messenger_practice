from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = 'users_messenger'

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.message = data['message']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (message, user_id) VALUES (%(message)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE user_id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM messages WHERE user_id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM messages WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)