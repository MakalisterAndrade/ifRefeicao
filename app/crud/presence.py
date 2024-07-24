# app/crud/presence.py
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.presence import Presence as PresenceModel
from app.schemas.presence import PresenceCreate as PresenceCreateSchema

def get_present_users(db: Session):
    return db.query(PresenceModel).all()

def mark_present(db: Session, user_id: int):
    presence = PresenceModel(user_id=user_id, timestamp=datetime.utcnow())
    db.add(presence)
    db.commit()
    db.refresh(presence)
    return presence
