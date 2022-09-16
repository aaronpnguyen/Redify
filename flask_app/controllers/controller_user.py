from flask_app import app
from flask import redirect, render_template, flash, session, request
from flask_app.controllers.controller_spotify import TOKEN_INFO
from flask_app.models import model_user, model_post, model_track, model_artist, model_topic
from flask_bcrypt import Bcrypt
import os

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
        return redirect('/login/user')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid password")
        return redirect('/login/user')
    session['user_id'] = user.id

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

    return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    if os.path.exists(".cache"):
        os.remove(".cache")
    return redirect('/')

@app.route('/home')
def home():
    if 'user_id' in session:
        data = {
            'id': session['user_id']
        }
        user = model_user.User.get_user_by_id(data)
        topics = model_topic.Topic.get_favorite_topics_by_user_id({'user_id': session['user_id']})
        userFeed = model_post.Post.show_favorite_posts(data)
    else:
        user = None
        topics = model_topic.Topic.get_top_5_topics()
        userFeed = None
        
    posts = model_post.Post.get_all()
    return render_template('home.html', user = user, posts = posts, topics = topics, userFeed = userFeed)

@app.route('/profile/<string:username>')
def profile(username):
    user = model_user.User.get_user_by_name({'user_name': username})
    favorite_tracks = model_track.Track.get_all_for_user({'user_id': user.id})
    favorite_artists = model_artist.Artist.get_all_for_user({'user_id': user.id})
    posts = model_post.Post.get_posts_for_user({'id': user.id})
    return render_template('profile.html', user = user, tracks = favorite_tracks, artists = favorite_artists, posts = posts)

@app.route('/settings/<string:username>')
def settings(username):
    if 'user_id' not in session:
        return redirect('/home')

    user = model_user.User.get_user_by_name({'user_name': username})
    if session['user_id'] is not user.id:
        return redirect('/home')
        
    return render_template('settings.html', user = user)

@app.route('/update/email/<int:id>', methods = ['POST'])
def updateEmail(id):
    user = model_user.User.get_user_by_id({'id': id})

    if 'user_id' in session != user.id:
        return redirect(f'/settings/{user.user_name}')

    if not model_user.User.validate_email_update(request.form):
        return redirect(f'/settings/{user.user_name}')

    model_user.User.update_email({
        'id': id,
        'email': request.form['email']
    })
    return redirect(f'/settings/{user.user_name}')

@app.route('/update/password/<int:id>', methods = ['POST'])
def updatePassword(id):
    user = model_user.User.get_user_by_id({'id': id})

    if 'user_id' in session != user.id:
        return redirect('home')
    if not model_user.User.validate_password_update(request.form):
        return redirect(f'/settings/{user.user_name}')
    if not bcrypt.check_password_hash(user.password, request.form['old_password']):
        flash("Invalid password")
        return redirect(f'/settings/{user.user_name}')

    pw_hash = bcrypt.generate_password_hash(request.form['new_password'])
    model_user.User.update_password({
        'id': id,
        'password': pw_hash
    })
    return redirect(f'/settings/{user.user_name}')