"""
Script para descargar el CSV de incidentes viales del C5.

Descarga desde Datos Abiertos CDMX y guarda en data/raw/incidentesc5.csv
"""

import requests
import os
from pathlib import Path

# TODO: Verificar URL actual en datos.cdmx.gob.mx
# URL del recurso CSV de incidentes viales C5
C5_CSV_URL = "https://datos.cdmx.gob.mx/dataset/incidentes-viales-c5/resource/c3035e8d-f315-4c8c-bfbb-b7f818d5acb4/download/incidentesc5.csv"

# Ruta donde guardar el CSV
DATA_RAW_DIR = Path(__file__).parent.parent.parent / "data" / "raw"
OUTPUT_FILE = DATA_RAW_DIR / "incidentesc5.csv"


def download_c5_csv():
    """
    Descarga el CSV de incidentes viales del C5 desde Datos Abiertos CDMX.
    
    Returns:
        str: Ruta al archivo descargado
    """
    # Crear directorio si no existe
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Descargando CSV del C5 desde: {C5_CSV_URL}")
    print(f"Guardando en: {OUTPUT_FILE}")
    
    try:
        # Descargar archivo
        response = requests.get(C5_CSV_URL, stream=True, timeout=30)
        response.raise_for_status()
        
        # Guardar archivo
        with open(OUTPUT_FILE, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = OUTPUT_FILE.stat().st_size
        print(f"✓ Descarga completada. Tamaño: {file_size / 1024 / 1024:.2f} MB")
        
        return str(OUTPUT_FILE)
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error al descargar: {e}")
        raise
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        raise


if __name__ == "__main__":
    download_c5_csv()

