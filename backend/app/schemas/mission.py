"""schemas/mission.py"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import MissionStatus


class MissionBase(BaseModel):
    code: str
    title: str
    requester: str | None = None
    destination: str | None = None
    note: str | None = None


class MissionCreate(MissionBase):
    pass


class MissionUpdate(BaseModel):
    title: str | None = None
    requester: str | None = None
    destination: str | None = None
    status: MissionStatus | None = None
    note: str | None = None


class MissionRead(MissionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: MissionStatus
    created_at: datetime
