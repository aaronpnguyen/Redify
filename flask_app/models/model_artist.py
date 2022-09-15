from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Artist:
    def __init__(self, data):
        self.id = data['id']
        self.artist_name = data['artist_name']
        self.artist_image = data['artist_image']
        self.followers = data['followers']
        self.genre = data['genre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    # CREATE

    @classmethod
    def create_artist(cls, data):
        query = "INSERT INTO favorite_artists (artist_name, artist_image, followers, genre, user_id) VALUES (%(artist_name)s, %(artist_image)s, %(followers)s, %(genre)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def show_all(cls):
        query = "SELECT * FROM favorite_artists"
        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            all_artists = []
            for artist in results:
                all_artists.append(artist)
            return all_artists
        return []
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM favorite_artists WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_all_for_user(cls, data):
        query = "SELECT * FROM favorite_artists WHERE user_id = %(user_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            all_artists = []
            for artist in results:
                all_artists.append(artist)
            return all_artists
        return []

    @classmethod
    def update_artist(cls, data):
        query = "UPDATE favorite_artists SET artist_name = %(artist_name)s, artist_image = %(artist_image)s, followers = %(followers)s, genre = %(genre)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
        