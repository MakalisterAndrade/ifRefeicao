# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.models.reservation import Reservation as ReservationModel
from app.schemas.user import UserCreate as UserCreateSchema

def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_matricula(db: Session, matricula: str):
    return db.query(UserModel).filter(UserModel.matricula == matricula).first()

def create_user(db: Session, user: UserCreateSchema):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()

def get_present_users(db: Session):
    return db.query(ReservationModel).filter(ReservationModel.present == True).all()

def get_scheduled_users(db: Session):
    return db.query(ReservationModel).filter(ReservationModel.present == False, ReservationModel.canceled == False).all()

def get_canceled_users(db: Session):
    return db.query(ReservationModel).filter(ReservationModel.canceled == True).all()
