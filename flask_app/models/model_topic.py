from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import model_user

class Topic:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    # CREATE

    @classmethod
    def create_topic(cls, data):
        query = "INSERT INTO topics (title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def create_favorite_topic(cls, data):
        query = "INSERT INTO favorite_topics (topic_id, user_id) VALUES (%(topic_id)s, %(user_id)s);"
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
        query = "SELECT * FROM topics LEFT JOIN users ON topics.user_id = users.id WHERE topics.title = %(title)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            topic = cls(results[0])
            user_data = {
                'id': topic.user_id
            }
            topic.user = model_user.User.get_user_by_id(user_data)
            return topic
        return []
        
    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM topics WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_favorite_topics_by_user_id(cls, data):
        query = "SELECT * FROM favorite_topics LEFT JOIN topics ON topic_id = topics.id WHERE favorite_topics.user_id = %(user_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            all_favorites = []
            for favorite in results:
                all_favorites.append(favorite)
            return all_favorites
        return []
    
    @classmethod
    def get_top_5_topics(cls):
        query = "SELECT *, COUNT(topic_id) FROM favorite_topics LEFT JOIN topics ON favorite_topics.topic_id = topics.id GROUP BY topic_id ORDER BY COUNT(topic_id) DESC LIMIT 5"
        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            top_topics = []
            for topic in results:
                top_topics.append(topic)
            return top_topics
        return []

    @classmethod
    def check_favorited(cls, data):
        query = "SELECT * FROM favorite_topics LEFT JOIN topics on topics.id = favorite_topics.topic_id WHERE favorite_topics.user_id = %(user_id)s AND topic_id = %(topic_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return Topic(results[0])
        return None
    
    @classmethod
    def get_active(cls, data):
        query = "SELECT * FROM favorite_topics WHERE topic_id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)

        return len(results)

    @classmethod
    def delete_favorited(cls, data):
        query = "DELETE FROM favorite_topics WHERE topic_id = %(topic_id)s AND user_id = %(user_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)
            