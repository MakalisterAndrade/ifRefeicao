# app/schemas/reservation.py
from pydantic import BaseModel
from datetime import date
from app.models.reservation import MealTypeEnum

class ReservationBase(BaseModel):
    user_id: int
    meal_type: MealTypeEnum
    date: date

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    present: bool
    canceled: bool

    class Config:
        orm_mode = True
