from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.auth import LoginRequest, TokenResponse, RegisterWithInviteRequest, VerifyEmailRequest
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.core.security import require_admin, get_current_user
from app.common.enums import UserStatus
from app.models.user import User

router = APIRouter()


def _to_response(user: User) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role,
        status=user.status
    )


@router.post("/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    user = await AuthService.authenticate(payload.email, payload.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token = AuthService.issue_token(user)
    return TokenResponse(access_token=token, user=_to_response(user))


@router.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate, current_user: User = Depends(require_admin)):
    """Admin-direct user creation — bypasses invite/verification entirely."""
    db_user = await UserService.create_user(user)
    return _to_response(db_user)


@router.post("/auth/register-with-invite", response_model=TokenResponse)
async def register_with_invite(payload: RegisterWithInviteRequest):
    """
    Public endpoint (no auth required — the invite token itself is the
    credential proving this signup is legitimate). Returns a token
    immediately so the frontend can navigate to the waiting page, even
    though the account is still PENDING_VERIFICATION at this point.
    """
    try:
        user = await AuthService.register_with_invite(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    token = AuthService.issue_token(user)
    return TokenResponse(access_token=token, user=_to_response(user))


@router.post("/auth/verify-email", response_model=UserResponse)
async def verify_email(
    payload: VerifyEmailRequest,
    current_user: User = Depends(get_current_user)  # any status, just needs a valid token
):
    success = await AuthService.verify_email(current_user, payload.code)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    return _to_response(current_user)


@router.post("/auth/resend-code")
async def resend_code(current_user: User = Depends(get_current_user)):
    if current_user.status == UserStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Email already verified")

    await AuthService.resend_verification_code(current_user)
    return {"detail": "Verification code resent"}


@router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return _to_response(current_user)

from app.schemas.auth import ChangePasswordRequest

@router.post("/auth/change-password")
async def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user)  # any logged-in user, own account only
):
    success = await AuthService.change_password(
        current_user, payload.current_password, payload.new_password
    )

    if not success:
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    return {"detail": "Password updated"}