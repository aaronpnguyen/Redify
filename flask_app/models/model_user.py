from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r"^[a-zA-z,'-. ]{2,50}$")
PASSWORD_REGEX = re.compile(r"")

class User:
    def __init__(self, data):
        self.id = data['id']
        self.user_name = data['user_name']
        self.email = data['email']
        self.password = data['password'] # This should be hashed
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []
        self.topics = []
    
    # CREATE

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (user_name, email, password) VALUES (%(user_name)s, %(email)s, %(password)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    # GET

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE user_name = %(user_name)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            all_users = []
            for user in results:
                all_users.append(cls(user))
            return User(results[0])
        return []

    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE user_name = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            all_users = []
            for user in results:
                all_users.append(cls(user))
            return User(results[0])
        return []
    
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return User(results[0])
            
    # VALIDATION

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['user_name']) < 2: # Checks if the user name is valid
            flash("Invalid user name, must have more than 2 characters.")
            is_valid = False
        if User.get_email(data): # Checks if the email already exists (if its true, it exists)
            flash("This email already exists.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): # Checks if the email is valid
            flash("Invalid email, please try again.")
            is_valid = False
        if len(data['password']) < 8:
            flash("Invalid password, must be longer than 8 characters.")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match")
            is_valid = False
        
        return is_valid
