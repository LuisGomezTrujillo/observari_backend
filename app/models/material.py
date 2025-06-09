from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from ..enums import MaterialStatus

if TYPE_CHECKING:
    from .area import Area
    from .activity import Activity
    from .script import Script
    from .script_material_link import ScriptMaterialLink

class Material(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    reference: str
    description: Optional[str] = None
    photo_url: Optional[str] = None
    status: MaterialStatus
    area_id: int = Field(foreign_key="area.id")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    area: Optional["Area"] = Relationship(back_populates="materials")
    activities: List["Activity"] = Relationship(back_populates="material")
    script_links: List["ScriptMaterialLink"] = Relationship(back_populates="material")
    scripts: List["Script"] = Relationship(
        back_populates="materials",
        link_model=__import__("app.models.script_material_link").models.script_material_link.ScriptMaterialLink  # ✅ CARGA DIRECTA DE CLASE
    )
