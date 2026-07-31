from datetime import datetime

from beanie import Document
from pydantic import EmailStr

from app.common.enums import UserRole


class Invite(Document):
    """
    Represents a single admin-generated invite link. The invite carries
    the role that will be assigned to whoever redeems it — the new user
    never chooses their own role, it's fixed at creation time.

    `used` prevents replay: once someone registers with this token,
    it can never be used again, even if the link is shared further.
    """
    token: str          # random, unguessable — this is what's in the URL
    email: EmailStr      # who this invite was sent to; only they can use it
    role: UserRole
    created_by: str      # id of the admin who generated it
    expires_at: datetime
    used: bool = False

    class Settings:
        name = "invite"