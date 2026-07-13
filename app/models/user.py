'''
This is used for structure for creating a user
'''
from beanie import Document
from pydantic import EmailStr

from app.common.enums import UserRole


class User(Document):

    name: str

    email: EmailStr

    hashed_password: str

    role: UserRole


    class Settings:
        #this specifies which collection to insert the user into ChartsDB-->Users-->user
        name = "user"