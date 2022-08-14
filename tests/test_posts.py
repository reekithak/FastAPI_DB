from typing import List

import pytest

from ..app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    # posts = schemas.PostOut(res.json()) (loop in this, list comprehension)
    posts_lists = list(map(validate, res.json()))
    print(res.json())

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    # assert posts_lists[0].Post.id == test_posts[0].id . # You've ti setup order in which post is fetched


def test_unauth_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauth_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/124242")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert res.status_code == 200
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("soemthing different", "dayum", False),
    ("some thing random", "awesome random content", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title,
                                                  "content": content,
                                                  "published": published})
    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]


def test_create_posts_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "asdasf",
                                                  "content": "fasasfsa"
                                                  })
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "asdasf"
    assert created_post.content == "fasasfsa"
    assert created_post.published == True
    assert created_post.user_id == test_user["id"]


def test_unauth_user_create_post(client, test_posts, test_user):
    res = client.post(f"/posts/",
                      json={"title": "ansfnsf",
                            "content": "fsfhbdsjfbds"})
    assert res.status_code == 401
