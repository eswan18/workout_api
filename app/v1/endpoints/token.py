from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.v1.models.token import Token
from app.v1.auth import authenticate_user, create_token_payload
from app import db


router = APIRouter(prefix="/token")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db.get_db),
) -> dict[str, str]:
    user = authenticate_user(form_data.username, form_data.password, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_token_payload(user.email, form_data, db)
