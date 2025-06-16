from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .script import Script
    from .material import Material

class ScriptMaterialLink(SQLModel, table=True):
    script_id: Optional[int] = Field(
        default=None, 
        foreign_key="script.id", 
        primary_key=True
    )
    material_id: Optional[int] = Field(
        default=None, 
        foreign_key="material.id", 
        primary_key=True
    )
    quantity: Optional[int] = Field(default=1)
    required: bool = Field(default=True)

    # Relationships
    script: Optional["Script"] = Relationship(back_populates="script_material_links")
    material: Optional["Material"] = Relationship(back_populates="script_material_links")