import flask

from datetime import datetime
from flask_blog import models
from flask_blog.database import db
from urllib.parse import quote

NO_POSTS_MESSAGE = b"No posts here so far."


def test_empty_db(client):
    rv = client.get("/")
    assert NO_POSTS_MESSAGE in rv.data


def test_create_post(app_context, client):
    title = "Test Post"
    content = "This is a test"
    rv = client.post(
        "/create",
        data=dict(title=title, content=content, tags="foo, bar"),
        follow_redirects=True,
    )
    assert flask.request.path == "/"
    assert NO_POSTS_MESSAGE not in rv.data
    assert title.encode() in rv.data

    posts = models.Post.query.all()
    assert len(posts) == 1
    assert posts[0].title == title
    assert posts[0].content == content
    assert len(posts[0].tags) == 2
    assert posts[0].tags[0].name == "foo"
    assert posts[0].tags[1].name == "bar"

def test_edit_post(app_context, client):
    tag = models.Tag(name="foo")
    post = models.Post(title="Test Post", content="This is a test", tags=[tag])

    db.session.add(post)
    db.session.commit()

    client.post(
        f"{post.id}/edit",
        data=dict(title="New Title", content="New content", tags="bar"),
        follow_redirects=True,
    )

    posts = models.Post.query.all()
    assert len(posts) == 1
    assert posts[0].title == "New Title"
    assert posts[0].content == "New content"
    assert len(posts[0].tags) == 1
    assert posts[0].tags[0].name == "bar"


def test_delete_post(app_context, client):
    post = models.Post(title="Test Post", content="This is a test")

    db.session.add(post)
    db.session.commit()

    client.post(
        f"{post.id}/delete",
        data=dict(),
        follow_redirects=True,
    )

    posts = models.Post.query.all()
    assert len(posts) == 0

def test_filter_tag(app_context, client):
    tag = models.Tag(name="foo")
    post = models.Post(title="Test Post", content="This is a test", tags=[tag])

    db.session.add(post)
    db.session.commit()

    rv = client.get("/tag/foo")
    assert b"Test Post" in rv.data

def test_filter_created_at(app_context, client):
    post = models.Post(title="Test Post", content="This is a test")

    db.session.add(post)
    db.session.commit()

    created_at = quote(post.created_at.strftime('%Y-%m-%d+%H:%M:%S.%f'), '+')

    rv = client.get("/?created_at=" + created_at)
    assert b"Test Post" in rv.data