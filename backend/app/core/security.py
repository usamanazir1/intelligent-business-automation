"""Security helpers: password hashing and JWT token issuance/validation."""

from datetime import datetime, timedelta, timezone
from typing import cast

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

settings = get_settings()


def hash_password(plain_password: str) -> str:
    """Return a bcrypt hash for the given plaintext password."""
    return cast(str, pwd_context.hash(plain_password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return ``True`` if the plaintext matches the stored hash."""
    return cast(bool, pwd_context.verify(plain_password, hashed_password))


def create_access_token(subject: str, extra_claims: dict | None = None) -> str:
    """Create a signed JWT access token for the given subject (username)."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload: dict = {"sub": subject, "exp": expire}
    if extra_claims:
        payload.update(extra_claims)
    return cast(
        str, jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    )


def decode_access_token(token: str) -> dict | None:
    """Decode and validate a JWT. Returns the payload or ``None`` if invalid."""
    try:
        return cast(
            dict,
            jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm]),
        )
    except JWTError:
        return None
