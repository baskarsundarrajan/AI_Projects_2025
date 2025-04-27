from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from .schema import User
from services.firebase_auth import verify_user_token
from firebase_admin import auth
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()


@router.post("/user/register")
def resigter_user(user: User):
    try:
        user = auth.create_user(email=user.username, password=user.password)

        return JSONResponse(
            content={
                "message": f"User account created successfuly for user {user.uid}"
            },
            status_code=201,
        )
    except auth.EmailAlreadyExistsError as _:
        raise HTTPException(
            status_code=400,
            detail=f"Account already created for the email {user.username}",
        ) from _
        
def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        # print(token)
        user = verify_user_token(token)
        # print(user)

        return user["user_id"]
    except auth.ExpiredIdTokenError as e:
        raise HTTPException(status_code=400, detail="Token Expried") from e