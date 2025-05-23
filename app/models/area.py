from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from .enums import AreaType

if TYPE_CHECKING:
    from .environment import Environment
    from .material import Material
    from .script import Script
    from .activity import Activity

class Area(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    area_type: AreaType
    environment_id: int = Field(foreign_key="environment.id")

    environment: Optional["Environment"] = Relationship(back_populates="areas")
    materials: List["Material"] = Relationship(back_populates="area")
    scripts: List["Script"] = Relationship(back_populates="area")
    activities: List["Activity"] = Relationship(back_populates="area")
