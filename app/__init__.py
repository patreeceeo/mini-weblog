# encoding=utf8  
from __future__ import unicode_literals
import os
import pyth
from markdown import markdown
from flask import Flask, send_file
from flask import render_template
from markdown_embed_media import MarkdownEmbedMedia
app = Flask(__name__)
app.debug=True



class Post(object):

    @staticmethod
    def path():
        return pyth.unix("~/weblog-data/")

    @staticmethod
    def path_for(filename):
        return os.path.join(Post.path(), filename.strip())

    # @staticmethod
    # def is_post_file(filename):
    #     return os.path.isfile(Post.path_for(filename)) and filename[0] != "." and filename.split(".")[1] == "txt"

    def __init__(self, filename):
        without_extension = filename.split(".")[0]
        self.title = without_extension
        self.filepath = self.path_for(filename)
        self.url = '/post/' + without_extension + '.html'
        self.file = open(self.filepath)
        raw_content = self.file.read()
        self.content = markdown(raw_content.decode("utf-8"), extensions=[MarkdownEmbedMedia(), 'markdown.extensions.smarty'])

@app.route('/favicon.ico')
def get_favicon():
    return send_file(os.path.join(os.getcwd(), 'favicon.ico'))

@app.route('/static/<subdir>/<filename>')
def get_static_file(subdir, filename):
    return send_file(os.path.join(pyth.unix("~/weblog-static/"), "static", subdir, filename))

@app.route("/")
def index():
    posts = [ Post(filename) for filename in open(pyth.unix("~/weblog-data/index.txt")).readlines() ]
    return render_template('index.html', posts=posts)

@app.route("/post/<slug>.html")
def get_formatted_post(slug):
    post = Post(slug + ".txt")
    filenames = [ filename.strip() for filename in open(pyth.unix("~/weblog-data/index.txt")).readlines() ]
    post_index = filenames.index(slug + ".txt")
    if post_index > 0:
        post_prev = Post(filenames[post_index - 1])
    else:
        post_prev = None

    if post_index < len(filenames) - 1:
        post_next = Post(filenames[post_index + 1])
    else:
        post_next = None
    return render_template('post.html', title=post.title, content=post.content, post_prev=post_prev, post_next=post_next)

# if not app.debug:
#    import logging
#    from themodule import TheHandlerYouWant
#    file_handler = TheHandlerYouWant(...)
#    file_handler.setLevel(logging.WARNING)
#    app.logger.addHandler(file_handler)
