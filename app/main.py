from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router_global import api_router
from .database import Base, engine

app = FastAPI(
    title="COEX Telemetry API",
    description="API REST para la recepción y consulta de telemetría GPS de los vehículos de COEX CA-03. Recibe posiciones desde dispositivos Raspberry Pi embarcados y expone endpoints para visualización en tiempo real e histórico.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix="/api/v1")
Base.metadata.create_all(bind=engine)
