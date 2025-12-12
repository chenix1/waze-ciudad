# Waze Ciudadano CDMX 🚗

**Proyecto Final - Curso "Fuentes de Datos"**

Sistema completo de reportes ciudadanos de incidentes viales para la Ciudad de México, integrando datos oficiales del C5 (Centro de Comando, Control, Cómputo, Comunicaciones y Contacto Ciudadano) con reportes en tiempo real de usuarios.

## 📋 Descripción General

Este proyecto es una **mini-aplicación tipo Waze ciudadano** que permite:

1. **Visualizar un mapa interactivo** de CDMX con incidentes viales
2. **Registrar reportes ciudadanos** de incidentes (baches, choques, semáforos descompuestos, inundaciones, manifestaciones, etc.)
3. **Combinar datos ciudadanos con datos históricos oficiales** del C5 (Datos Abiertos CDMX)
4. **Analizar estadísticas** por zona (colonias, alcaldías, horas del día)
5. **Generar certificados PDF** de riesgo vial por colonia o alcaldía
6. **Procesar grandes volúmenes de datos** usando cómputo distribuido

## 🏗️ Arquitectura del Proyecto

```
waze-ciudadano-cdmx/
├── backend/              # API FastAPI
│   ├── main.py          # Aplicación principal
│   ├── database.py      # Configuración SQLAlchemy
│   ├── models.py        # Modelos de base de datos
│   ├── schemas.py       # Schemas Pydantic
│   ├── routers/         # Endpoints de la API
│   ├── services/        # Lógica de negocio (stats, certificates)
│   ├── etl/            # Procesamiento de datos (download, process, distributed)
│   └── templates/       # Plantillas HTML para certificados
├── frontend/            # Interfaz web
│   ├── index.html      # Página principal
│   ├── app.js          # Lógica JavaScript (Leaflet, API calls)
│   └── styles.css      # Estilos
├── data/
│   ├── raw/            # CSV originales del C5
│   └── processed/      # Datos procesados
├── notebooks/          # Notebooks de exploración (pandas/numpy)
├── scripts/           # Scripts bash (descarga de datos)
├── docker/            # Dockerfiles y docker-compose
└── README.md          # Este archivo
```

## 🔗 Conexión con Temas del Curso

Este proyecto integra explícitamente todos los temas del curso "Fuentes de Datos":

### 1. **a_github** - Control de Versiones y GitHub
- ✅ Repositorio Git estructurado con commits descriptivos
- ✅ Uso de ramas para desarrollo (feature branches)
- ✅ README y documentación en el repo
- ✅ `.gitignore` apropiado para Python y datos

**Archivos relevantes:**
- `.gitignore` (crear si no existe)
- Estructura de commits: `git commit -m "feat: agregar endpoint de estadísticas"`

### 2. **python_env** - Entornos Virtuales Python
- ✅ Uso de `venv` o `virtualenv` para aislar dependencias
- ✅ `requirements.txt` con todas las dependencias del proyecto
- ✅ Instrucciones claras para crear y activar el entorno

**Archivos relevantes:**
- `backend/requirements.txt`
- Comandos: `python -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`

### 3. **intro_python** - Programación Python Básica
- ✅ Scripts Python para ETL (`backend/etl/download_c5.py`, `process_c5.py`)
- ✅ Lógica de negocio en servicios (`backend/services/`)
- ✅ Manejo de errores y validaciones
- ✅ Type hints y docstrings

**Archivos relevantes:**
- `backend/etl/download_c5.py`
- `backend/etl/process_c5.py`
- `backend/services/stats_service.py`
- `backend/services/certificates_service.py`

### 4. **intro_python_interactivo** - Notebooks Jupyter
- ✅ Notebook de exploración de datos C5
- ✅ Uso interactivo de pandas y numpy
- ✅ Visualizaciones con matplotlib/seaborn

**Archivos relevantes:**
- `notebooks/01_exploracion_c5.ipynb`

### 5. **pandas** y **pandas_v2** - Procesamiento de Datos
- ✅ Carga y limpieza de CSV con pandas
- ✅ Transformaciones y agregaciones
- ✅ Análisis estadísticos por zona, tipo, hora
- ✅ ETL completo de datos C5

**Archivos relevantes:**
- `backend/etl/process_c5.py` (ETL con pandas)
- `backend/services/stats_service.py` (análisis con pandas)
- `notebooks/01_exploracion_c5.ipynb` (exploración interactiva)

### 6. **numpy** - Cálculos Numéricos
- ✅ Estadísticas descriptivas (media, mediana, percentiles)
- ✅ Operaciones vectoriales sobre arrays
- ✅ Integración con pandas para análisis numérico

**Archivos relevantes:**
- `backend/services/stats_service.py`
- `notebooks/01_exploracion_c5.ipynb`

