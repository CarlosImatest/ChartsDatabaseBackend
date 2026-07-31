import secrets
from datetime import datetime, timedelta, timezone

from app.models.invite import Invite
from app.models.user import User
from app.schemas.invite import InviteCreate
from app.core.config import settings
from app.services.email_service import EmailService


class InviteService:

    @staticmethod
    async def create_invite(payload: InviteCreate, created_by: str) -> Invite:
        # Prevent inviting someone who's already an account holder
        existing_user = await User.find_one(User.email == payload.email)
        if existing_user:
            raise ValueError("A user with this email already exists")

        token = secrets.token_urlsafe(32)  # unguessable, URL-safe
        expires_at = datetime.now(timezone.utc) + timedelta(
            hours=settings.invite_expire_hours
        )

        invite = Invite(
            token=token,
            email=payload.email,
            role=payload.role,
            created_by=created_by,
            expires_at=expires_at
        )
        await invite.insert()

        invite_url = f"{settings.frontend_url}/register?invite={token}"
        EmailService.send_invite(payload.email, invite_url, payload.role.value)

        return invite

    @staticmethod
    async def get_valid_invite(token: str) -> Invite:
        """
        Looks up an invite by token and validates it's actually usable.
        Raises ValueError with a specific reason on failure — the route
        layer turns this into a 400 with that message.
        """
        invite = await Invite.find_one(Invite.token == token)

        if not invite:
            raise ValueError("Invite not found")
        if invite.used:
            raise ValueError("Invite has already been used")
        if invite.expires_at < datetime.now(timezone.utc):
            raise ValueError("Invite has expired")

        return invite

    @staticmethod
    async def mark_used(invite: Invite) -> None:
        invite.used = True
        await invite.save()