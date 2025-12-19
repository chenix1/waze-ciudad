const API_BASE_URL = "http://localhost:8000";
let map, markers = [];
let dragMarker = null;

function initMap() {
    console.log('Iniciando mapa...');
    const center = [19.4326, -99.1332];
    map = L.map('map').setView(center, 12);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    setTimeout(function() { map.invalidateSize(); }, 100);
    
    dragMarker = L.marker(center, {
        draggable: true,
        icon: L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        })
    }).addTo(map);
    
    dragMarker.bindPopup("Arrastra este marcador").openPopup();
    
    dragMarker.on('dragend', function(e) {
        const pos = e.target.getLatLng();
        document.getElementById('lat').value = pos.lat.toFixed(6);
        document.getElementById('lon').value = pos.lng.toFixed(6);
        dragMarker.bindPopup("Lat: " + pos.lat.toFixed(6) + "<br>Lon: " + pos.lng.toFixed(6)).openPopup();
    });
    
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;
        dragMarker.setLatLng([lat, lng]);
        document.getElementById('lat').value = lat.toFixed(6);
        document.getElementById('lon').value = lng.toFixed(6);
        dragMarker.bindPopup("Lat: " + lat.toFixed(6) + "<br>Lon: " + lng.toFixed(6)).openPopup();
    });
    
    console.log('Mapa listo');
}

async function cargarReportes() {
    try {
        const r = await fetch(API_BASE_URL + '/reports?limit=200');
        const data = await r.json();
        
        markers.forEach(function(m) { map.removeLayer(m); });
        markers = [];
        
        data.forEach(function(rep) {
            const m = L.circleMarker([rep.lat, rep.lon], {
                radius: 8,
                fillColor: '#ff6b6b',
                color: '#333',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.7
            }).addTo(map);
            
            m.bindPopup(
                '<strong>' + rep.tipo + '</strong><br>' +
                (rep.descripcion || 'Sin descripción') + '<br>' +
                '<small>' + (rep.colonia || rep.alcaldia || 'Sin ubicación') + '</small>'
            );
            
            markers.push(m);
        });
        
        console.log('Reportes cargados:', data.length);
        
        const lista = document.getElementById('reports-list');
        if (data.length === 0) {
            lista.innerHTML = '<p>No hay reportes</p>';
        } else {
            lista.innerHTML = data.slice(0, 10).map(function(r) {
                return '<div class="report-item">' +
                    '<strong>' + r.tipo + '</strong>' +
                    '<p>' + (r.colonia || r.alcaldia || 'Sin ubicación') + '</p>' +
                    '<small>' + new Date(r.created_at).toLocaleString('es-MX') + '</small>' +
                    '</div>';
            }).join('');
        }
        
    } catch(e) {
        console.error('Error:', e);
        document.getElementById('reports-list').innerHTML = '<p class="error">Error al cargar reportes</p>';
    }
}

function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function verEnMapa(lat, lon) {
    closeModal('reportsModal');
    map.setView([lat, lon], 16);
    dragMarker.setLatLng([lat, lon]);
}

function setupModalButtons() {
    const reportsPanel = document.querySelector('#reports-list').parentElement;
    const btnViewReports = document.createElement('button');
    btnViewReports.className = 'btn-view-modal';
    btnViewReports.textContent = 'Ver Todos los Reportes';
    btnViewReports.onclick = function() {
        loadAllReportsModal();
    };
    reportsPanel.insertBefore(btnViewReports, document.querySelector('#reports-list'));
    
    window.onclick = function(event) {
        if (event.target.className === 'modal') {
            event.target.style.display = 'none';
        }
    };
}

