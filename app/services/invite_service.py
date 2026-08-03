import secrets
from datetime import datetime, timedelta, timezone

from app.models.invite import Invite
from app.models.user import User
from app.schemas.invite import InviteCreate
from app.core.config import settings
from app.services.email_service import EmailService
import resend



class InviteService:

    @staticmethod
    async def create_invite(payload: InviteCreate, created_by: str) -> Invite:
        existing_user = await User.find_one(User.email == payload.email)
        if existing_user:
            raise ValueError("A user with this email already exists")

        token = secrets.token_urlsafe(32)
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

        try:
            EmailService.send_invite(payload.email, invite_url, payload.role.value)
        except resend.exceptions.ResendError as e:
            # The invite record still exists and is valid — the admin
            # can manually share invite_url even if the email bounced.
            # We surface this as a clear 502 rather than a raw 500.
            raise ValueError(f"Invite created, but email failed to send: {e}")

        return invite

    @staticmethod
    async def get_valid_invite(token: str) -> Invite:
        invite = await Invite.find_one(Invite.token == token)

        if not invite:
            raise ValueError("Invite not found")
        if invite.used:
            raise ValueError("Invite has already been used")

        # invite.expires_at comes back from MongoDB as naive (no tzinfo),
        # even though we stored it as UTC-aware. datetime.now(timezone.utc)
        # is aware, so comparing them directly raises TypeError. We strip
        # tzinfo from "now" to compare apples to apples — both sides
        # represent UTC, just one has the label attached and one doesn't.
        now_naive_utc = datetime.now(timezone.utc).replace(tzinfo=None)

        if invite.expires_at < now_naive_utc:
            raise ValueError("Invite has expired")

        return invite

    @staticmethod
    async def mark_used(invite: Invite) -> None:
        invite.used = True
        await invite.save()