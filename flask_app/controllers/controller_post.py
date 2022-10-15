from flask_app import app
from flask import redirect, render_template, session, request
from flask_app.models.model_topic import Topic
from flask_app.models.model_post import Post
from flask_app.models.model_comment import Comment
from flask_app.models.model_user import User

@app.route('/form/post')
def postForm():
    if 'user_id' not in session:
        return redirect('/home')
    user = User.get_user_by_id({'id': session['user_id']})
    allTopics = Topic.get_favorite_topics_by_user_id({'user_id': session['user_id']})
    return render_template('postForm.html', topics = allTopics, user = user)

@app.route('/submit/form/post', methods=['POST'])
def submitPost():
    if 'user_id' not in session:
        return redirect('/home')
    
    if not Post.validate_post(request.form):
        return redirect('/form/post')

    # Breaking down spotify link into digestable (parsed) data for database
    link = request.form['link']
    if link:
        try:
            valid = link.index('spotify.com/')
            if valid:
                url = link[valid + 12:]
                urlData = url.split('/')
                type = urlData[0]
                link = urlData[1]
        except:
            type = ""
            link = ""
    else:
        type = ""
        link = ""

    data = {
        'title': request.form['title'],
        'message': request.form['message'],
        'type': type,
        'link': link,
        'topic_id': request.form['topic_id'],
        'user_id': session['user_id']
    }
    Post.create_post(data)
    return redirect('/home')

@app.route('/post/<int:id>')
def viewPost(id):
    post = Post.get_one_by_id({'id': id})
    if not post:
        return redirect('/home') # If post doesn't exist, return home
    
    comments = Comment.get_comments_for_post({'post_id': id})
    activeCount = Topic.get_active({'id': post.topic_id})
    if 'user_id' in session:
        user = User.get_user_by_id({'id': session['user_id']})
    user = None

    return render_template('onePost.html', post = post, comments = comments, activeCount = activeCount, user = user)

@app.route('/submit/form/comment/<int:post_id>', methods=['POST'])
def submitComment(post_id):
    link = request.form['link']

    if not Comment.validate_comment(request.form):
        return redirect(f'/post/{post_id}')

    # Breaking down spotify link into digestable (parsed) data for database
    if link:
        try:
            valid = link.index('spotify.com/')
            if valid:
                url = link[valid + 12:]
                urlData = url.split('/')
                type = urlData[0]
                link = urlData[1]
        except:
            type = ""
            link = ""
    else:
        type = ""
        link = ""

    data = {
        'message': request.form['message'],
        'type': type,
        'link': link,
        'post_id': post_id,
        'user_id': session['user_id']
    }
    Comment.create_comment(data)
    return redirect(f'/post/{post_id}')