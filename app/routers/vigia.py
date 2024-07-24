# app/routers/vigia.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_user_by_matricula, mark_present
from app.routers.admin import manager

router = APIRouter()

@router.get("/vigia/validate/{qrcode}")
def validate_qrcode(qrcode: str, db: Session = Depends(get_db)):
    user = get_user_by_matricula(db, matricula=qrcode)
    if user:
        presence = mark_present(db, user.id)
        message = {
            "user_id": user.id,
            "nome_completo": user.nome_completo,
            "timestamp": presence.timestamp.isoformat()
        }
        manager.broadcast(message)
        return {"message": f"User {user.nome_completo} is present"}
    raise HTTPException(status_code=404, detail="User not found")
