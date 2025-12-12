"""
Aplicación principal FastAPI para Waze Ciudadano CDMX.

Incluye:
- Configuración de CORS
- Routers para reports, stats, certificates
- Endpoint de health check
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db
from backend.routers import reports, stats, certificates

# Crear aplicación FastAPI
app = FastAPI(
    title="Waze Ciudadano CDMX API",
    description="API para reportes ciudadanos de incidentes viales y análisis de datos C5",
    version="1.0.0"
)

# Configurar CORS para permitir requests del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(reports.router)
app.include_router(stats.router)
app.include_router(certificates.router)


@app.on_event("startup")
def startup_event():
    """Inicializa la base de datos al arrancar la aplicación."""
    init_db()


@app.get("/")
def root():
    """Endpoint raíz con información básica."""
    return {
        "message": "Waze Ciudadano CDMX API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Endpoint de health check."""
    return {"status": "ok"}

