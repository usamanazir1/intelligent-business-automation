"""Authentication endpoints.

Provides the OAuth2 password flow used to obtain a JWT access token.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.security import create_access_token, decode_access_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    username: str
    roles: list[str]


# Placeholder user store — replace with a database-backed repository.
_DEMO_USERS: dict[str, dict] = {
    "admin": {"password": "admin", "roles": ["admin", "automator"]},
}


@router.post("/login", response_model=TokenResponse, summary="Obtain access token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    """Exchange credentials for a signed JWT access token."""
    user = _DEMO_USERS.get(form_data.username)
    if user is None or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tokens_expires_in_s = 1_800
    token = create_access_token(
        subject=form_data.username, extra_claims={"roles": user["roles"]}
    )
    return TokenResponse(access_token=token, expires_in=tokens_expires_in_s)


@router.get("/users/me", response_model=UserResponse, summary="Current user")
async def read_me(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """Return the profile of the user identified by the bearer token."""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserResponse(username=payload["sub"], roles=payload.get("roles", []))
