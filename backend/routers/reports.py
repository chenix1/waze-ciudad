"""
Router para endpoints de reportes ciudadanos.

Endpoints:
- POST /reports: crear nuevo reporte
- GET /reports: listar reportes con filtros opcionales
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from backend.database import get_db
from backend.models import UserReport
from backend.schemas import UserReportCreate, UserReportRead

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("", response_model=UserReportRead, status_code=201)
def create_report(
    report: UserReportCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo reporte ciudadano.
    
    Valida coordenadas (CDMX) y guarda en la base de datos.
    """
    db_report = UserReport(
        tipo=report.tipo,
        descripcion=report.descripcion,
        lat=report.lat,
        lon=report.lon,
        alcaldia=report.alcaldia,
        colonia=report.colonia
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


@router.get("", response_model=List[UserReportRead])
def get_reports(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de incidente"),
    alcaldia: Optional[str] = Query(None, description="Filtrar por alcaldía"),
    colonia: Optional[str] = Query(None, description="Filtrar por colonia"),
    limit: int = Query(200, ge=1, le=1000, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """
    Obtiene lista de reportes ciudadanos con filtros opcionales.
    
    Ordenados por fecha de creación descendente.
    """
    query = db.query(UserReport)
    
    if tipo:
        query = query.filter(UserReport.tipo == tipo)
    if alcaldia:
        query = query.filter(UserReport.alcaldia == alcaldia)
    if colonia:
        query = query.filter(UserReport.colonia == colonia)
    
    reports = query.order_by(UserReport.created_at.desc()).limit(limit).all()
    return reports

