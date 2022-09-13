from flask_app import app
from flask import redirect, render_template, flash, session, request
from flask_app.models import model_user, model_post, model_track, model_artist
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/home')

# LOGIN/REGISTRATION

@app.route('/login/user')
def login_user():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():

    data = {
        'user_name': request.form['user_name'],
        'password': request.form['password']
    }
    user = model_user.User.get_user_by_name(data)

    if not user:
        flash("Invalid username")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid password")
        return redirect('/')
    session['user_id'] = user.id

    print(user.id)

    return redirect('/home')

@app.route('/register/user')
def register_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_user():
    if not model_user.User.validate_user(request.form):
        return redirect('/register/user')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'user_name': request.form['user_name'],
        'email': request.form['email'],
        'password': pw_hash
    }

    user_id = model_user.User.create_user(data)
    session['user_id'] = user_id

    return redirect('/spotify/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/home')
def home():
    if 'user_id' in session:
        data = {
            'id': session['user_id']
        }
        user = model_user.User.get_user_by_id(data)
    else:
        user = None
    posts = model_post.Post.get_all()
    return render_template('home.html', user = user, posts = posts)

@app.route('/profile/<string:username>')
def profile(username):
    user = model_user.User.get_user_by_name({'user_name': username})
    favorite_tracks = model_track.Track.get_all_for_user({'user_id': user.id})
    favorite_artists = model_artist.Artist.get_all_for_user({'user_id': user.id})
    return render_template('profile.html', user = user, tracks = favorite_tracks, artists = favorite_artists)
