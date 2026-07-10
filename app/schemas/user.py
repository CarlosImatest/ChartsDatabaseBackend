'''
This is the stucture that the Frontend will use when creating a user
'''

from pydantic import BaseModel, EmailStr

from app.common.enums import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: UserRole