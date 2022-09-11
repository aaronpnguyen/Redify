from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Track:
    def __init__(self, data):
        self.id = data['id']
        self.track_name = data['track_name']
        self.track_artist = data['track_artist']
        self.track_id = data['track_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    # CREATE

    @classmethod
    def create_track(cls, data):
        query = "INSERT INTO favorite_tracks (track_name, track_artist, track_id, user_id) VALUES (%(track_name)s, %(track_artist)s, %(track_id)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)