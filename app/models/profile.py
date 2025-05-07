from datetime import date, datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.user import User    

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    first_name: str = Field(nullable=False)
    middle_name: Optional[str] = None
    last_name: str = Field(nullable=False)
    second_last_name: Optional[str] = None
    photo_url: Optional[str] = None
    birth_date: date
    mobile_phone: Optional[str] = None
    home_address: Optional[str] = None
    role: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: "User" = Relationship(back_populates="profile")