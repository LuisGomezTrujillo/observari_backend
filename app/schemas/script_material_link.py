from pydantic import BaseModel, ConfigDict
from typing import Optional


class ScriptMaterialLinkBase(BaseModel):
    script_id: int
    material_id: int
    quantity: Optional[int] = 1
    required: bool = True


class ScriptMaterialLinkCreate(ScriptMaterialLinkBase):
    pass


class ScriptMaterialLinkUpdate(BaseModel):
    quantity: Optional[int] = None
    required: Optional[bool] = None


class ScriptMaterialLinkRead(ScriptMaterialLinkBase):
    model_config = ConfigDict(from_attributes=True)