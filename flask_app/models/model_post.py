from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import model_user
from flask import flash

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.message = data['message']
        self.link = data['link']
        self.liked = 0
        self.genre = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        self.topic_id = data['topic_id']
    
    # CREATE

    @classmethod
    def create_post(cls, data):
        query = "INSERT INTO posts (title, message, type, link, user_id, topic_id) VALUES (%(title)s, %(message)s, %(type)s, %(link)s, %(user_id)s, %(topic_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM topics LEFT JOIN posts on posts.topic_id WHERE posts.user_id = %(user_id)s AND posts.title = %(title)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_post_for_topic(cls, data):
        query = "SELECT * FROM posts LEFT JOIN users on posts.user_id WHERE topic_id = %(topic_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if results:
            all_posts = []
            for data in results:
                post = cls(data)
                user_data = {
                    'id': data['user_id']
                }
                user = model_user.User.get_user_by_id(user_data)
                post.user = user
                all_posts.append(post)
            return all_posts
        return []

    @classmethod
    def show_all(cls):
        query = "SELECT * FROM posts ORDER BY created_at DESC"
        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            all_posts = []
            for post in results:
                all_posts.append(post)
            return all_posts
        return []