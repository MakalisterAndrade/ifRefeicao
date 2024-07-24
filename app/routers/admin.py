# app/routers/admin.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.reservation import get_present_users, get_scheduled_users, get_canceled_users
import csv
from app.models.reservation import MealTypeEnum

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.send_counts(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

    async def send_counts(self, websocket: WebSocket):
        db = next(get_db())
        present_users = get_present_users(db)
        scheduled_users = get_scheduled_users(db)
        canceled_users = get_canceled_users(db)

        counts = {
            "present_almoco": len([pu for pu in present_users if pu.meal_type == MealTypeEnum.almoco]),
            "present_jantar": len([pu for pu in present_users if pu.meal_type == MealTypeEnum.jantar]),
            "scheduled_almoco": len([su for su in scheduled_users if su.meal_type == MealTypeEnum.almoco]),
            "scheduled_jantar": len([su for su in scheduled_users if su.meal_type == MealTypeEnum.jantar]),
            "canceled_almoco": len([cu for cu in canceled_users if cu.meal_type == MealTypeEnum.almoco]),
            "canceled_jantar": len([cu for cu in canceled_users if cu.meal_type == MealTypeEnum.jantar])
        }

        await websocket.send_json(counts)

manager = ConnectionManager()

@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    content = await file.read()
    decoded_content = content.decode("utf-8").splitlines()
    reader = csv.reader(decoded_content)
    for row in reader:
        matricula, nome_completo = row
        user = crud.get_user_by_matricula(db, matricula=matricula)
        if user:
            user.is_interno = True
            db.commit()
    return {"message": "CSV file processed successfully"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
            await manager.send_counts(websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.get("/admin", response_class=HTMLResponse)
async def get_admin_page():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Admin Panel</title>
        </head>
        <body>
            <h1>Admin Panel</h1>
            <h2>Almoço</h2>
            <p>Presentes: <span id='present-almoco'></span></p>
            <p>Agendados: <span id='scheduled-almoco'></span></p>
            <p>Cancelados: <span id='canceled-almoco'></span></p>
            <h2>Jantar</h2>
            <p>Presentes: <span id='present-jantar'></span></p>
            <p>Agendados: <span id='scheduled-jantar'></span></p>
            <p>Cancelados: <span id='canceled-jantar'></span></p>
            <script>
                const ws = new WebSocket("ws://localhost:8000/ws");
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    document.getElementById('present-almoco').textContent = data.present_almoco;
                    document.getElementById('scheduled-almoco').textContent = data.scheduled_almoco;
                    document.getElementById('canceled-almoco').textContent = data.canceled_almoco;
                    document.getElementById('present-jantar').textContent = data.present_jantar;
                    document.getElementById('scheduled-jantar').textContent = data.scheduled_jantar;
                    document.getElementById('canceled-jantar').textContent = data.canceled_jantar;
                };
            </script>
        </body>
    </html>
    """
