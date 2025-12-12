/**
 * Aplicación principal del frontend.
 * 
 * Maneja:
 * - Mapa Leaflet con marcadores de reportes
 * - Formulario de creación de reportes
 * - Actualización periódica de reportes
 * - Estadísticas
 */

// Configuración
const API_BASE_URL = "http://localhost:8000";
const UPDATE_INTERVAL = 30000; // 30 segundos

// Variables globales
let map;
let markers = [];
let updateIntervalId;

// Inicializar mapa
function initMap() {
    // Coordenadas de CDMX (centro aproximado)
    const cdmxCenter = [19.4326, -99.1332];
    
    // Crear mapa
    map = L.map('map').setView(cdmxCenter, 12);
    
    // Agregar capa base de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{s}/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Agregar marcador de ejemplo en el centro
    const centerMarker = L.marker(cdmxCenter).addTo(map);
    centerMarker.bindPopup("Centro de CDMX").openPopup();
    
    // Permitir hacer clic en el mapa para obtener coordenadas
    map.on('click', function(e) {
        const { lat, lng } = e.latlng;
        document.getElementById('lat').value = lat.toFixed(6);
        document.getElementById('lon').value = lng.toFixed(6);
    });
}

// Cargar reportes desde la API
async function cargarReportes() {
    try {
        const response = await fetch(`${API_BASE_URL}/reports?limit=200`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const reports = await response.json();
        
        // Limpiar marcadores anteriores
        markers.forEach(marker => map.removeLayer(marker));
        markers = [];
        
        // Agregar marcadores al mapa
        reports.forEach(report => {
            const marker = L.circleMarker(
                [report.lat, report.lon],
                {
                    radius: 8,
                    fillColor: getColorByTipo(report.tipo),
                    color: '#333',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.7
                }
            ).addTo(map);
            
            marker.bindPopup(`
                <strong>${report.tipo}</strong><br>
                ${report.descripcion || 'Sin descripción'}<br>
                <small>${report.colonia || report.alcaldia || 'Ubicación desconocida'}</small><br>
                <small>${new Date(report.created_at).toLocaleString('es-MX')}</small>
            `);
            
            markers.push(marker);
        });
        
        // Actualizar lista de reportes
        actualizarListaReportes(reports);
        
        console.log(`✓ ${reports.length} reportes cargados`);
    } catch (error) {
        console.error('Error al cargar reportes:', error);
        document.getElementById('reports-list').innerHTML = 
            '<p class="error">Error al cargar reportes. Verifica que la API esté corriendo.</p>';
    }
}

// Obtener color según tipo de incidente
function getColorByTipo(tipo) {
    const colors = {
        'bache': '#ff6b6b',
        'choque': '#ee5a6f',
        'semaforo': '#feca57',
        'inundacion': '#48dbfb',
        'manifestacion': '#ff9ff3',
        'otro': '#a55eea'
    };
    return colors[tipo] || '#95a5a6';
}

// Actualizar lista de reportes en el sidebar
function actualizarListaReportes(reports) {
    const listContainer = document.getElementById('reports-list');
    
    if (reports.length === 0) {
        listContainer.innerHTML = '<p>No hay reportes aún.</p>';
        return;
    }
    
    const html = reports.slice(0, 10).map(report => `
        <div class="report-item">
            <strong>${report.tipo}</strong>
            <p>${report.colonia || report.alcaldia || 'Ubicación desconocida'}</p>
            <small>${new Date(report.created_at).toLocaleString('es-MX')}</small>
        </div>
    `).join('');
    
    listContainer.innerHTML = html;
}

// Manejar envío de formulario
document.getElementById('report-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        tipo: document.getElementById('tipo').value,
        descripcion: document.getElementById('descripcion').value,
        lat: parseFloat(document.getElementById('lat').value),
        lon: parseFloat(document.getElementById('lon').value),
        alcaldia: document.getElementById('alcaldia').value || null,
        colonia: document.getElementById('colonia').value || null
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/reports`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al crear reporte');
        }
        
        const newReport = await response.json();
        console.log('✓ Reporte creado:', newReport);
        
        // Mostrar mensaje de éxito
        alert('✓ Reporte creado exitosamente');
        
        // Limpiar formulario
        document.getElementById('report-form').reset();
        
        // Recargar reportes
        cargarReportes();
        
    } catch (error) {
        console.error('Error al crear reporte:', error);
        alert(`✗ Error: ${error.message}`);
    }
});

// Usar ubicación actual
document.getElementById('btn-use-current-location').addEventListener('click', function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                
                document.getElementById('lat').value = lat.toFixed(6);
                document.getElementById('lon').value = lon.toFixed(6);
                
                // Centrar mapa en la ubicación
                map.setView([lat, lon], 15);
                
                alert('✓ Ubicación obtenida');
            },
            function(error) {
                alert('✗ Error al obtener ubicación: ' + error.message);
            }
        );
    } else {
        alert('✗ Tu navegador no soporta geolocalización');
    }
});

// Cargar estadísticas
document.getElementById('btn-load-stats').addEventListener('click', async function() {
    const statsContent = document.getElementById('stats-content');
    statsContent.innerHTML = '<p class="loading">Cargando estadísticas...</p>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/stats/top-zonas?tipo_zona=colonia&limit=10`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const stats = await response.json();
        
        if (stats.length === 0) {
            statsContent.innerHTML = '<p>No hay estadísticas disponibles.</p>';
            return;
        }
        
        const html = `
            <h3>Top 10 Colonias con Más Incidentes</h3>
            <ul class="stats-list">
                ${stats.map(stat => `
                    <li>
                        <strong>${stat.zona}</strong>
                        <span class="stat-number">${stat.total_incidentes}</span>
                        <small>C5: ${stat.incidentes_c5} | Usuarios: ${stat.incidentes_usuarios}</small>
                    </li>
                `).join('')}
            </ul>
        `;
        
        statsContent.innerHTML = html;
        
    } catch (error) {
        console.error('Error al cargar estadísticas:', error);
        statsContent.innerHTML = '<p class="error">Error al cargar estadísticas.</p>';
    }
});

// Inicializar aplicación
document.addEventListener('DOMContentLoaded', function() {
    initMap();
    cargarReportes();
    
    // Actualizar reportes periódicamente
    updateIntervalId = setInterval(cargarReportes, UPDATE_INTERVAL);
    
    console.log('✓ Aplicación inicializada');
});

