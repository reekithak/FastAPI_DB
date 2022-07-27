from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils
from ..oauth2 import *

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_cred.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN_NOT_FOUND, detail="Invalid Credentials")
    if not utils.verify_pass(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN_NOT_FOUND, detail="Invalid Credentials")

    # Create a token, incase it's all right, return token.
    access_token = create_access_token(data={"user_id": user.id
                                             })
    print(access_token)
    return {"Access Token": access_token,
            "Token Type": "bearer"}
