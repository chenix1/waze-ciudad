"""
Módulo de configuración de base de datos SQLAlchemy.

Conecta con SQLite para desarrollo. Deja preparado para migrar a Postgres si se desea.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Ruta a la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/waze_cdmx.db"

# Crear directorio data si no existe
os.makedirs("data", exist_ok=True)

# Engine de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necesario para SQLite
)

# SessionLocal para crear sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos declarativos
Base = declarative_base()


def get_db():
    """
    Dependency para obtener sesión de base de datos en FastAPI.
    
    Yields:
        Session: Sesión de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa las tablas en la base de datos.
    """
    Base.metadata.create_all(bind=engine)

