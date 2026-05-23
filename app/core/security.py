from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta

from app.core.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    raise NotImplementedError("Available in the full package")


def get_password_hash(password: str) -> str:
    raise NotImplementedError("Available in the full package")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    raise NotImplementedError("Available in the full package")


def create_refresh_token(data: dict) -> str:
    raise NotImplementedError("Available in the full package")


def decode_token(token: str) -> dict:
    raise NotImplementedError("Available in the full package")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    raise NotImplementedError("Available in the full package")


def get_current_active_subscriber(current_user: User = Depends(get_current_user)) -> User:
    raise NotImplementedError("Available in the full package")
