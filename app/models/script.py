from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .area import Area
    from .material import Material
    from .script_material_link import ScriptMaterialLink
    from .activity import Activity

class Script(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    area_id: int = Field(foreign_key="area.id")

    area: Optional["Area"] = Relationship(back_populates="scripts")
    script_links: List["ScriptMaterialLink"] = Relationship(back_populates="script")
    materials: List["Material"] = Relationship(
        back_populates="scripts",
        link_model=__import__("app.models.script_material_link").models.script_material_link.ScriptMaterialLink  # ✅ CARGA DIRECTA DE CLASE
    )
    activities: List["Activity"] = Relationship(back_populates="script")
