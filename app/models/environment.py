from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from .enums import EnvironmentType

if TYPE_CHECKING:
    from .area import Area
    from .activity import Activity

class Environment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    environment_type: EnvironmentType

    areas: List["Area"] = Relationship(back_populates="environment")
    activities: List["Activity"] = Relationship(back_populates="environment")
