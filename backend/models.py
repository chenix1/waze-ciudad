"""
Modelos SQLAlchemy para las tablas de la base de datos.

Define:
- C5Incident: incidentes oficiales del C5
- UserReport: reportes ciudadanos
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from backend.database import Base


class C5Incident(Base):
    """
    Modelo para incidentes viales oficiales del C5 (Datos Abiertos CDMX).
    """
    __tablename__ = "c5_incidents"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, nullable=False, index=True)
    anio = Column(Integer, index=True)
    mes = Column(Integer)
    hora = Column(Integer, index=True)
    dia_semana = Column(String(20))
    tipo_incidente = Column(String(200), index=True)
    alcaldia = Column(String(200), index=True)
    colonia = Column(String(200), index=True)
    latitud = Column(Float)
    longitud = Column(Float)
    descripcion = Column(Text, nullable=True)
    fuente = Column(String(50), default="c5")


class UserReport(Base):
    """
    Modelo para reportes ciudadanos de incidentes viales.
    """
    __tablename__ = "user_reports"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    tipo = Column(String(100), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    alcaldia = Column(String(200), nullable=True, index=True)
    colonia = Column(String(200), nullable=True, index=True)
    fuente = Column(String(50), default="usuario")

