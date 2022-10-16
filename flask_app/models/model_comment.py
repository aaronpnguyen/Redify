from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import model_user

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.message = data['message']
        self.type = data['type']
        self.link = data['link']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.user = None

    @classmethod
    def create_comment(cls, data):
        query = "INSERT INTO comments (message, type, link, user_id, post_id) VALUES (%(message)s, %(type)s, %(link)s, %(user_id)s, %(post_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_comments_for_post(cls, data):
        query = "SELECT * FROM comments LEFT JOIN users ON comments.user_id = users.id WHERE post_id = %(post_id)s ORDER BY comments.created_at DESC"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            all_comments = []
            for data in results:
                comment = cls(data)
                user_data = {
                    'id': data['users.id']
                }
                comment.user = model_user.User.get_user_by_id(user_data)
                all_comments.append(comment)
            return all_comments
        return []
    
    @staticmethod
    def validate_comment(data):
        is_valid = True
        if len(data['message']) < 2:
            flash("Message must contain more than 2 characters!", "message")
            is_valid = False
        if data['link']:
            if 'spotify' not in data['link']:
                flash("Invalid spotify link!", "link")
                is_valid = False
        return is_valid

'''
    Queries created by Aaron Nguyen
    https://www.linkedin.com/in/aaronpnguyen/
'''