#!/bin/bash
# Script para descargar el CSV de incidentes viales del C5
# Desde Datos Abiertos CDMX

# TODO: Verificar URL actual en datos.cdmx.gob.mx
URL="https://datos.cdmx.gob.mx/dataset/incidentes-viales-c5/resource/c3035e8d-f315-4c8c-bfbb-b7f818d5acb4/download/incidentesc5.csv"

# Directorio de destino
DATA_DIR="$(dirname "$0")/../data/raw"
OUTPUT_FILE="$DATA_DIR/incidentesc5.csv"

# Crear directorio si no existe
mkdir -p "$DATA_DIR"

echo "Descargando CSV del C5..."
echo "URL: $URL"
echo "Destino: $OUTPUT_FILE"

# Descargar usando curl
if command -v curl &> /dev/null; then
    curl -L -o "$OUTPUT_FILE" "$URL"
elif command -v wget &> /dev/null; then
    wget -O "$OUTPUT_FILE" "$URL"
else
    echo "Error: Se requiere curl o wget para descargar el archivo"
    exit 1
fi

# Verificar que el archivo se descargó correctamente
if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo "✓ Descarga completada. Tamaño: $SIZE"
else
    echo "✗ Error: No se pudo descargar el archivo"
    exit 1
fi

