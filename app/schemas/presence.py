# app/schemas/presence.py
from pydantic import BaseModel
from datetime import datetime

class PresenceBase(BaseModel):
    user_id: int
    timestamp: datetime

class PresenceCreate(PresenceBase):
    pass

class Presence(PresenceBase):
    id: int

    class Config:
        orm_mode = True
