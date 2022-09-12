from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Topic:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.genres = []

    # CREATE

    @classmethod
    def create_topic(cls, data):
        query = "INSERT INTO topics (title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # GET

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM topics"
        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            all_topics = []
            for topic in results:
                all_topics.append(topic)
            return all_topics
        
        return []

    @classmethod
    def get_one_by_title(cls, data):
        query = "SELECT * FROM topics LEFT JOIN posts on posts.topic_id LEFT JOIN users ON posts.user_id WHERE topics.title = %(title)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0])
        
    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM topics WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0])