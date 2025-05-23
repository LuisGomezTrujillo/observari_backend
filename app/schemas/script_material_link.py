from pydantic import BaseModel, ConfigDict

class ScriptMaterialLinkBase(BaseModel):
    script_id: int
    material_id: int

class ScriptMaterialLinkCreate(ScriptMaterialLinkBase):
    pass

class ScriptMaterialLinkRead(ScriptMaterialLinkBase):
    model_config = ConfigDict(from_attributes=True)

class ScriptMaterialLinkDelete(ScriptMaterialLinkBase):
    pass