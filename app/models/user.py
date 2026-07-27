from beanie import Document
from pydantic import EmailStr

from app.common.enums import UserRole


class User(Document):

    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    role: UserRole

    class Settings:
        name = "user"