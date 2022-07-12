from fastapi import FastAPI, Response, status, HTTPException, Depends
# from fastapi.params import Body
from pydantic import BaseModel
# from typing import Optional
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='123456', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection Established")
        break
    except Exception as e:
        print("Connection to DB Failed")
        print(e)
        time.sleep(2)

my_posts = [{"title": "title1",
             "content": "content1",
             "id": 1},
            {"title": "title2",
             "content": "content2",
             "id": 2}
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
    cursor.execute("""SELECT * from posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title,
                    post.content,
                    post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {
        "data": new_post
    }


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * from posts ORDER BY created_at desc LIMIT 1""")
    return {
        "latest post": my_posts[-1]
    }


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * from  posts WHERE id=%s """, str(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found")
    return {"post detail": post
            }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE from posts WHERE id=%s RETURNING *""", str(id))
    post = cursor.fetchall()
    conn.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


'''
id & post are the data that we recieve from the frontend
'''


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s  WHERE id=%s RETURNING *""", (
        post.title,
        post.content,
        post.published,
        str(id)
    ))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found")
    return {"data": post}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "Success"}
