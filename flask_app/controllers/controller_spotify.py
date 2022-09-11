from ftplib import all_errors
from logging import NullHandler
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask_app import SPOTIFY_APP_ID, SPOTIFY_APP_SECRET, app
import time
from flask import redirect, url_for, session, request, render_template, flash
from flask_app.models.model_artist import Artist

# SPOTIFY AUTH
app.config['session_spotify'] = 'spotify has logged'
TOKEN_INFO = "session_token"

def create_spotify_oauth():
    scope = "user-library-read user-top-read"
    return SpotifyOAuth(
        client_id = SPOTIFY_APP_ID,
        client_secret = SPOTIFY_APP_SECRET,
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
    return redirect(url_for('home', _external = False))

# This is a user's profile
@app.route('/stats/<string:term>')
def userStats(term):
    try:
        token = getToken()
    except:
        print("spotify has not logged")
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
        details = {
            'artistName': item['name'],
            'artistImage': item['images'][0]['url']
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
    
    # return request.current_user_top_artists(50, 0, term) # Show JSON
    return render_template('profile.html', tracks = tracks, artists = artists)

@app.route('/save/spotify_stats', methods=['POST'])
def saveStats():
    try:
        token = getToken()
    except:
        print("spotify has not logged")
        return redirect(url_for('spotifyLogin', _external = False))
    request = spotipy.Spotify(auth = token['access_token'])

    topArtists = request.current_user_top_artists(5, 0, "long_term")['items']
    topTracks = request.current_user_top_tracks(5, 0, "long_term")['items']
    
    allArtists = Artist.show_all_for_user({'user_id': session['user_id']})

    # Conditional to check whether we are updating or saving to database
    if allArtists:
        for i, artist in enumerate(topArtists):
            data = {
                'id': allArtists[i]['id'],
                'artist_name': artist['name'],
                'artist_image': artist['images'][0]['url']
            }
            Artist.update_artist(data)
    else:
        for artist in topArtists:
            data = {
                'artist_name': artist['name'],
                'artist_image': artist['images'][0]['url'],
                'user_id': session['user_id']
            }
            Artist.create_artist(data)

    return redirect('/home')
