from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.script import Script
    from app.models.material import Material

class ScriptMaterialLink(SQLModel, table=True):
    script_id: int = Field(foreign_key="script.id", primary_key=True)
    material_id: int = Field(foreign_key="material.id", primary_key=True)

    script: Optional["Script"] = Relationship(back_populates="script_links")
    material: Optional["Material"] = Relationship(back_populates="script_links")
