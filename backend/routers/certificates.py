"""
Router para endpoints de certificados PDF.

Endpoints:
- GET /certificates/zona: genera certificado PDF de riesgo vial por zona
"""

from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.certificates_service import CertificatesService
from backend.services.stats_service import StatsService
import tempfile
import os

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("/zona")
def get_certificate_zona(
    tipo_zona: str = Query(..., description="Tipo de zona: 'colonia' o 'alcaldia'"),
    nombre_zona: str = Query(..., description="Nombre de la zona"),
    db: Session = Depends(get_db)
):
    """
    Genera un certificado PDF de riesgo vial para una zona específica.
    
    Combina estadísticas de C5 y reportes ciudadanos.
    """
    if tipo_zona not in ["colonia", "alcaldia"]:
        return {"error": "tipo_zona debe ser 'colonia' o 'alcaldia'"}
    
    stats_service = StatsService(db)
    certificates_service = CertificatesService()
    
    # Obtener estadísticas de la zona
    stats = stats_service.get_zona_stats(tipo_zona=tipo_zona, nombre_zona=nombre_zona)
    
    # Generar PDF
    pdf_path = certificates_service.generate_certificate(
        tipo_zona=tipo_zona,
        nombre_zona=nombre_zona,
        stats=stats
    )
    
    # Retornar PDF como respuesta
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"certificado_riesgo_vial_{nombre_zona.replace(' ', '_')}.pdf"
    )

