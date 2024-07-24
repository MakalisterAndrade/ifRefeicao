# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String, unique=True, index=True)
    nome_completo = Column(String, index=True)
    is_interno = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