async function loadAllReportsModal() {
    openModal('reportsModal');
    const container = document.getElementById('allReportsContainer');
    container.innerHTML = '<p class="loading">Cargando reportes...</p>';
    
    try {
        const r = await fetch(API_BASE_URL + '/reports?limit=1000');
        const data = await r.json();
        
        if (data.length === 0) {
            container.innerHTML = '<p>No hay reportes registrados.</p>';
            return;
        }
        
        container.innerHTML = data.map(function(rep) {
            return '<div class="report-card" onclick="verEnMapa(' + rep.lat + ',' + rep.lon + ')">' +
                '<h3>📍 ' + rep.tipo + '</h3>' +
                '<div class="meta">' +
                '<span>📅 ' + new Date(rep.created_at).toLocaleString('es-MX') + '</span>' +
                '<span>🏘️ ' + (rep.colonia || rep.alcaldia || 'Sin ubicación') + '</span>' +
                '</div>' +
                (rep.descripcion ? '<div class="description">' + rep.descripcion + '</div>' : '') +
                '<div style="margin-top:10px;"><small>Lat: ' + rep.lat.toFixed(6) + ', Lon: ' + rep.lon.toFixed(6) + '</small></div>' +
                '</div>';
        }).join('');
        
    } catch(e) {
        container.innerHTML = '<p class="error">Error al cargar reportes</p>';
    }
}

function setupUseLocationButton() {
    const btn = document.getElementById('btn-use-current-location');
    if (btn) {
        btn.addEventListener('click', function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        dragMarker.setLatLng([lat, lon]);
                        map.setView([lat, lon], 15);
                        document.getElementById('lat').value = lat.toFixed(6);
                        document.getElementById('lon').value = lon.toFixed(6);
                        dragMarker.bindPopup("Tu ubicación actual").openPopup();
                        alert('Ubicación obtenida');
                    },
                    function(error) {
                        alert('Error: ' + error.message);
                    }
                );
            } else {
                alert('Tu navegador no soporta geolocalización');
            }
        });
    }
}

function setupReportForm() {
    const form = document.getElementById('report-form');
    if (form) {
        form.addEventListener('submit', async function(e) {
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
                const r = await fetch(API_BASE_URL + '/reports', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(formData)
                });
                
                if (!r.ok) {
                    const error = await r.json();
                    throw new Error(error.detail || 'Error al crear reporte');
                }
                
                alert('Reporte creado exitosamente');
                form.reset();
                cargarReportes();
                
            } catch(error) {
                alert('Error: ' + error.message);
            }
        });
    }
}

function setupStatsButton() {
    const btn = document.getElementById('btn-load-stats');
    if (btn) {
        btn.textContent = 'Ver Estadísticas';
        btn.addEventListener('click', async function() {
            await openStatsModalWithFilters();
        });
    }
}

async function openStatsModalWithFilters() {
    openModal('statsModal');
    const statsDiv = document.getElementById('allStatsContainer');
    
    // Cargar opciones de filtros
    statsDiv.innerHTML = '<p class="loading">Cargando opciones...</p>';
    
    try {
        const r = await fetch(API_BASE_URL + '/stats/opciones');
        const opciones = await r.json();
        
        console.log('Opciones recibidas:', opciones);
        
        // Crear formulario de filtros
        statsDiv.innerHTML = `
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="margin-top: 0;">🔍 Filtros de Búsqueda</h3>
                <p style="color: #666; font-size: 0.9em; margin-bottom: 15px;">
                    Selecciona al menos un filtro para consultar las estadísticas
                </p>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 500;">
                        Tipo de Incidente:
                    </label>
                    <select id="filtro-tipo" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <option value="">(Opcional)</option>
                        ${opciones.tipos_incidente.map(t => `<option value="${t}">${t}</option>`).join('')}
                    </select>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 500;">
                        Alcaldía:
                    </label>
                    <select id="filtro-alcaldia" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <option value="">(Opcional)</option>
                        ${opciones.alcaldias.map(a => `<option value="${a}">${a}</option>`).join('')}
                    </select>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 500;">
                        Colonia:
                    </label>
                    <select id="filtro-colonia" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <option value="">(Opcional)</option>
                        ${opciones.colonias.map(c => `<option value="${c}">${c}</option>`).join('')}
                    </select>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 500;">
                        Límite de resultados:
                    </label>
                    <select id="filtro-limit" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                        <option value="20">20 resultados</option>
                        <option value="50" selected>50 resultados</option>
                        <option value="100">100 resultados</option>
                    </select>
                </div>
                
                <button id="btn-buscar-stats" style="width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 4px; font-weight: 500; cursor: pointer; font-size: 16px;">
                    🔎 Consultar Estadísticas
                </button>
                
                <div id="error-filtros" style="color: #e74c3c; margin-top: 10px; display: none;">
                    ⚠️ Debes seleccionar al menos un filtro
                </div>
            </div>
            
            <div id="resultados-stats" style="margin-top: 20px;"></div>
        `;
        
        // Agregar evento al botón de búsqueda
        document.getElementById('btn-buscar-stats').addEventListener('click', buscarEstadisticas);
        
    } catch(e) {
        console.error('Error:', e);
        statsDiv.innerHTML = '<p class="error">Error al cargar opciones: ' + e.message + '</p>';
    }
}

