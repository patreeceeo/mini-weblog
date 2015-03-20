from flask import Flask
from flask import render_template
app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return "Hello, world! (I'm using Flask!)"

@app.route("/post/<basename>.html")
def get_formatted_post(basename):
    import os
    from markdown import markdown
    markdown_content = open("{cwd}/static/posts/{basename}.txt".format(cwd=os.getcwd(), basename=basename)).read()
    return render_template('post.html', title=basename, content=markdown(markdown_content))

# if not app.debug:
#    import logging
#    from themodule import TheHandlerYouWant
#    file_handler = TheHandlerYouWant(...)
#    file_handler.setLevel(logging.WARNING)
#    app.logger.addHandler(file_handler)
