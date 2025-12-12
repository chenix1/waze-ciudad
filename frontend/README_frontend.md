# Frontend - Waze Ciudadano CDMX

## Descripción

Frontend web para visualizar y crear reportes de incidentes viales en CDMX.

## Tecnologías

- HTML5
- JavaScript (ES6+)
- CSS3
- Leaflet (mapas interactivos)
- OpenStreetMap (tiles de mapa)

## Cómo Servir el Frontend

### Opción 1: Live Server (VSCode)

1. Instala la extensión "Live Server" en VSCode
2. Abre `index.html`
3. Haz clic derecho → "Open with Live Server"

### Opción 2: Python HTTP Server

```bash
cd frontend
python3 -m http.server 5500
```

Luego abre: http://localhost:5500

### Opción 3: Node.js http-server

```bash
npx http-server frontend -p 5500
```

## Configuración

Asegúrate de que la API backend esté corriendo en `http://localhost:8000`.

Si la API está en otra URL, edita `API_BASE_URL` en `app.js`.

## Funcionalidades

- Mapa interactivo con marcadores de reportes
- Formulario para crear nuevos reportes
- Actualización automática cada 30 segundos
- Estadísticas de top zonas
- Geolocalización del usuario