async function buscarEstadisticas() {
    const tipo = document.getElementById('filtro-tipo').value;
    const alcaldia = document.getElementById('filtro-alcaldia').value;
    const colonia = document.getElementById('filtro-colonia').value;
    const limit = document.getElementById('filtro-limit').value;
    
    // Validar que al menos un filtro esté seleccionado
    if (!tipo && !alcaldia && !colonia) {
        document.getElementById('error-filtros').style.display = 'block';
        return;
    }
    
    document.getElementById('error-filtros').style.display = 'none';
    
    const resultadosDiv = document.getElementById('resultados-stats');
    resultadosDiv.innerHTML = '<p class="loading">Consultando estadísticas...</p>';
    
    try {
        // Construir URL con parámetros
        let url = API_BASE_URL + '/stats/filtradas?limit=' + limit;
        if (tipo) url += '&tipo_incidente=' + encodeURIComponent(tipo);
        if (alcaldia) url += '&alcaldia=' + encodeURIComponent(alcaldia);
        if (colonia) url += '&colonia=' + encodeURIComponent(colonia);
        
        console.log('Consultando:', url);
        
        const r = await fetch(url);
        const data = await r.json();
        
        console.log('Resultados:', data);
        
        if (data.error) {
            resultadosDiv.innerHTML = '<p class="error">Error: ' + data.error + '</p>';
            return;
        }
        
        // Mostrar resumen
        let html = `
            <div style="background: #e8f5e9; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="margin-top: 0; color: #2e7d32;">📊 Resumen de Consulta</h3>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                    <div>
                        <strong>Total Incidentes:</strong><br>
                        <span style="font-size: 24px; color: #667eea;">${data.total_incidentes}</span>
                    </div>
                    <div>
                        <strong>Datos C5:</strong><br>
                        <span style="font-size: 24px; color: #667eea;">${data.incidentes_c5}</span>
                    </div>
                    <div>
                        <strong>Reportes Usuarios:</strong><br>
                        <span style="font-size: 24px; color: #667eea;">${data.incidentes_usuarios}</span>
                    </div>
                </div>
            </div>
        `;
        
        // Filtros aplicados
        html += '<div style="background: #fff3cd; padding: 10px; border-radius: 4px; margin-bottom: 20px; font-size: 0.9em;">';
        html += '<strong>Filtros aplicados:</strong> ';
        const filtros = [];
        if (data.filtros_aplicados.tipo_incidente) filtros.push('Tipo: ' + data.filtros_aplicados.tipo_incidente);
        if (data.filtros_aplicados.alcaldia) filtros.push('Alcaldía: ' + data.filtros_aplicados.alcaldia);
        if (data.filtros_aplicados.colonia) filtros.push('Colonia: ' + data.filtros_aplicados.colonia);
        html += filtros.join(' | ');
        html += '</div>';
        
        // Top Colonias
        if (data.top_colonias && data.top_colonias.length > 0) {
            html += '<h3>🏘️ Top Colonias</h3>';
            html += '<table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">';
            html += '<thead><tr style="background: #667eea; color: white;">';
            html += '<th style="padding: 10px; text-align: left;">Posición</th>';
            html += '<th style="padding: 10px; text-align: left;">Colonia</th>';
            html += '<th style="padding: 10px; text-align: center;">Total</th>';
            html += '</tr></thead><tbody>';
            
            data.top_colonias.forEach(function(item, i) {
                html += '<tr style="border-bottom: 1px solid #ddd;">';
                html += '<td style="padding: 10px;"><strong>' + (i + 1) + '</strong></td>';
                html += '<td style="padding: 10px;">' + item.colonia + '</td>';
                html += '<td style="padding: 10px; text-align: center; font-weight: bold; color: #667eea;">' + item.total + '</td>';
                html += '</tr>';
            });
            
            html += '</tbody></table>';
        }
        
        // Top Tipos
        if (data.top_tipos && data.top_tipos.length > 0) {
            html += '<h3>🚗 Top Tipos de Incidente</h3>';
            html += '<table style="width: 100%; border-collapse: collapse;">';
            html += '<thead><tr style="background: #667eea; color: white;">';
            html += '<th style="padding: 10px; text-align: left;">Tipo</th>';
            html += '<th style="padding: 10px; text-align: center;">Total</th>';
            html += '</tr></thead><tbody>';
            
            data.top_tipos.forEach(function(item) {
                html += '<tr style="border-bottom: 1px solid #ddd;">';
                html += '<td style="padding: 10px;">' + item.tipo + '</td>';
                html += '<td style="padding: 10px; text-align: center; font-weight: bold; color: #667eea;">' + item.total + '</td>';
                html += '</tr>';
            });
            
            html += '</tbody></table>';
        }
        
        resultadosDiv.innerHTML = html;
        
    } catch(e) {
        console.error('Error:', e);
        resultadosDiv.innerHTML = '<p class="error">Error al consultar: ' + e.message + '</p>';
    }
}

