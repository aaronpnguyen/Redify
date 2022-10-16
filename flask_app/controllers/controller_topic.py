from flask import redirect, session, render_template, request
from flask_app import app
from flask_app.models.model_topic import Topic
from flask_app.models.model_post import Post
from flask_app.models.model_user import User
from flask_app.models.model_comment import Comment

@app.route('/form/topic')
def topicForm():
    if 'user_id' not in session:
        return redirect('/home')
    user = User.get_user_by_id({'id': session['user_id']})
    return render_template('topicForm.html', user = user)

@app.route('/all/topics')
def allTopics():
    topics = Topic.get_all()
    if 'user_id' in session:
        user = User.get_user_by_id({'id': session['user_id']})
    else:
        user = None
    return render_template('topics.html', topics = topics, user = user)

@app.route('/t/<string:topicName>')
def oneTopic(topicName):
    topic = Topic.get_one_by_title({'title': topicName})
    if topic:
        posts = Post.get_post_for_topic({'topic_id': topic.id})
        activeCount = Topic.get_active({'id': topic.id})
    else:
        return redirect('/home')
    # print(posts.topic.title)
    if 'user_id' in session:
        favorited = Topic.check_favorited({'user_id': session['user_id'], 'topic_id': topic.id})
        user = User.get_user_by_id({'id': session['user_id']})
    else:
        favorited = None
        user = None
    return render_template('oneTopic.html', topic = topic, posts = posts, favorited = favorited, user = user, activeCount = activeCount)

@app.route('/submit/form/topic', methods=['POST'])
def submitTopic():
    if 'user_id' not in session:
        return redirect('/home')
    
    if not Topic.validate_topic(request.form):
        return redirect('/form/topic')

    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Topic.create_favorite_topic({
        'topic_id': Topic.create_topic(data),
        'user_id': session['user_id']
    })
    return redirect('/home')

@app.route('/add/favorite/topic/<int:id>', methods=['POST'])
def addFavorite(id):
    if 'user_id' not in session:
        return redirect('/home')

    data = {
        'topic_id': id,
        'user_id': session['user_id']
    }
    Topic.create_favorite_topic(data)
    topic = Topic.get_one_by_id({'id': id})
    return redirect(f'/t/{topic.title}')

@app.route('/remove/favorite/topic/<int:topic_id>', methods = ['POST'])
def removeFavorite(topic_id):
    if 'user_id' not in session:
        return redirect('/home')

    data = {
        'topic_id': topic_id,
        'user_id': session['user_id']
    }
    Topic.delete_favorited(data)
    topic = Topic.get_one_by_id({'id': topic_id})
    return redirect(f'/t/{topic.title}')
