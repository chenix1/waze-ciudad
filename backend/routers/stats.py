"""
Router para endpoints de estadísticas.

Endpoints:
- GET /stats/top-zonas: top colonias/alcaldías con más incidentes
- GET /stats/horas-peligrosas: distribución de incidentes por hora
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.schemas import TopZonaStats, HoraStats
from backend.services.stats_service import StatsService

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/top-zonas", response_model=List[TopZonaStats])
def get_top_zonas(
    tipo_zona: str = Query("colonia", description="Tipo de zona: 'colonia' o 'alcaldia'"),
    limit: int = Query(10, ge=1, le=50, description="Número de zonas a retornar"),
    db: Session = Depends(get_db)
):
    """
    Obtiene las top N zonas (colonias o alcaldías) con más incidentes.
    
    Combina datos de C5 y reportes ciudadanos.
    """
    if tipo_zona not in ["colonia", "alcaldia"]:
        return {"error": "tipo_zona debe ser 'colonia' o 'alcaldia'"}
    
    stats_service = StatsService(db)
    return stats_service.get_top_zonas(tipo_zona=tipo_zona, limit=limit)


@router.get("/horas-peligrosas", response_model=List[HoraStats])
def get_horas_peligrosas(
    db: Session = Depends(get_db)
):
    """
    Obtiene la distribución de incidentes por hora del día.
    
    Combina datos de C5 y reportes ciudadanos.
    """
    stats_service = StatsService(db)
    return stats_service.get_horas_peligrosas()