### 7. **certificados** - Generación de PDF
- ✅ Plantilla HTML con Jinja2 (`backend/templates/certificado_zona.html`)
- ✅ Conversión HTML→PDF con WeasyPrint
- ✅ Certificados personalizados por zona con estadísticas

**Archivos relevantes:**
- `backend/services/certificates_service.py`
- `backend/templates/certificado_zona.html`
- `backend/routers/certificates.py` (endpoint `/certificates/zona`)

### 8. **computo_distribuido** - Procesamiento Paralelo
- ✅ Uso de `multiprocessing.Pool` y `ProcessPoolExecutor`
- ✅ Procesamiento de chunks grandes de datos en paralelo
- ✅ Procesamiento de múltiples archivos históricos simultáneamente

**Archivos relevantes:**
- `backend/etl/distributed.py` (ejemplos didácticos de cómputo distribuido)

### 9. **docker** y **dockerhub** - Contenedores
- ✅ Dockerfile para backend con todas las dependencias
- ✅ Dockerfile opcional para frontend (nginx)
- ✅ docker-compose.yml para orquestar servicios
- ✅ Instrucciones para construir y subir imagen a DockerHub

**Archivos relevantes:**
- `docker/Dockerfile.backend`
- `docker/Dockerfile.frontend`
- `docker/docker-compose.yml`

### 10. **vscode** - Desarrollo en VSCode/Cursor
- ✅ Estructura de proyecto clara y navegable
- ✅ Type hints para mejor autocompletado
- ✅ Configuración recomendada para debugging
- ✅ Extensiones sugeridas (Python, Jupyter, Docker)

## 🚀 Instalación y Uso

### Prerrequisitos

- Python 3.11 o superior
- pip (gestor de paquetes Python)
- Git
- (Opcional) Docker y Docker Compose

### Paso 1: Clonar el Repositorio

```bash
cd /home/bernardo
git clone <url-del-repo> waze-ciudadano-cdmx
cd waze-ciudadano-cdmx
```

### Paso 2: Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate
```

### Paso 3: Instalar Dependencias

```bash
# Instalar dependencias del backend
pip install -r backend/requirements.txt
```

**Nota para WeasyPrint:** Si planeas generar certificados PDF, necesitarás instalar dependencias del sistema. En Ubuntu/Debian:

```bash
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libfontconfig1 libcairo2 libgdk-pixbuf2.0-0
```

### Paso 4: Descargar Datos del C5

**Opción A: Usando script Python**
```bash
python backend/etl/download_c5.py
```

**Opción B: Usando script bash**
```bash
bash scripts/download_c5.sh
```

**Nota:** La URL del CSV puede cambiar. Verifica en [Datos Abiertos CDMX](https://datos.cdmx.gob.mx/dataset/incidentes-viales-c5) y actualiza la constante `C5_CSV_URL` en `backend/etl/download_c5.py` si es necesario.

### Paso 5: Procesar Datos del C5

```bash
# Procesar CSV y cargar a base de datos
python backend/etl/process_c5.py
```

Esto:
- Lee el CSV crudo de `data/raw/incidentesc5.csv`
- Limpia y transforma los datos
- Guarda CSV procesado en `data/processed/`
- Inserta datos en la base de datos SQLite (`data/waze_cdmx.db`)

**Nota:** Es posible que necesites ajustar los nombres de columnas en `process_c5.py` según el esquema real del CSV del C5.

### Paso 6: Inicializar Base de Datos

La base de datos se inicializa automáticamente al arrancar la API, pero puedes hacerlo manualmente:

```bash
python -c "from backend.database import init_db; init_db()"
```

### Paso 7: Levantar la API Backend

```bash
# Desde la raíz del proyecto
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en:
- API: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs
- Documentación alternativa: http://localhost:8000/redoc

### Paso 8: Servir el Frontend

**Opción A: Live Server (VSCode)**
1. Instala la extensión "Live Server" en VSCode
2. Abre `frontend/index.html`
3. Clic derecho → "Open with Live Server"

**Opción B: Python HTTP Server**
```bash
cd frontend
python3 -m http.server 5500
```

**Opción C: Node.js http-server**
```bash
npx http-server frontend -p 5500
```

Abre en el navegador: http://localhost:5500

### Paso 9: Usar la Aplicación

1. **Ver reportes en el mapa:** Los reportes se cargan automáticamente al abrir la página
2. **Crear nuevo reporte:** Completa el formulario y haz clic en "Enviar Reporte"
3. **Usar mi ubicación:** Haz clic en "Usar Mi Ubicación" para obtener coordenadas automáticamente
4. **Ver estadísticas:** Haz clic en "Cargar Top Zonas" en el panel de estadísticas

## 📊 Endpoints de la API

### Reportes

- `POST /reports` - Crear nuevo reporte ciudadano
- `GET /reports` - Listar reportes (con filtros opcionales: `?tipo=bache&alcaldia=Benito Juárez&limit=50`)

