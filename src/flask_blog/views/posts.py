from flask import Blueprint, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

from ..database import db
from ..models import Post, Tag
from ..utils import find_or_create_tags, tags_to_string

posts = Blueprint("posts", __name__)


@posts.route("/")
def index():
    created_at = request.args.get('created_at')
    query = Post.query
    if not created_at:
        posts = query.all()
    else:
        posts = query.filter(Post.created_at == created_at)
    tags = Tag.query.all()
    return render_template("index.html", posts=posts, tags=tags)


@posts.route("/<int:post_id>")
def post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    tags = post.tags
    return render_template("post.html", post=post, tags=tags)


@posts.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        tag_names = request.form["tags"]

        tags = find_or_create_tags(tag_names)

        if not title:
            flash("Title is required!")
        else:
            new_post = Post(title=title, content=content, tags=tags)

            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for("posts.index"))
    return render_template("create.html")


@posts.route("/<int:post_id>/edit", methods=("GET", "POST"))
def edit(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        tag_names = request.form["tags"]

        tags = find_or_create_tags(tag_names)

        if not title:
            flash("Title is required!")
        else:
            post.title = title
            post.content = content
            post.tags = tags

            db.session.commit()

            return redirect(url_for("posts.index"))

    tags_string = tags_to_string(post.tags)
    return render_template("edit.html", post=post, tags_string=tags_string)


@posts.route("/<int:post_id>/delete", methods=("POST",))
def delete(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)

    db.session.delete(post)
    db.session.commit()

    flash('"{}" was successfully deleted!'.format(post.id))
    return redirect(url_for("posts.index"))


@posts.route("/tag/<string:tag_name>")
def tag(tag_name):
    tag = Tag.query.filter(Tag.name == tag_name).first()
    if not tag:
        abort(404)
    posts = tag.posts
    print(posts, tag)
    return render_template("tag.html", posts=posts, tag=tag)
