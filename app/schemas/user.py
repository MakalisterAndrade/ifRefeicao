# app/schemas/user.py
from pydantic import BaseModel

class UserBase(BaseModel):
    matricula: str
    nome_completo: str

class UserCreate(UserBase):
    is_interno: bool = False
    is_admin: bool = False

class User(UserBase):
    id: int
    is_interno: bool
    is_admin: bool

    class Config:
        orm_mode = True
