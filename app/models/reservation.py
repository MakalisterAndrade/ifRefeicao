# app/models/reservation.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class MealTypeEnum(PyEnum):
    almoco = "almoço"
    jantar = "jantar"

class Reservation(Base):
    __tablename__ = "reservations"

    reseevation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    meal_type = Column(Enum(MealTypeEnum), index=True)
    date = Column(DateTime, index=True)
    present = Column(Boolean, default=False)
    canceled = Column(Boolean, default=False)
