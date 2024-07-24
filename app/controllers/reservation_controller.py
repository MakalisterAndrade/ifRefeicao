from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, date as dt_date, time as dt_time
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import ReservationCreate

def create_reservation(db: Session, reservation: ReservationCreate):
    user = db.query(User).filter(User.id == reservation.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    cutoff_time = dt_time(6, 0)  # 6 AM

    # Check if the reservation date is today and the current time is after the cutoff time
    if not user.is_resident and reservation.date == current_date and current_time > cutoff_time:
        raise HTTPException(status_code=400, detail="Reservations for today must be made before 6 AM")

    if not user.is_resident and reservation.date <= dt_date.today():
        raise HTTPException(status_code=400, detail="Reservations must be made at least one day in advance")

    if user.is_resident and reservation.date.weekday() == 4 and reservation.meal_type == "jantar":
        # Lógica para notificar o usuário sobre a reserva do jantar de sexta-feira
        pass

    db_reservation = Reservation(user_id=reservation.user_id, date=reservation.date, meal_type=reservation.meal_type)
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    # Notificar administrador
    notify_admin(f"New reservation: {reservation.user_id} for {reservation.meal_type} on {reservation.date}")
    return db_reservation

def cancel_reservation(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    db.delete(reservation)
    db.commit()
    # Notificar administrador
    notify_admin(f"Reservation {reservation_id} cancelada")
    return {"detail": "Reservation cancelada"}

def notify_admin(message: str):
    # Função para notificar o administrador
    print(f"Admin notified: {message}")
