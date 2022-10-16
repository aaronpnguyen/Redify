from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Track:
    def __init__(self, data):
        self.id = data['id']
        self.track_name = data['track_name']
        self.track_artist = data['track_artist']
        self.track_image = data['track_image']
        self.track_id = data['track_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    # CREATE

    @classmethod
    def create_track(cls, data):
        query = "INSERT INTO favorite_tracks (track_name, track_artist, track_image, track_id, user_id) VALUES (%(track_name)s, %(track_artist)s, %(track_image)s, %(track_id)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # GET

    @classmethod
    def get_all_for_user(cls, data):
        query = "SELECT * FROM favorite_tracks WHERE user_id = %(user_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            all_tracks = []
            for track in results:
                all_tracks.append(track)
            return all_tracks
        return []
    
    # UPDATE

    @classmethod
    def update_track(cls, data):
        query = "UPDATE favorite_tracks SET track_name = %(track_name)s, track_artist = %(track_artist)s, track_image = %(track_image)s, track_id = %(track_id)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

'''
    Queries created by Aaron Nguyen
    https://www.linkedin.com/in/aaronpnguyen/
'''