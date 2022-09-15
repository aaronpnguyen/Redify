from flask_app import app
from flask import redirect, render_template, session, request
from flask_app.models.model_topic import Topic
from flask_app.models.model_post import Post
from flask_app.models.model_comment import Comment

@app.route('/form/post')
def postForm():
    if 'user_id' not in session:
        return redirect('/home')
    allTopics = Topic.get_all()
    return render_template('postForm.html', topics = allTopics)

@app.route('/submit/form/post', methods=['POST'])
def submitPost():
    if 'user_id' not in session:
        return redirect('/home')
        
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
            type = type
            link = link
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
    if post:
        comments = Comment.get_comments_for_post({'post_id': id})
    else:
        return redirect('/home')
    return render_template('onePost.html', post = post, comments = comments)