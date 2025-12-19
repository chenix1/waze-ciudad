"""
Script ETL para procesar el CSV de incidentes viales del C5.

Lee el CSV crudo, limpia y transforma datos, y los inserta en la base de datos.
Usa pandas para el procesamiento.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
import sys

# Agregar el directorio raíz al path para importar módulos del backend
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.database import SessionLocal, init_db
from backend.models import C5Incident


def parse_fecha_hora(fecha_str: str) -> datetime:
    """
    Parsea una cadena de fecha/hora a datetime.
    
    Intenta varios formatos comunes.
    """
    if pd.isna(fecha_str) or fecha_str == "":
        return None
    
    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%dT%H:%M:%S",
    ]
    
    for fmt in formatos:
        try:
            return pd.to_datetime(fecha_str, format=fmt)
        except:
            continue
    
    # Si ninguno funciona, intentar parseo automático
    try:
        return pd.to_datetime(fecha_str)
    except:
        return None


def process_c5_csv(
    csv_path: str = None,
    save_processed: bool = True,
    insert_to_db: bool = True
):
    """
    Procesa el CSV de incidentes C5.
    
    Args:
        csv_path: Ruta al CSV crudo. Si es None, usa data/raw/incidentesc5.csv
        save_processed: Si True, guarda CSV procesado en data/processed/
        insert_to_db: Si True, inserta datos en la base de datos SQLite
    """
    # Ruta por defecto
    if csv_path is None:
        csv_path = Path(__file__).parent.parent.parent / "data" / "raw" / "incidentesc5.csv"
    
    csv_path = Path(csv_path)
    
    if not csv_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {csv_path}")
    
    print(f"Leyendo CSV: {csv_path}")
    
    # Leer CSV con pandas
    # TODO: Ajustar encoding, separador y nombres de columnas según el esquema real
    try:
        df = pd.read_csv(csv_path, encoding="utf-8", low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="latin-1", low_memory=False)
    
    print(f"Filas leídas: {len(df)}")
    print(f"Columnas: {list(df.columns)}")
    
    # TODO: Ajustar nombres de columnas según el esquema real del CSV
    # Asumiendo nombres comunes, pero deben verificarse:
    column_mapping = {
        # Mapeo esperado (ajustar según CSV real)
        "fecha_creacion": "fecha_hora",
        "incidente_c4": "tipo_incidente",
        "alcaldia_catalogo": "alcaldia",
        "colonia_catalogo": "colonia",
        "latitud": "latitud",
        "longitud": "longitud",
    }
    
    # Renombrar columnas si existen
    df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
    
    # Procesar fecha_hora
    if "fecha_hora" in df.columns:
        df["fecha_hora"] = df["fecha_hora"].apply(parse_fecha_hora)
    else:
        print("⚠ Advertencia: No se encontró columna de fecha/hora")
        df["fecha_hora"] = pd.NaT
    
    # Extraer componentes de fecha
    df["anio"] = pd.to_datetime(df["fecha_hora"]).dt.year
    df["mes"] = pd.to_datetime(df["fecha_hora"]).dt.month
    df["hora"] = pd.to_datetime(df["fecha_hora"]).dt.hour
    df["dia_semana"] = pd.to_datetime(df["fecha_hora"]).dt.day_name()
    
    # Limpiar y normalizar columnas de texto
    text_columns = ["tipo_incidente", "alcaldia", "colonia", "descripcion"]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace("nan", None)
            df[col] = df[col].replace("", None)
    
    # Convertir coordenadas a float
    if "latitud" in df.columns:
        df["latitud"] = pd.to_numeric(df["latitud"], errors="coerce")
    if "longitud" in df.columns:
        df["longitud"] = pd.to_numeric(df["longitud"], errors="coerce")
    
    # Filtrar filas con fecha_hora válida
    df = df[df["fecha_hora"].notna()]
    
    print(f"Filas después de limpieza: {len(df)}")
    
    # Guardar CSV procesado
    if save_processed:
        processed_dir = Path(__file__).parent.parent.parent / "data" / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)
        processed_file = processed_dir / "incidentesc5_procesado.csv"
        
        # Seleccionar solo columnas relevantes
        columns_to_save = [
            "fecha_hora", "anio", "mes", "hora", "dia_semana",
            "tipo_incidente", "alcaldia", "colonia",
            "latitud", "longitud", "descripcion"
        ]
        columns_to_save = [c for c in columns_to_save if c in df.columns]
        
        df[columns_to_save].to_csv(processed_file, index=False, encoding="utf-8")
        print(f"✓ CSV procesado guardado en: {processed_file}")
    
    # Insertar en base de datos
    if insert_to_db:
        init_db()
        db: Session = SessionLocal()
        
        try:
            # Limpiar tabla existente (opcional, comentar si se quiere acumular)
            # db.query(C5Incident).delete()
            # db.commit()
            
            # Insertar en lotes
            batch_size = 1000
            total_rows = len(df)
            
            for i in range(0, total_rows, batch_size):
                batch = df.iloc[i:i + batch_size]
                
                incidents = []
                for _, row in batch.iterrows():
                    incident = C5Incident(
                        fecha_hora=row.get("fecha_hora"),
                        anio=int(row.get("anio")) if pd.notna(row.get("anio")) else None,
                        mes=int(row.get("mes")) if pd.notna(row.get("mes")) else None,
                        hora=int(row.get("hora")) if pd.notna(row.get("hora")) else None,
                        dia_semana=str(row.get("dia_semana")) if pd.notna(row.get("dia_semana")) else None,
                        tipo_incidente=str(row.get("tipo_incidente")) if pd.notna(row.get("tipo_incidente")) else None,
                        alcaldia=str(row.get("alcaldia")) if pd.notna(row.get("alcaldia")) else None,
                        colonia=str(row.get("colonia")) if pd.notna(row.get("colonia")) else None,
                        latitud=float(row.get("latitud")) if pd.notna(row.get("latitud")) else None,
                        longitud=float(row.get("longitud")) if pd.notna(row.get("longitud")) else None,
                        descripcion=str(row.get("descripcion")) if pd.notna(row.get("descripcion")) else None,
                        fuente="c5"
                    )
                    incidents.append(incident)
                
                db.bulk_save_objects(incidents)
                db.commit()
                
                print(f"  Insertadas {min(i + batch_size, total_rows)} / {total_rows} filas")
            
            print(f"✓ Datos insertados en la base de datos")
        
        except Exception as e:
            db.rollback()
            print(f"✗ Error al insertar en BD: {e}")
            raise
        finally:
            db.close()
    
    return df


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Procesa CSV de incidentes C5")
    parser.add_argument("--csv", type=str, help="Ruta al CSV crudo")
    parser.add_argument("--no-save", action="store_true", help="No guardar CSV procesado")
    parser.add_argument("--no-db", action="store_true", help="No insertar en BD")
    
    args = parser.parse_args()
    
    process_c5_csv(
        csv_path=args.csv,
        save_processed=not args.no_save,
        insert_to_db=not args.no_db
    )

