from pydantic import BaseModel, EmailStr

from app.schemas.user import UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class RegisterWithInviteRequest(BaseModel):
    """
    Note: no `email` or `role` fields here — both come from the invite
    itself (looked up server-side via invite_token), so the frontend
    form never lets the new user choose or spoof their own role.
    """
    invite_token: str
    first_name: str
    last_name: str
    password: str


class VerifyEmailRequest(BaseModel):
    code: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str