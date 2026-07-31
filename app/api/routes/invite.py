from fastapi import APIRouter, Depends, HTTPException

from app.schemas.invite import InviteCreate, InviteResponse
from app.services.invite_service import InviteService
from app.core.security import require_admin
from app.core.config import settings
from app.models.user import User

router = APIRouter()


@router.post("/invites", response_model=InviteResponse)
async def create_invite(
    payload: InviteCreate,
    current_user: User = Depends(require_admin)  # only admins can invite
):
    try:
        invite = await InviteService.create_invite(
            payload, created_by=str(current_user.id)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return InviteResponse(
        token=invite.token,
        email=invite.email,
        role=invite.role,
        invite_url=f"{settings.frontend_url}/register?invite={invite.token}",
        expires_at=invite.expires_at.isoformat()
    )