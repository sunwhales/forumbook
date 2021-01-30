from flask import Flask, render_template, request, redirect
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import boto3
import json
import cgi
import requests

form = cgi.FieldStorage()
username =  form.getvalue('username')
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
# db = SQLAlchemy(app)

# aws_access_key_id = YOUR_ACCESS_KEY
# aws_secret_access_key = YOUR_SECRET_KEY
# dynamodb = boto3.resource('dynamodb',endpoint_url="http://localhost:8000")
# dynamodb = boto3.resource('dynamodb',region_name='ap-southeast-2')

# client = boto3.client('apigateway')

class BlogPost:
    def __init__(self,title,content):
        self.title = title
        self.content  = content
        self.author = 'torres'
        self.date_posted = datetime.now()

    def __repr__(self):
        return 'Blog post' + str(self.title)

# class BlogPost(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     author = db.Column(db.String(20), nullable=False, default='N/A')
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
#
#     def __repr__(self):
#         return 'Blog post ' + str(self.id)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/posts', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_author = 'a'
        new_post_url = 'https://l83f8x1esf.execute-api.ap-southeast-2.amazonaws.com/prod/postmessage'
        blog = BlogPost(request.form['title'], request.form['content'])
        data = {'title': blog.title, 'author': blog.author, 'content': blog.content, 'datetime': blog.date_posted}
        # http://localhost:8085/sendjson
        requests.post(url=new_post_url, headers=headers2, data=data, verify=False)
        return redirect('/posts')
    else:
        getmessage_url = 'https://l83f8x1esf.execute-api.ap-southeast-2.amazonaws.com/prod/getmessage'
        resp = requests.get(getmessage_url)
        data = resp.json()

        # all_posts = data.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=data)

@app.route('/posts/delete/<string:title>')
def delete(title):
    headers2 = {'Content-Type': 'application/json'}
    delmes_url = 'https://l83f8x1esf.execute-api.ap-southeast-2.amazonaws.com/prod/deletemessage'
    data = {'title': title}
    # http://localhost:8085/sendjson
    requests.post(url= delmes_url, headers=headers2, data=data, verify=False)

    # post = BlogPost.query.get_or_404(id)
    # db.session.delete(post)
    # db.session.commit()
    return redirect('/posts')

@app.route('/posts/wcount/<string:title>')
def wcount(title):
    headers2 = {'Content-Type': 'application/json'}
    getwcmes_url = 'https://l83f8x1esf.execute-api.ap-southeast-2.amazonaws.com/prod/inputemr'
    data = {'title': title}
    # http://localhost:8085/sendjson
    requests.post(url=getwcmes_url, headers=headers2, data=data, verify=False)
    # post = BlogPost.query.get_or_404(id)
    # message = post.content
    # db.session.delete(post)
    # db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<string:title>', methods=['GET', 'POST'])
def edit(title):
    headers2 = {'Content-Type': 'application/json'}
    if request.method == 'POST':
        editmes_url = 'https://l83f8x1esf.execute-api.ap-southeast-2.amazonaws.com/prod/editmessage'
        blog = BlogPost(title,request.form['content'])
        data = {'title':title,'author':blog.author,'content':blog.content,'datetime':blog.date_posted}
        # http://localhost:8085/sendjson
        requests.post(url=editmes_url, headers=headers2, data=data, verify=False)
        return redirect('/posts')
        # post = BlogPost.query.get_or_404(id)
    else:
        return render_template('edit.html', post=post)

    # if request.method == 'POST':
    #     post.title = request.form['title']
    #     post.author = 'a'
    #     post.content = request.form['content']
    #     db.session.commit()
    #     return redirect('/posts')
    # else:
    #     return render_template('edit.html', post=post)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        headers2 = {'Content-Type': 'application/json'}
        if request.method == 'POST':
            new_post_url = 'https://l83f8x1esf.execute-api.ap-southeast-2.amazonaws.com/prod/postmessage'
            blog = BlogPost(request.form['title'], request.form['content'])
            data = {'title':blog.title,'author':blog.author,'content':blog.content,'datetime':blog.date_posted}
            # http://localhost:8085/sendjson
            requests.post(url=new_post_url, headers=headers2, data = data, verify=False)
            return redirect('/posts')
            # post = BlogPost.query.get_or_404(id)
        else:
            return render_template('edit.html', post=post)
    #     post.title = request.form['title']
    #     post.author = 'a'
    #     post.content = request.form['content']
    #     new_post = BlogPost(title=post_title, content=post_content, author=post_author)
    #     db.session.add(new_post)
    #     db.session.commit()
    #     return redirect('/posts')
    # else:
    #     return render_template('new_post.html')

if __name__ == "__main__":
    app.run(debug=True)