"""schemas/location.py"""
from pydantic import BaseModel, ConfigDict


class LocationBase(BaseModel):
    code: str
    name: str
    description: str | None = None


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    description: str | None = None


class LocationRead(LocationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
