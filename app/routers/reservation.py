# app/routers/reservation.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, time, timedelta
from app import crud, schemas, database

router = APIRouter()

def check_reservation_rules(user_id: int, meal_type: str, date: datetime, db: Session):
    # Verificar se já existe uma reserva para o mesmo tipo de refeição no mesmo dia
    if crud.has_existing_reservation(db, user_id, meal_type, date):
        raise HTTPException(status_code=400, detail=f"User already has a {meal_type} reservation for {date.date()}")

    # Verificar se o usuário pode agendar para a data especificada
    user = crud.get_user(db, user_id)
    current_time = datetime.now()

    if not user.is_interno:
        if date.date() == datetime.now().date():
            if current_time.time() >= time(6, 0):
                raise HTTPException(status_code=400, detail="Usuários não internos só podem fazer reservas para hoje até às 6h")
        elif date.date() == datetime.now().date() + timedelta(days=1):
            if current_time.time() >= time(6, 0):
                raise HTTPException(status_code=400, detail="Usuários não internos só podem fazer reservas para amanhã até às 6h de hoje")
        else:
            raise HTTPException(status_code=400, detail="Usuários não internos só podem fazer reservas para hoje ou amanhã")

@router.post("/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(database.get_db)):
    check_reservation_rules(reservation.user_id, reservation.meal_type, reservation.date, db)
    return crud.create_reservation(db=db, reservation=reservation)

@router.get("/{reservation_id}", response_model=schemas.Reservation)
def get_reservation(reservation_id: int, db: Session = Depends(database.get_db)):
    reservation = crud.get_reservation(db, reservation_id=reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.delete("/{user_id}/{reservation_id}", response_model=schemas.Reservation)
def cancel_reservation(user_id: int, reservation_id: int, db: Session = Depends(database.get_db)):
    reservation = crud.cancel_reservation(db, user_id=user_id, reservation_id=reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation
