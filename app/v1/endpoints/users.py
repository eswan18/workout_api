import os

from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models.user import UserIn, UserOut
from ..auth import get_current_user
from ...db import models as db_models
from ...db import get_db
from app.v1.auth import hash_pw

USER_CREATION_SECRET = os.environ["USER_CREATION_SECRET"]

router = APIRouter(prefix="/users")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(
    user: UserIn,
    secret: str = Body(),
    db: Session = Depends(get_db),
) -> db_models.User:
    """
    Create a new user. Requires a secret string, for now.
    """
    # The worst auth ever, but works until I add a Captcha or something.
    if secret != USER_CREATION_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user creation secret",
        )

    email = user.email
    password = user.password
    hashed_pw = hash_pw(email, password)

    user_record = db_models.User(email=email, pw_hash=hashed_pw)
    try:
        db.add(user_record)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="an account with that email address is already in use",
        )
    db.refresh(user_record)
    return user_record


@router.get("/me", response_model=UserOut)
def get_me(
    current_user: db_models.User = Depends(get_current_user),
) -> UserOut:
    """
    Fetch information about your own user.
    """
    return UserOut(id=current_user.id, email=current_user.email)
