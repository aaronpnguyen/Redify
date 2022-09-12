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

    link = request.form['link']

    if link:
        try:
            valid = link.index('spotify.com/')
            if valid:
                url = link[valid + 12:]
                urlData = url.split('/')
                print(urlData[0], urlData[1])
                type = urlData[0]
                link = urlData[1]
        except:
            type = ""
            print("not a valid link")

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