"""
Ejemplo de cómputo distribuido usando multiprocessing.

Demuestra cómo procesar múltiples archivos o chunks grandes de datos
en paralelo usando multiprocessing.Pool o ProcessPoolExecutor.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict, Any
import time


def process_chunk(chunk_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Procesa un chunk de datos (simula procesamiento pesado).
    
    Esta función se ejecuta en un proceso separado.
    
    Args:
        chunk_data: Diccionario con 'chunk_id' y 'data' (DataFrame o datos)
        
    Returns:
        Diccionario con resultados del procesamiento
    """
    chunk_id = chunk_data["chunk_id"]
    data = chunk_data["data"]
    
    # Simular procesamiento pesado
    # En un caso real, aquí harías:
    # - Limpieza de datos
    # - Cálculos estadísticos
    # - Agregaciones
    # - etc.
    
    time.sleep(0.1)  # Simular trabajo
    
    # Ejemplo: calcular estadísticas del chunk
    if isinstance(data, pd.DataFrame):
        result = {
            "chunk_id": chunk_id,
            "rows": len(data),
            "mean": data.select_dtypes(include=[np.number]).mean().to_dict() if len(data) > 0 else {},
            "sum": data.select_dtypes(include=[np.number]).sum().to_dict() if len(data) > 0 else {},
        }
    else:
        result = {
            "chunk_id": chunk_id,
            "processed": True,
        }
    
    return result


def process_dataframe_parallel(
    df: pd.DataFrame,
    num_processes: int = None,
    chunk_size: int = 10000
) -> List[Dict[str, Any]]:
    """
    Procesa un DataFrame grande dividiéndolo en chunks y procesándolos en paralelo.
    
    Args:
        df: DataFrame a procesar
        num_processes: Número de procesos a usar (por defecto: número de CPUs)
        chunk_size: Tamaño de cada chunk
        
    Returns:
        Lista de resultados de cada chunk
    """
    if num_processes is None:
        num_processes = cpu_count()
    
    # Dividir DataFrame en chunks
    chunks = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size]
        chunks.append({
            "chunk_id": i // chunk_size,
            "data": chunk
        })
    
    print(f"Procesando {len(chunks)} chunks con {num_processes} procesos...")
    
    # Procesar en paralelo usando ProcessPoolExecutor
    results = []
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Enviar tareas
        futures = {executor.submit(process_chunk, chunk): chunk for chunk in chunks}
        
        # Recoger resultados conforme se completan
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                print(f"  Chunk {result['chunk_id']} completado")
            except Exception as e:
                print(f"  Error en chunk: {e}")
    
    return results


def process_multiple_files_parallel(
    file_paths: List[str],
    num_processes: int = None
) -> List[Dict[str, Any]]:
    """
    Procesa múltiples archivos CSV en paralelo.
    
    Útil cuando tienes datos históricos separados por año o mes.
    
    Args:
        file_paths: Lista de rutas a archivos CSV
        num_processes: Número de procesos a usar
        
    Returns:
        Lista de resultados de cada archivo
    """
    if num_processes is None:
        num_processes = min(cpu_count(), len(file_paths))
    
    def process_file(file_path: str) -> Dict[str, Any]:
        """Procesa un archivo CSV."""
        try:
            df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)
            return {
                "file": file_path,
                "rows": len(df),
                "columns": list(df.columns),
                "status": "success"
            }
        except Exception as e:
            return {
                "file": file_path,
                "status": "error",
                "error": str(e)
            }
    
    print(f"Procesando {len(file_paths)} archivos con {num_processes} procesos...")
    
    # Procesar en paralelo
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = {executor.submit(process_file, fp): fp for fp in file_paths}
        results = []
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"  {result['file']}: {result['status']}")
    
    return results


def example_usage():
    """
    Ejemplo de uso del cómputo distribuido.
    """
    print("=== Ejemplo de Cómputo Distribuido ===\n")
    
    # Ejemplo 1: Procesar DataFrame grande en chunks
    print("1. Procesando DataFrame grande en chunks paralelos:")
    df_large = pd.DataFrame({
        "x": np.random.randn(50000),
        "y": np.random.randn(50000),
        "z": np.random.randn(50000)
    })
    
    start = time.time()
    results = process_dataframe_parallel(df_large, chunk_size=10000)
    elapsed = time.time() - start
    
    print(f"   Tiempo total: {elapsed:.2f} segundos")
    print(f"   Chunks procesados: {len(results)}\n")
    
    # Ejemplo 2: Procesar múltiples archivos
    print("2. Procesando múltiples archivos en paralelo:")
    # Simular archivos (en producción, usar rutas reales)
    file_paths = [
        "data/raw/incidentesc5_2020.csv",
        "data/raw/incidentesc5_2021.csv",
        "data/raw/incidentesc5_2022.csv",
    ]
    
    # Filtrar solo los que existen
    existing_files = [fp for fp in file_paths if Path(fp).exists()]
    
    if existing_files:
        start = time.time()
        results = process_multiple_files_parallel(existing_files)
        elapsed = time.time() - start
        print(f"   Tiempo total: {elapsed:.2f} segundos")
    else:
        print("   (No se encontraron archivos de ejemplo)")


if __name__ == "__main__":
    example_usage()

