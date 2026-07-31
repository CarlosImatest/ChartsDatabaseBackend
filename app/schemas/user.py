from pydantic import BaseModel, EmailStr

from app.common.enums import UserRole, UserStatus


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: UserRole


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole
    status: UserStatus