function setupStatsPanel() {
    cargarOpcionesIniciales();
    
    document.getElementById('stat-alcaldia').addEventListener('change', async function() {
        const alcaldia = this.value;
        const coloniaSelect = document.getElementById('stat-colonia');
        
        if (!alcaldia) {
            coloniaSelect.disabled = true;
            coloniaSelect.innerHTML = '<option value="">Primero selecciona alcaldía</option>';
            return;
        }
        
        coloniaSelect.innerHTML = '<option value="">Cargando...</option>';
        coloniaSelect.disabled = true;
        
        try {
            const r = await fetch(API_BASE_URL + '/stats/colonias/' + encodeURIComponent(alcaldia));
            const data = await r.json();
            
            coloniaSelect.innerHTML = '<option value="">(Opcional)</option>' +
                data.colonias.map(c => '<option value="' + c + '">' + c + '</option>').join('');
            coloniaSelect.disabled = false;
            
        } catch(e) {
            coloniaSelect.innerHTML = '<option value="">Error al cargar</option>';
        }
    });
    
    document.getElementById('btn-consultar-stats').addEventListener('click', consultarStats);
}

async function cargarOpcionesIniciales() {
    try {
        const r = await fetch(API_BASE_URL + '/stats/opciones');
        const data = await r.json();
        
        const tipoSelect = document.getElementById('stat-tipo');
        tipoSelect.innerHTML = '<option value="">(Opcional)</option>' +
            data.tipos_incidente.map(t => '<option value="' + t + '">' + t + '</option>').join('');
        
        const alcaldiaSelect = document.getElementById('stat-alcaldia');
        alcaldiaSelect.innerHTML = '<option value="">(Opcional)</option>' +
            data.alcaldias.map(a => '<option value="' + a + '">' + a + '</option>').join('');
        
        console.log('Opciones cargadas:', data.tipos_incidente.length, 'tipos,', data.alcaldias.length, 'alcaldias');
        
    } catch(e) {
        console.error('Error cargando opciones:', e);
    }
}

