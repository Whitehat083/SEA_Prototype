# backend/api/main_api.py

import sys
import os
import asyncio
from typing import List
from pydantic import BaseModel

# -- Project Root Setup --
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.core.swarm_manager import SwarmManager

class GoToCommand(BaseModel):
    coordinates: List[float]

app = FastAPI(title="SEA C2 Server")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

swarm = SwarmManager()

# --- Rotas HTTP (sem alterações) ---
@app.on_event("startup")
async def startup_event():
    print("SEA C2 Server Initialized. Awaiting connections...")

@app.post("/api/command/takeoff_all")
async def takeoff_all():
    swarm.command_takeoff_all()
    return {"message": "Takeoff command sent to all drones."}

@app.post("/api/command/land_all")
async def land_all():
    swarm.command_land_all()
    return {"message": "Land command sent to all drones."}

@app.post("/api/command/go_to_all")
async def go_to_all_command(command: GoToCommand):
    target_pos = [command.coordinates[0], command.coordinates[1], 50.0]
    swarm.command_go_to_all(target_pos)
    return {"message": f"Go-To command sent for all drones to target."}

# --- Rota WebSocket (COM DIAGNÓSTICO) ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Backend: Tentativa de conexão WebSocket recebida.")
    await websocket.accept()
    print("Backend: Conexão WebSocket ACEITA.")
    try:
        while True:
            telemetry_data = swarm.get_swarm_telemetry()
            # print("Backend: Enviando dados de telemetria...") # Descomente para log verboso
            await websocket.send_json(telemetry_data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Backend: Conexão WebSocket FECHADA pelo cliente.")
    except Exception as e:
        print(f"Backend: Ocorreu um erro na conexão WebSocket: {e}")