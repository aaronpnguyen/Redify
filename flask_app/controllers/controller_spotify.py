import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask_app import SPOTIFY_APP_ID, SPOTIFY_APP_SECRET, app
import time, os
from flask import redirect, url_for, session, request, render_template, flash
from flask_app.models.model_artist import Artist
from flask_app.models.model_track import Track
from flask_app.models.model_user import User

# SPOTIFY AUTH
app.config['session_spotify'] = 'spotify has logged'
TOKEN_INFO = "session_token"

# After spotify redirects, redirects user to page they originally intended to go to (instead of home)
last_route = ""

def create_spotify_oauth():
    scope = "user-library-read user-top-read"
    return SpotifyOAuth(
        client_id = SPOTIFY_APP_ID,
        client_secret = SPOTIFY_APP_SECRET,
        show_dialog = True,
        redirect_uri = url_for('spotifyRedirect', _external = True),
        scope = scope
    )

def getToken():
    token = session.get(TOKEN_INFO, None)
    if not token:
        raise "exception"
    now = int(time.time())
    expired = token['expires_at'] - now < 60
    if expired:
        sp_oauth = create_spotify_oauth()
        token = sp_oauth.refresh_access_token(token['refresh_token'])
    return token

@app.route('/spotify/login')
def spotifyLogin():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/spotify/redirect')
def spotifyRedirect():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')
    token = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token
    print(token['access_token'])
    return redirect(session['last_route'])
    # return redirect(url_for('home', _external = False))

# User Stats
@app.route('/stats/<string:term>')
def userStats(term):
    try:
        token = getToken()
    except:
        print("spotify has not logged")
        session['last_route'] = "/stats/short_term"
        return redirect(url_for('spotifyLogin', _external = False))
    request = spotipy.Spotify(auth = token['access_token'])

    # Conditionals for the query to run
    if term == "short_term" or term == "medium_term" or term == "long_term":
        term = term
    else:
        term = "short_term"

    # Running query for API call
    topArtists = request.current_user_top_artists(50, 0, term)['items']
    topTracks = request.current_user_top_tracks(50, 0, term)['items']

    artists = []
    tracks = []

    # Parse out data to easily access
    for item in topArtists:
        if item['genres']:
            genre = item['genres'][0]
        else:
            genre = "Unknown genre!"
        details = {
            'artistName': item['name'],
            'artistImage': item['images'][0]['url'],
            'followers': item['followers']['total'],
            'genre': genre
        }
        artists.append(details)

    for item in topTracks:
        details = {
            'songName': item['name'],
            'artistName': item['album']['artists'][0]['name'],
            'songImage': item['album']['images'][2]['url'],
            'songId': item['id']
        }
        tracks.append(details)
    if 'user_id' in session:
        user = User.get_user_by_id({'id': session['user_id']})
    else:
        user = None
    
    print(term)
    # return request.current_user_top_artists(50, 0, term) # Show JSON
    return render_template('stats.html', tracks = tracks, artists = artists, user = user, term = term)

@app.route('/save/spotify_stats', methods=['POST'])
def saveStats():
    user = User.get_user_by_id({'id': session['user_id']})
    try:
        token = getToken()
    except:
        print("spotify has not logged")
        session['last_route'] = f'/profile/{user.user_name}'
        return redirect(url_for('spotifyLogin', _external = False))
    request = spotipy.Spotify(auth = token['access_token'])

    topArtists = request.current_user_top_artists(5, 0, "long_term")['items']
    topTracks = request.current_user_top_tracks(5, 0, "long_term")['items']
    
    allArtists = Artist.get_all_for_user({'user_id': session['user_id']})
    allTracks = Track.get_all_for_user({'user_id': session['user_id']})

    # Conditional to check whether we are updating or saving to database
    if allArtists:
        for i, artist in enumerate(topArtists):
            if artist['genres']:
                genre = artist['genres'][0]
            else:
                genre = "Unkown genre!"
            data = {
                'id': allArtists[i]['id'],
                'artist_name': artist['name'],
                'artist_image': artist['images'][0]['url'],
                'followers': artist['followers']['total'],
                'genre': genre
            }
            Artist.update_artist(data)
    else:
        for artist in topArtists:
            if artist['genres']:
                genre = artist['genres'][0]
            else:
                genre = "Unkown genre!"
            data = {
                'artist_name': artist['name'],
                'artist_image': artist['images'][0]['url'],
                'user_id': session['user_id'],
                'followers': artist['followers']['total'],
                'genre': genre
            }
            Artist.create_artist(data)

    if allTracks:
        for i, track in enumerate(topTracks):
            data = {
                'id': allTracks[i]['id'],
                'track_name': track['name'],
                'track_artist': track['album']['artists'][0]['name'],
                'track_image': track['album']['images'][2]['url'],
                'track_id': track['id'],
            }
            Track.update_track(data)
    else:
        for track in topTracks:
            data = {
                'track_name': track['name'],
                'track_artist': track['album']['artists'][0]['name'],
                'track_image': track['album']['images'][2]['url'],
                'track_id': track['id'],
                'user_id': session['user_id']
            }
            Track.create_track(data)
    return redirect(f'/profile/{user.user_name}')

@app.route('/spotify/logout', methods = ['POST'])
def spotify_logout():
    if 'user_id' not in session:
        return redirect('/')
    
    user = User.get_user_by_id({'id': session['user_id']})
    if os.path.exists(".cache"):
        os.remove(".cache")
    session['last_route'] = None # Removes last route/redirect path
    session['session_token'] = None # Deletes spotify token
    return redirect(f'/settings/{user.user_name}')