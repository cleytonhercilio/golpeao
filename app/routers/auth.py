from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
import bcrypt

from app.config import settings
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, Token, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@router.post("/register", response_model=UserOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(400, "Username já em uso")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email já em uso")
    user = User(
        username=data.username,
        email=data.email,
        password_hash=_hash_password(data.password),
        display_name=data.display_name,
        avatar_emoji=data.avatar_emoji,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not _verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    return Token(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
