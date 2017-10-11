from flask import Flask, render_template, request, abort, redirect

import models

app = Flask(__name__)

@app.route("/")
def index():
    page = models.get_page_info()
    return render_template("index.html", page=page)

@app.route("/posts/new")
def new():
    return render_template("new.html")

@app.route("/posts", methods=["POST"])
def create_post():
    postContents = request.form['postContents']
    createOption = request.form['createOption']
    if not (postContents and createOption) :
        abort(400)

    if createOption == "createAndPublish":
        publish = True
    else:
        publish = False

    models.create_post(postContents, publish)

    if publish:
        return redirect("/posts")
    else:
        return redirect("/unpublished_posts")

@app.route("/posts", methods=["GET"])
def get_posts():
    posts = models.get_posts()
    return render_template("posts.html", posts=posts)

@app.route("/unpublished_posts", methods=["GET"])
def get_unpublished_posts():
    posts = models.get_posts(unpublished=True)
    return render_template("posts.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0', threaded=True)
