from .. import models, schemas
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Tuple, Optional
from .. import oauth2

router = APIRouter(prefix="/posts", tags=["Posts"])


# , response_model=List[schemas.PostOut]
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = "",
):
    # posts = (
    #     db.query(models.Post)
    #
    # )

    # Votes Default=> Left inner join
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                                         models.Vote.post_id == models.Post.id,
                                                                                         isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    # print(posts.all())
    # print(results.all())
    # print(type(results.all()))
    # print(type(results.first()))
    # print([row._asdict() for row in results.all()])

    return posts.all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
        post: schemas.PostCreate,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(user_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/latest", response_model=schemas.Post)
def get_latest_post(
        db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).all()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found"
        )
    return post[-1]


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
        id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user),
):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                                         models.Vote.post_id == models.Post.id,
                                                                                         isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        id: int,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


"""
id & post are the data that we recieve from the frontend
"""


@router.put("/{id}", response_model=schemas.Post)
def update_post(
        id: int,
        post: schemas.PostCreate,
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    curr_post = post_query.first()

    if not curr_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found"
        )
    if curr_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform"
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
