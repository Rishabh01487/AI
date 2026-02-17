"""JWT utilities using PyJWT."""
import jwt
from datetime import datetime, timedelta
from typing import Optional
from ..config import settings

ALGORITHM = "HS256"


def create_access_token(subject: str, expires_minutes: int = 60) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return None
