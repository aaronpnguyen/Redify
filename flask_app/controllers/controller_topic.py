from flask import redirect, url_for, session, render_template, flash, request
from flask_app import app
from flask_app.models.model_topic import Topic

@app.route('/form/topic')
def topicForm():
    return render_template('topicForm.html')

@app.route('/all/topics')
def allTopics():
    topics = Topic.show_all()
    return render_template('topics.html', topics = topics)

@app.route('/submit/form/topic', methods=['POST'])
def submitTopic():
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Topic.create_topic(data)
    return redirect('/home')