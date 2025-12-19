"""
Router para endpoints de estadísticas con filtros.
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from backend.database import get_db
from backend.schemas import TopZonaStats, HoraStats
from backend.services.stats_service import StatsService

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/opciones")
def get_opciones_filtros(db: Session = Depends(get_db)):
    """
    Obtiene las opciones disponibles para los filtros.
    Retorna listas de tipos de incidentes, alcaldías y colonias.
    """
    stats_service = StatsService(db)
    return stats_service.get_opciones_filtros()


@router.get("/filtradas")
def get_estadisticas_filtradas(
    tipo_incidente: Optional[str] = Query(None, description="Tipo de incidente"),
    alcaldia: Optional[str] = Query(None, description="Alcaldía"),
    colonia: Optional[str] = Query(None, description="Colonia"),
    limit: int = Query(50, ge=1, le=200, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """
    Obtiene estadísticas filtradas.
    Al menos uno de los filtros debe estar presente.
    """
    # Validar que al menos un filtro esté presente
    if not any([tipo_incidente, alcaldia, colonia]):
        raise HTTPException(
            status_code=400,
            detail="Debes proporcionar al menos un filtro: tipo_incidente, alcaldia o colonia"
        )
    
    stats_service = StatsService(db)
    return stats_service.get_estadisticas_filtradas(
        tipo_incidente=tipo_incidente,
        alcaldia=alcaldia,
        colonia=colonia,
        limit=limit
    )


@router.get("/top-zonas", response_model=List[TopZonaStats])
def get_top_zonas(
    tipo_zona: str = Query("colonia", description="Tipo de zona: 'colonia' o 'alcaldia'"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Endpoint antiguo - mantener por compatibilidad."""
    if tipo_zona not in ["colonia", "alcaldia"]:
        raise HTTPException(status_code=400, detail="tipo_zona debe ser 'colonia' o 'alcaldia'")
    
    stats_service = StatsService(db)
    return stats_service.get_top_zonas(tipo_zona=tipo_zona, limit=limit)


@router.get("/horas-peligrosas", response_model=List[HoraStats])
def get_horas_peligrosas(db: Session = Depends(get_db)):
    """Obtiene la distribución de incidentes por hora del día."""
    stats_service = StatsService(db)
    return stats_service.get_horas_peligrosas()
