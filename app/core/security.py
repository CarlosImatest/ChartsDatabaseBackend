from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from app.core.config import settings
from app.models.user import User
from app.common.enums import UserRole

# HTTPBearer just means "expect an Authorization: Bearer <token> header."
# Unlike OAuth2PasswordBearer, it doesn't assume there's a login form
# behind it — which is correct here, since our /auth/login endpoint
# takes JSON, not OAuth2's form-encoded username/password.
bearer_scheme = HTTPBearer()

ROLE_RANK = {
    UserRole.VIEWER: 0,
    UserRole.EDITOR: 1,
    UserRole.ADMIN: 2,
}


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials  # the raw token, "Bearer " already stripped

    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await User.get(user_id)
    if user is None:
        raise credentials_exception

    return user


def require_role(minimum: UserRole):
    async def checker(current_user: User = Depends(get_current_user)) -> User:
        if ROLE_RANK[current_user.role] < ROLE_RANK[minimum]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires at least {minimum.value} role"
            )
        return current_user

    return checker


require_viewer = require_role(UserRole.VIEWER)
require_editor = require_role(UserRole.EDITOR)
require_admin = require_role(UserRole.ADMIN)