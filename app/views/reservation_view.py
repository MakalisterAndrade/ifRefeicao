from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from datetime import date as dt_date
import asyncio
from app.controllers.reservation_controller import create_reservation, cancel_reservation
from app.schemas.reservation import ReservationCreate, Reservation
from app.database import get_db

router = APIRouter()

@router.post("/reservations/", response_model=Reservation)
def create_new_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    return create_reservation(db, reservation)

@router.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    return cancel_reservation(db, reservation_id)

@router.websocket("/ws/admin")
async def admin_websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data == "get_counts":
                lunch_count = db.query(Reservation).filter(Reservation.meal_type == "almoço", Reservation.date == dt_date.today()).count()
                dinner_count = db.query(Reservation).filter(Reservation.meal_type == "jantar", Reservation.date == dt_date.today()).count()
                await websocket.send_text(f"Almoço: {lunch_count}, Jantar: {dinner_count}")
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        print("Client disconnected")
