# app/api/routes/users.py

from fastapi import APIRouter

from app.schemas.user import UserCreate
from app.schemas.user import UserResponse

from app.services.user_service import UserService

router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):

    db_user = await UserService.create_user(user)

    return UserResponse(
        id=str(db_user.id),
        name=db_user.name,
        email=db_user.email,
        role=db_user.role
    )