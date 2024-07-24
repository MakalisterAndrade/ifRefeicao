from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate
import csv

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, matricula=user.matricula, is_resident=user.is_resident, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def upload_users_from_csv(db: Session, file_path: str):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user = UserCreate(
                name=row['name'],
                matricula=row['matricula'],
                is_resident=row.get('is_resident', 'False').lower() in ['true', '1']
            )
            create_user(db, user)
