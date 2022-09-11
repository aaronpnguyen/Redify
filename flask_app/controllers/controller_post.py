from flask_app import app
from flask import redirect, render_template, flash, session, request
from flask_app.models.model_topic import Topic
from flask_app.models.model_post import Post

@app.route('/form/post')
def postForm():
    allTopics = Topic.show_all()
    return render_template('postForm.html', topics = allTopics)

@app.route('/submit/form/post', methods=['POST'])
def submitPost():
    data = {
        'title': request.form['title'],
        'message': request.form['message'],
        'topic_id': request.form['topic_id'],
        'user_id': session['user_id']
    }
    Post.create_post(data)
    return redirect('/home')

