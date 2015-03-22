# encoding=utf8  
from __future__ import unicode_literals
import os
from markdown import markdown
from flask import Flask, send_file
from flask import render_template
app = Flask(__name__)
app.debug = True

class Post(object):

    @staticmethod
    def path():
        return os.path.join(os.getcwd(), "static", "posts")

    @staticmethod
    def path_for(filename):
        return os.path.join(Post.path(), filename)

    @staticmethod
    def is_post_file(filename):
        return os.path.isfile(Post.path_for(filename)) and filename[0] != "."

    def __init__(self, name):
        self.title = name
        self.filepath = self.path_for(name)
        self.url = '/post/' + name + '.html'
        self.file = open(self.filepath)
        raw_content = self.file.read()
        self.content = markdown(raw_content)

@app.route('/favicon.ico')
def get_favicon():
    return send_file(os.path.join(os.getcwd(), 'favicon.ico'))

@app.route('/static/<subdir>/<filename>')
def get_static_file(subdir, filename):
    return send_file(os.path.join(os.getcwd(), 'static', subdir, filename))

@app.route("/")
def index():
    posts = [ Post(os.path.basename(filename)) for filename in os.listdir(Post.path()) if os.path.isfile(Post.path_for(filename)) ]
    return render_template('index.html', posts=posts)

@app.route("/post/<basename>.html")
def get_formatted_post(basename):
    post = Post(basename)
    return render_template('post.html', title=post.title, content=post.content)


# if not app.debug:
#    import logging
#    from themodule import TheHandlerYouWant
#    file_handler = TheHandlerYouWant(...)
#    file_handler.setLevel(logging.WARNING)
#    app.logger.addHandler(file_handler)
