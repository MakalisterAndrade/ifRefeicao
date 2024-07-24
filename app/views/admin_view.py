from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.controllers.user_controller import create_user, upload_users_from_csv
from app.schemas.user import UserCreate, User
from app.database import get_db

router = APIRouter()

@router.post("/users/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.post("/users/upload_csv/")
def upload_users(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido")
    file_location = f"app/temp/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    upload_users_from_csv(db, file_location)
    return {"detail": "Usuários enviados com sucesso"}
