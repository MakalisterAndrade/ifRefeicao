# app/crud/reservation.py
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from app.models.reservation import Reservation as ReservationModel
from app.schemas.reservation import ReservationCreate as ReservationCreateSchema

def get_reservation(db: Session, reservation_id: int):
    return db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()

def create_reservation(db: Session, reservation: ReservationCreateSchema):
    db_reservation = ReservationModel(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_meal_count(db: Session, meal_type: str, date: datetime):
    return db.query(func.count(ReservationModel.id)).filter(ReservationModel.meal_type == meal_type, ReservationModel.date == date).scalar()

def get_present_users(db: Session):
    return db.query(ReservationModel).filter(ReservationModel.present == True).all()

def get_scheduled_users(db: Session):
    return db.query(ReservationModel).filter(ReservationModel.present == False, ReservationModel.canceled == False).all()

def get_canceled_users(db: Session):
    return db.query(ReservationModel).filter(ReservationModel.canceled == True).all()

def cancel_reservation(db: Session, user_id: int, reservation_id: int):
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id, ReservationModel.user_id == user_id).first()
    if reservation:
        reservation.canceled = True
        db.commit()
        db.refresh(reservation)
    return reservation

def get_user_reservations_for_date(db: Session, user_id: int, date: datetime):
    return db.query(ReservationModel).filter(
        and_(ReservationModel.user_id == user_id, ReservationModel.date == date)
    ).all()

def has_existing_reservation(db: Session, user_id: int, meal_type: str, date: datetime):
    return db.query(ReservationModel).filter(
        and_(ReservationModel.user_id == user_id, ReservationModel.meal_type == meal_type, ReservationModel.date == date)
    ).first() is not None
