# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database
from fastapi.responses import StreamingResponse
from app.utils import generate_qr_code

router = APIRouter()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_matricula(db, matricula=user.matricula)
    if db_user:
        raise HTTPException(status_code=400, detail="Matricula already registered")
    return crud.create_user(db=db, user=user)

@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db=db, user_id=user_id)
    return user

@router.get("/{user_id}/qrcode", response_class=StreamingResponse)
def get_user_qr_code(user_id: int, db: Session = Depends(database.get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user:
        qr_code = generate_qr_code(user.matricula)
        return StreamingResponse(qr_code, media_type="image/png")
    raise HTTPException(status_code=404, detail="User not found")
