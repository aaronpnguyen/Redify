from flask import redirect, session, render_template, request
from flask_app import app
from flask_app.models.model_topic import Topic
from flask_app.models.model_post import Post

@app.route('/form/topic')
def topicForm():
    return render_template('topicForm.html')

@app.route('/all/topics')
def allTopics():
    topics = Topic.get_all()
    return render_template('topics.html', topics = topics)

@app.route('/t/<string:topicName>')
def oneTopic(topicName):
    topic = Topic.get_one_by_title({'title': topicName})
    posts = Post.get_post_for_topic({'topic_id': topic.id})
    return render_template('oneTopic.html', topic = topic, posts = posts)

@app.route('/submit/form/topic', methods=['POST'])
def submitTopic():
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Topic.create_favorite_topic({
        'id': Topic.create_topic(data),
        'user_id': session['user_id']
    })
    return redirect('/home')

# @app.route('/add/favorite/topic', methods=['POST'])
# def addFavorite():
#     data = {
#         'topic_id': request.form[]
#     }
#     return redirect('/home')
