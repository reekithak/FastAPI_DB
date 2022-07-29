from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "title1", "content": "content1", "id": 1},
    {"title": "title2", "content": "content2", "id": 2},
]


def get_id(id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "hello"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    return {"latest post": my_posts[-1]}


# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     curr_post = [p for p in my_posts if p["id"] == int(id)]
#     if not curr_post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f"post with {id} not found"}
#     return curr_post


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    curr_post = [p for p in my_posts if p["id"] == int(id)]
    if not curr_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found"
        )
    return curr_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    curr_post = [p for p in my_posts if p["id"] == int(id)]
    if not curr_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found"
        )
    my_posts.pop(get_id(id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


"""
id & post are the data that we recieve from the frontend
"""


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index_ = get_id(id)
    curr_post = [p for p in my_posts if p["id"] == int(id)]
    if not curr_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found"
        )
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index_] = post_dict
    return {"data": post_dict}
