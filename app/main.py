# app/main.py
from fastapi import FastAPI
from app.routers import user, reservation, admin, vigia
from app.database import engine, Base
from app.models.user import User

app = FastAPI()

# Recrie todas as tabelas (Cuidado: Isso apaga os dados existentes)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(reservation.router, prefix="/reservations", tags=["reservations"])
app.include_router(admin.router, tags=["admin"])
app.include_router(vigia.router, tags=["vigia"])
