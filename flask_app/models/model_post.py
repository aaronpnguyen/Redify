from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import model_user
from flask_app.models import model_topic
from flask import flash

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.message = data['message']
        self.type = data['type']
        self.link = data['link']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        self.topic_id = data['topic_id']
        self.topic = None
    
    # CREATE

    @classmethod
    def create_post(cls, data):
        query = "INSERT INTO posts (title, message, type, link, user_id, topic_id) VALUES (%(title)s, %(message)s, %(type)s, %(link)s, %(user_id)s, %(topic_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # GET

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM topics LEFT JOIN posts ON posts.topic_id WHERE posts.user_id = %(user_id)s AND posts.title = %(title)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return Post(results[0])
    
    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id LEFT JOIN topics ON posts.topic_id = topics.id WHERE posts.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            post = cls(results[0])
            user_data = {
                'id': post.user_id
            }
            topic_data = {
                'id': post.topic_id
            }
            post.user = model_user.User.get_user_by_id(user_data)
            post.topic = model_topic.Topic.get_one_by_id(topic_data)
            return post
        return Post(results[0])
    
    @classmethod
    def get_post_for_topic(cls, data):
        query = "SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id WHERE topic_id = %(topic_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if results:
            all_posts = []
            for data in results:
                post = cls(data)
                user_data = {
                    'id': data['users.id']
                }
                user = model_user.User.get_user_by_id(user_data)
                post.user = user
                all_posts.append(post)
            return all_posts
        return []
    
    @classmethod
    def get_posts_for_user(cls, data):
        query = "SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id LEFT JOIN topics ON posts.topic_id = topics.id WHERE users.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            all_posts = []
            for data in results:
                post = cls(data)
                user_data = {
                    'id': data['users.id']
                }
                topic_data = {
                    'id': data['topics.id']
                }
                post.user = model_user.User.get_user_by_id(user_data)
                post.topic = model_topic.Topic.get_one_by_id(topic_data)
                all_posts.append(post)
            return all_posts
        return []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts LEFT JOIN topics ON posts.topic_id = topics.id LEFT JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC"
        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            all_posts = []
            for data in results:
                post = cls(data)
                topic_data = {
                    'id': data['topic_id']
                }
                user_data = {
                    'id': data['user_id']
                }
                user = model_user.User.get_user_by_id(user_data)
                topic = model_topic.Topic.get_one_by_id(topic_data)
                post.user = user
                post.topic = topic
                all_posts.append(post)
            return all_posts
        return []

    @classmethod
    def show_favorite_posts(cls, data):
        query = "SELECT * FROM favorite_topics LEFT JOIN topics ON favorite_topics.topic_id = topics.id LEFT JOIN posts ON posts.topic_id = favorite_topics.topic_id WHERE favorite_topics.user_id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if results:
            all_posts = []
            for data in results:
                post = Post(data)
                topic_data = {
                    'id': data['topic_id']
                }
                user_data = {
                    'id': data['user_id']
                }
                post.topic = model_topic.Topic.get_one_by_id(topic_data)
                post.user = model_user.User.get_user_by_id(user_data)
                all_posts.append(post)
                print(post.user.user_name)
                print(post.topic.title)
            return all_posts
        return []