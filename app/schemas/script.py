from pydantic import BaseModel
from typing import Optional

class ScriptBase(BaseModel):
    title: str
    area_id: int

class ScriptCreate(ScriptBase):
    pass

class ScriptRead(ScriptBase):
    id: int