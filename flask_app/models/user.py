from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email) VALUES(%(first_name)s,%(last_name)s,%(email)s);"
        user_id = connectToMySQL('users').query_db(query,data)
        return user_id

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        result = connectToMySQL('users').query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_one_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        result = connectToMySQL('users').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL('users').query_db(query,data)


    @classmethod
    def delete(cls,data):
        query = "DELETE FROM users WHERE id=%(id)s;"
        return connectToMySQL('users').query_db(query,data)
    
    @staticmethod
    def validate_user(user,users):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name must be at least 3 characters.")
            is_valid = False
        if len(user['email']) < 3:
            flash("Email must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        for new_user in users:
            if (user['email'] == new_user.email):
                flash("Email address needs to be unique")
                is_valid = False
        return is_valid
