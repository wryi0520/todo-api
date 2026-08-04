import psycopg
from fastapi import APIRouter, Depends, HTTPException, status

from app import crud
from app.db import get_db
from app.deps import get_current_user
from app.schemas import Token, UserCreate, UserLogin, UserOut
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, conn: psycopg.Connection = Depends(get_db)):
    if crud.get_user_by_username(conn, user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    if crud.get_user_by_email(conn, user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(conn, user)


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, conn: psycopg.Connection = Depends(get_db)):
    user = crud.get_user_by_username(conn, credentials.username)
    if user is None or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return Token(access_token=create_access_token(user["id"]))


@router.get("/me", response_model=UserOut)
def me(current_user: dict = Depends(get_current_user)):
    return current_user
