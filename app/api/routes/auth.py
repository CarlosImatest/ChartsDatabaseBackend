from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.core.security import require_admin, get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    user = await AuthService.authenticate(payload.email, payload.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token = AuthService.issue_token(user)

    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role=user.role
        )
    )


@router.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate, current_user: User = Depends(require_admin)):
    db_user = await UserService.create_user(user)

    return UserResponse(
        id=str(db_user.id),
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        email=db_user.email,
        role=db_user.role
    )


@router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user.id),
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        role=current_user.role
    )