from datetime import date, datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .area import Area
    from .material import Material
    from .activity import Activity

# Import the link model directly (not in TYPE_CHECKING block)
from .script_material_link import ScriptMaterialLink

class Script(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    area_id: int = Field(foreign_key="area.id")
    age_range: str
    objective: str
    steps: str
    duration_minutes: int
    created_by: str
    uploaded_by: str
    illustrations_url: Optional[str] = None
    video_url: Optional[str] = None
    pdf_url: Optional[str] = None
    reviewed_by: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[str] = Field(default=None, description="Comma-separated tags")
    is_active: bool = Field(default=True)
    created_at: date = Field(default_factory=lambda: date.today())
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    area: Optional["Area"] = Relationship(back_populates="scripts")
    script_material_links: List["ScriptMaterialLink"] = Relationship(back_populates="script")
    materials: List["Material"] = Relationship(
        back_populates="scripts",
        link_model=ScriptMaterialLink  # Use the class directly, not a string
    )
    activities: List["Activity"] = Relationship(back_populates="script")