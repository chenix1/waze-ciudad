"""
Modelos Pydantic para validación y serialización de datos.

Define schemas para requests y responses de la API.
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class UserReportCreate(BaseModel):
    """Schema para crear un reporte ciudadano."""
    tipo: str = Field(..., description="Tipo de incidente (bache, choque, semaforo, etc.)")
    descripcion: Optional[str] = Field(None, description="Descripción del incidente")
    lat: float = Field(..., description="Latitud")
    lon: float = Field(..., description="Longitud")
    alcaldia: Optional[str] = Field(None, description="Alcaldía")
    colonia: Optional[str] = Field(None, description="Colonia")

    @field_validator('lat')
    @classmethod
    def validate_lat(cls, v):
        """Valida que la latitud esté en el rango de CDMX."""
        if not (19.0 <= v <= 20.0):
            raise ValueError('Latitud debe estar entre 19.0 y 20.0 (CDMX)')
        return v

    @field_validator('lon')
    @classmethod
    def validate_lon(cls, v):
        """Valida que la longitud esté en el rango de CDMX."""
        if not (-100.0 <= v <= -98.0):
            raise ValueError('Longitud debe estar entre -100.0 y -98.0 (CDMX)')
        return v


class UserReportRead(BaseModel):
    """Schema para leer un reporte ciudadano."""
    id: int
    created_at: datetime
    tipo: str
    descripcion: Optional[str]
    lat: float
    lon: float
    alcaldia: Optional[str]
    colonia: Optional[str]
    fuente: str

    class Config:
        from_attributes = True


class C5IncidentRead(BaseModel):
    """Schema para leer un incidente C5."""
    id: int
    fecha_hora: datetime
    anio: int
    mes: int
    hora: int
    dia_semana: str
    tipo_incidente: str
    alcaldia: str
    colonia: str
    latitud: float
    longitud: float
    descripcion: Optional[str]
    fuente: str

    class Config:
        from_attributes = True


class TopZonaStats(BaseModel):
    """Schema para estadísticas de top zonas."""
    zona: str
    tipo_zona: str  # "colonia" o "alcaldia"
    total_incidentes: int
    incidentes_c5: int
    incidentes_usuarios: int


class HoraStats(BaseModel):
    """Schema para estadísticas por hora."""
    hora: int
    total_incidentes: int
    incidentes_c5: int
    incidentes_usuarios: int

