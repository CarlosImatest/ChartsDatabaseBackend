from pydantic import BaseModel, EmailStr

from app.common.enums import UserRole


class InviteCreate(BaseModel):
    email: EmailStr
    role: UserRole


class InviteResponse(BaseModel):
    token: str
    email: EmailStr
    role: UserRole
    invite_url: str
    expires_at: str