### Estadísticas

- `GET /stats/top-zonas?tipo_zona=colonia&limit=10` - Top zonas con más incidentes
- `GET /stats/horas-peligrosas` - Distribución de incidentes por hora

### Certificados

- `GET /certificates/zona?tipo_zona=colonia&nombre_zona=Narvarte Poniente` - Genera certificado PDF

### Health Check

- `GET /health` - Verificar estado de la API
- `GET /` - Información básica de la API

## 🐳 Docker

### Construir Imagen del Backend

```bash
cd docker
docker build -f Dockerfile.backend -t waze-cdmx-backend ..
```

### Ejecutar Contenedor

```bash
docker run -p 8000:8000 -v $(pwd)/../data:/app/data waze-cdmx-backend
```

### Usar Docker Compose

```bash
cd docker
docker-compose up --build
```

Esto levantará:
- Backend en http://localhost:8000
- Frontend en http://localhost:8080

### Subir a DockerHub

```bash
# Taggear la imagen
docker tag waze-cdmx-backend tu-usuario/waze-cdmx-backend:latest

# Login a DockerHub
docker login

# Push
docker push tu-usuario/waze-cdmx-backend:latest
```

## 📓 Notebooks

Explora los datos del C5 interactivamente:

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar jupyter si no está instalado
pip install jupyter matplotlib seaborn

# Abrir Jupyter
jupyter notebook notebooks/01_exploracion_c5.ipynb
```

## 🔧 Configuración y Ajustes

### Ajustar URL del CSV del C5

Si la URL del CSV cambia, edita:
- `backend/etl/download_c5.py` (línea `C5_CSV_URL`)
- `scripts/download_c5.sh` (variable `URL`)

### Ajustar Nombres de Columnas del CSV

El CSV del C5 puede tener nombres de columnas diferentes. Ajusta el mapeo en:
- `backend/etl/process_c5.py` (diccionario `column_mapping`)

### Cambiar Base de Datos a Postgres

Edita `backend/database.py`:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://usuario:password@localhost/waze_cdmx"
```

Y actualiza `requirements.txt` para incluir `psycopg2-binary`.

## 🧪 Ejemplos de Uso

### Crear un Reporte vía API

```bash
curl -X POST "http://localhost:8000/reports" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "bache",
    "descripcion": "Bache grande en avenida principal",
    "lat": 19.4326,
    "lon": -99.1332,
    "alcaldia": "Benito Juárez",
    "colonia": "Narvarte Poniente"
  }'
```

### Obtener Top Colonias

```bash
curl "http://localhost:8000/stats/top-zonas?tipo_zona=colonia&limit=5"
```

### Generar Certificado PDF

```bash
curl "http://localhost:8000/certificates/zona?tipo_zona=colonia&nombre_zona=Narvarte%20Poniente" \
  --output certificado.pdf
```

## 📝 Estructura de Datos

### Modelo C5Incident

- `id`: ID único
- `fecha_hora`: Fecha y hora del incidente
- `anio`, `mes`, `hora`, `dia_semana`: Componentes temporales
- `tipo_incidente`: Tipo de incidente
- `alcaldia`, `colonia`: Ubicación
- `latitud`, `longitud`: Coordenadas
- `fuente`: "c5"

### Modelo UserReport

- `id`: ID único
- `created_at`: Fecha de creación
- `tipo`: Tipo de incidente (bache, choque, etc.)
- `descripcion`: Descripción opcional
- `lat`, `lon`: Coordenadas
- `alcaldia`, `colonia`: Ubicación opcional
- `fuente`: "usuario"

## 🐛 Troubleshooting

### Error: "No module named 'backend'"

Asegúrate de estar en la raíz del proyecto y que el entorno virtual esté activado.

### Error: WeasyPrint no genera PDF

Instala las dependencias del sistema (ver Paso 3).

### Error: CORS en el frontend

Verifica que `API_BASE_URL` en `frontend/app.js` apunte a `http://localhost:8000`.

### Error: No se encuentra el CSV

Ejecuta `python backend/etl/download_c5.py` o `bash scripts/download_c5.sh`.

## 📚 Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Leaflet Documentation](https://leafletjs.com/)
- [Datos Abiertos CDMX](https://datos.cdmx.gob.mx/)
- [WeasyPrint Documentation](https://weasyprint.org/)

## 👥 Contribuciones

Este es un proyecto educativo. Siéntete libre de:
- Reportar bugs
- Sugerir mejoras
- Agregar funcionalidades
- Mejorar documentación

## 📄 Licencia

Este proyecto es de uso educativo. Los datos del C5 son públicos y provienen de Datos Abiertos CDMX.

---

**Desarrollado como Proyecto Final del Curso "Fuentes de Datos"**

Integra: GitHub, Python, pandas, numpy, cómputo distribuido, certificados PDF, Docker y desarrollo en VSCode/Cursor.

