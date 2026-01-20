from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os


# JWT Configuration - use custom secret key for our auth system
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET") or os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Either BETTER_AUTH_SECRET or JWT_SECRET_KEY environment variable must be set for JWT verification")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

security = HTTPBearer()


class TokenData:
    user_id: Optional[int] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    Verify the JWT token and return the user ID
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Better Auth may use different claim names, so check multiple possibilities
        user_id = payload.get("user_id") or payload.get("sub") or payload.get("id")

        if user_id is None:
            raise credentials_exception

        # Convert to int if it's a string
        if isinstance(user_id, str):
            try:
                user_id = int(user_id)
            except ValueError:
                raise credentials_exception

        token_data = TokenData()
        token_data.user_id = user_id
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get the current user from the JWT token
    """
    token = credentials.credentials
    user = verify_token(token)
    return user