async function consultarStats() {
    const tipo = document.getElementById('stat-tipo').value;
    const alcaldia = document.getElementById('stat-alcaldia').value;
    const colonia = document.getElementById('stat-colonia').value;
    
    const resultsDiv = document.getElementById('stats-results');
    
    if (!tipo && !alcaldia && !colonia) {
        resultsDiv.innerHTML = '<p class="error">Selecciona al menos un filtro</p>';
        return;
    }
    
    resultsDiv.innerHTML = '<p class="loading">Consultando...</p>';
    
    try {
        let url = API_BASE_URL + '/stats/filtradas?limit=20';
        if (tipo) url += '&tipo_incidente=' + encodeURIComponent(tipo);
        if (alcaldia) url += '&alcaldia=' + encodeURIComponent(alcaldia);
        if (colonia) url += '&colonia=' + encodeURIComponent(colonia);
        
        const r = await fetch(url);
        const data = await r.json();
        
        if (data.error) {
            resultsDiv.innerHTML = '<p class="error">' + data.error + '</p>';
            return;
        }
        
        let html = '<div style="background:#e8f5e9; padding:10px; border-radius:4px; margin:10px 0;">';
        html += '<strong>Total: ' + data.total_incidentes + '</strong><br>';
        html += '<small>C5: ' + data.incidentes_c5 + ' | Usuarios: ' + data.incidentes_usuarios + '</small>';
        html += '</div>';
        
        html += '<button onclick="verStatsDetalladas()" class="btn-secondary" style="margin-top:10px;">Ver Detalles Completos</button>';
        
        resultsDiv.innerHTML = html;
        
        window.lastStatsData = data;
        
    } catch(e) {
        resultsDiv.innerHTML = '<p class="error">Error: ' + e.message + '</p>';
    }
}

function verStatsDetalladas() {
    if (!window.lastStatsData) return;
    
    openModal('statsModal');
    const data = window.lastStatsData;
    
    let html = '<div style="background:#e8f5e9; padding:15px; border-radius:8px; margin-bottom:20px;">';
    html += '<h3 style="margin-top:0;">📊 Resultados Detallados</h3>';
    html += '<p><strong>Total: ' + data.total_incidentes + '</strong> | ';
    html += 'C5: ' + data.incidentes_c5 + ' | Usuarios: ' + data.incidentes_usuarios + '</p>';
    html += '</div>';
    
    if (data.top_tipos && data.top_tipos.length > 0) {
        html += '<h3>🚗 Tipos de Incidente</h3><table style="width:100%; border-collapse:collapse;">';
        html += '<tr style="background:#667eea; color:white;"><th style="padding:8px;">Tipo</th><th style="padding:8px;">Total</th></tr>';
        data.top_tipos.forEach(function(t) {
            html += '<tr style="border-bottom:1px solid #ddd;"><td style="padding:8px;">' + t.tipo + '</td>';
            html += '<td style="padding:8px; text-align:center; font-weight:bold;">' + t.total + '</td></tr>';
        });
        html += '</table>';
    }
    
    if (data.top_colonias && data.top_colonias.length > 0) {
        html += '<h3 style="margin-top:20px;">🏘️ Top Colonias</h3><table style="width:100%; border-collapse:collapse;">';
        html += '<tr style="background:#667eea; color:white;"><th style="padding:8px;">Colonia</th><th style="padding:8px;">Total</th></tr>';
        data.top_colonias.forEach(function(c) {
            html += '<tr style="border-bottom:1px solid #ddd;"><td style="padding:8px;">' + c.colonia + '</td>';
            html += '<td style="padding:8px; text-align:center; font-weight:bold;">' + c.total + '</td></tr>';
        });
        html += '</table>';
    }
    
    document.getElementById('allStatsContainer').innerHTML = html;
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando...');
    initMap();
    cargarReportes();
    setupUseLocationButton();
    setupReportForm();
    setupStatsPanel();
    setupModalButtons();
    setInterval(cargarReportes, 30000);
    console.log('Listo!');
});
