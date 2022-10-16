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
        self.posts = None
        self.topics = None
        self.favorite_tracks = None
        self.favorite_artists = None
    
    # CREATE

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (user_name, email, password) VALUES (%(user_name)s, %(email)s, %(password)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    # GET

    @classmethod
    def get_user_by_name(cls, data):
        query = "SELECT * FROM users WHERE user_name = %(user_name)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return User(results[0])
        return []

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
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
    
    @classmethod
    def update_email(cls, data):
        query = "UPDATE users SET email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update_password(cls, data):
        query = "UPDATE users SET password = %(password)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
        
    # VALIDATION

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['user_name']) < 2: # Checks if the user name is valid
            flash("Invalid user name, must have more than 2 characters.", "user_name")
            is_valid = False
        if User.get_user_by_email(data): # Checks if the email already exists (if its true, it exists)
            flash("This email already exists.", "email")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): # Checks if the email is valid
            flash("Invalid email, please try again.", "email")
            is_valid = False
        if len(data['password']) < 8:
            flash("Invalid password, must be longer than 8 characters.", "password")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match", "password")
            is_valid = False
        
        return is_valid
    
    @staticmethod
    def validate_email_update(data):
        is_valid = True
        if User.get_user_by_email(data):
            flash("This email is already in use.", "email")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): # Checks if the email is valid
            flash("Invalid email, please try again.", "email")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_password_update(data):
        is_valid = True
        if data['new_password'] != data['confirm_new']:
            flash("Passwords do not match", "password")
            is_valid = False
        if len(data['new_password']) < 8:
            flash("Invalid password, must be longer than 8 characters.", "new_password")
            is_valid = False
        return is_valid

