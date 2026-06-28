# Copyright 2026
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request


class GpsTrackingController(http.Controller):

    @http.route('/fleet/gps/tracking', type='http', auth='user', website=True)
    def gps_tracking_page(self, **kwargs):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>GPS Vehicle Tracking</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
            <style>
                body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
                .main-container { padding: 30px; }
                .header-card { background: rgba(255,255,255,0.95); border-radius: 20px; border: none; box-shadow: 0 20px 60px rgba(0,0,0,0.15); margin-bottom: 25px; }
                .tracking-card { background: rgba(255,255,255,0.95); border-radius: 20px; border: none; box-shadow: 0 20px 60px rgba(0,0,0,0.15); overflow: hidden; margin-bottom: 25px; }
                .tracking-card .card-body { padding: 0; }
                .iframe-container { position: relative; width: 100%; }
                .iframe-container iframe { width: 100%; height: 800px; border: none; display: block; }
                .iframe-container iframe { pointer-events: auto; }
                .btn-elegant { padding: 12px 30px; border-radius: 25px; font-weight: 500; transition: all 0.3s; border: none; }
                .btn-elegant:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
                .btn-primary-elegant { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                .btn-success-elegant { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; }
                .data-display { background: rgba(255,255,255,0.95); border-radius: 20px; border: none; box-shadow: 0 20px 60px rgba(0,0,0,0.15); margin-top: 25px; }
                .data-display pre { background: #f8f9fa; border-radius: 15px; padding: 20px; margin: 0; max-height: 300px; overflow-y: auto; }
                .page-title { font-weight: 700; color: #667eea; margin-bottom: 5px; }
                .page-subtitle { color: #6c757d; font-size: 0.95rem; margin-bottom: 0; }
            </style>
        </head>
        <body>
            <div class="container main-container">
                <div class="header-card card">
                    <div class="card-body">
                        <h2 class="page-title"><i class="fas fa-map-marked-alt mr-2"></i>GPS Vehicle Tracking</h2>
                        <p class="page-subtitle">Real-time vehicle location monitoring and tracking system</p>
                    </div>
                </div>
                <div class="tracking-card card">
                    <div class="card-body">
                        <div class="iframe-container">
                            <iframe 
                                id="gps-tracking-iframe"
                                src="https://www.itrack.top/V2/index.jsp#/" 
                                allow="geolocation; fullscreen; accelerometer; gyroscope; microphone; camera; clipboard-read; clipboard-write"
                                sandbox="allow-same-origin allow-scripts allow-popups allow-forms allow-presentation allow-top-navigation allow-downgrade"
                                loading="eager"
                                referrerpolicy="no-referrer-when-downgrade">
                            </iframe>
                        </div>
                    </div>
                </div>
                <div class="text-center">
                    <button id="capture-gps-data" class="btn btn-elegant btn-primary-elegant">
                        <i class="fas fa-map-pin mr-2"></i>Capture GPS Data
                    </button>
                    <button id="view-live-tracking" class="btn btn-elegant btn-success-elegant ml-3" onclick="window.location.href='/fleet/gps/live'">
                        <i class="fas fa-broadcast-tower mr-2"></i>Live Tracking
                    </button>
                </div>
                <div id="gps-data-display" class="data-display card" style="display: none;">
                    <div class="card-body">
                        <h4 class="mb-3"><i class="fas fa-database mr-2"></i>Captured GPS Data (Session)</h4>
                        <pre id="gps-data-content"></pre>
                    </div>
                </div>
            </div>
            <script>
                const GPS_DATA_KEY = 'gps_tracking_session_data';
                
                function initSessionStorage() {
                    if (!sessionStorage.getItem(GPS_DATA_KEY)) {
                        sessionStorage.setItem(GPS_DATA_KEY, JSON.stringify([]));
                    }
                }
                
                function getGpsData() {
                    const data = sessionStorage.getItem(GPS_DATA_KEY);
                    return data ? JSON.parse(data) : [];
                }
                
                function saveGpsData(data) {
                    sessionStorage.setItem(GPS_DATA_KEY, JSON.stringify(data));
                }
                
                function addGpsEntry(entry) {
                    const currentData = getGpsData();
                    entry.timestamp = new Date().toISOString();
                    entry.id = Date.now();
                    currentData.push(entry);
                    saveGpsData(currentData);
                    return entry;
                }
                
                initSessionStorage();
                
                document.getElementById('capture-gps-data').addEventListener('click', function() {
                    const vehicleId = prompt('Vehicle ID:');
                    const licensePlate = prompt('License Plate:');
                    const latitude = prompt('Latitude:');
                    const longitude = prompt('Longitude:');
                    const status = prompt('Status (moving/stopped/idle):') || 'moving';
                    
                    if (vehicleId && licensePlate && latitude && longitude) {
                        const entry = {
                            vehicle_id: vehicleId,
                            license_plate: licensePlate,
                            latitude: parseFloat(latitude),
                            longitude: parseFloat(longitude),
                            status: status
                        };
                        addGpsEntry(entry);
                        document.getElementById('gps-data-content').textContent = JSON.stringify(getGpsData(), null, 2);
                        document.getElementById('gps-data-display').style.display = 'block';
                        alert('GPS data entry saved to session!');
                    }
                });
            </script>
        </body>
        </html>
        """
        return request.make_response(html_content, headers=[('Content-Type', 'text/html')])

    @http.route('/fleet/gps/live', type='http', auth='user', website=True)
    def gps_live_page(self, **kwargs):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Live GPS Tracking</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
            <style>
                body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
                .main-container { padding: 30px; }
                .header-card { background: rgba(255,255,255,0.95); border-radius: 20px; border: none; box-shadow: 0 20px 60px rgba(0,0,0,0.15); margin-bottom: 25px; }
                .data-card { background: rgba(255,255,255,0.95); border-radius: 20px; border: none; box-shadow: 0 20px 60px rgba(0,0,0,0.15); margin-bottom: 25px; }
                .btn-elegant { padding: 12px 30px; border-radius: 25px; font-weight: 500; transition: all 0.3s; border: none; }
                .btn-elegant:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
                .btn-primary-elegant { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                .btn-danger-elegant { background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); color: white; }
                .btn-secondary-elegant { background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%); color: white; }
                .table-custom { margin: 0; }
                .table-custom thead { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                .table-custom th { border: none; padding: 15px; font-weight: 500; }
                .table-custom td { padding: 15px; vertical-align: middle; }
                .badge-moving { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
                .badge-stopped { background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); }
                .badge-idle { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
                .data-display pre { background: #f8f9fa; border-radius: 15px; padding: 20px; margin: 0; max-height: 400px; overflow-y: auto; }
                .empty-state { text-align: center; padding: 60px 20px; color: #6c757d; }
                .empty-state i { font-size: 4rem; margin-bottom: 20px; opacity: 0.5; }
                .page-title { font-weight: 700; color: #667eea; margin-bottom: 5px; }
                .page-subtitle { color: #6c757d; font-size: 0.95rem; margin-bottom: 0; }
            </style>
        </head>
        <body>
            <div class="container main-container">
                <div class="header-card card">
                    <div class="card-body">
                        <h2 class="page-title"><i class="fas fa-broadcast-tower mr-2"></i>Live GPS Tracking</h2>
                        <p class="page-subtitle">Real-time vehicle location monitoring dashboard</p>
                    </div>
                </div>
                <div class="data-card card">
                    <div class="card-body text-center">
                        <button id="refresh-live-data" class="btn btn-elegant btn-primary-elegant">
                            <i class="fas fa-sync-alt mr-2"></i>Refresh Data
                        </button>
                        <button id="clear-session-data" class="btn btn-elegant btn-danger-elegant ml-3">
                            <i class="fas fa-trash-alt mr-2"></i>Clear Data
                        </button>
                        <button id="back-to-tracking" class="btn btn-elegant btn-secondary-elegant ml-3" onclick="window.location.href='/fleet/gps/tracking'">
                            <i class="fas fa-arrow-left mr-2"></i>Back to Tracking
                        </button>
                    </div>
                </div>
                <div class="data-card card">
                    <div class="card-body">
                        <h4 class="mb-4"><i class="fas fa-map-marker-alt mr-2"></i>Vehicle Locations</h4>
                        <div class="table-responsive">
                            <table class="table table-custom">
                                <thead>
                                    <tr>
                                        <th><i class="fas fa-id-card mr-2"></i>Vehicle ID</th>
                                        <th><i class="fas fa-id-badge mr-2"></i>License Plate</th>
                                        <th><i class="fas fa-location-arrow mr-2"></i>Latitude</th>
                                        <th><i class="fas fa-location-arrow mr-2"></i>Longitude</th>
                                        <th><i class="fas fa-clock mr-2"></i>Timestamp</th>
                                        <th><i class="fas fa-info-circle mr-2"></i>Status</th>
                                    </tr>
                                </thead>
                                <tbody id="live-tracking-body"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="data-card card">
                    <div class="card-body">
                        <h4 class="mb-3"><i class="fas fa-database mr-2"></i>Raw Session Data</h4>
                        <div class="data-display">
                            <pre id="raw-session-data">No data</pre>
                        </div>
                    </div>
                </div>
            </div>
            <script>
                const GPS_DATA_KEY = 'gps_tracking_session_data';
                
                function getGpsData() {
                    const data = sessionStorage.getItem(GPS_DATA_KEY);
                    return data ? JSON.parse(data) : [];
                }
                
                function formatTimestamp(isoString) {
                    const date = new Date(isoString);
                    return date.toLocaleString();
                }
                
                function renderLiveTracking() {
                    const data = getGpsData();
                    const tbody = document.getElementById('live-tracking-body');
                    
                    if (data.length === 0) {
                        tbody.innerHTML = `
                            <tr>
                                <td colspan="6">
                                    <div class="empty-state">
                                        <i class="fas fa-satellite-dish"></i>
                                        <h4>No GPS Data Captured Yet</h4>
                                        <p>Capture some vehicle data from the tracking page to see it here.</p>
                                    </div>
                                </td>
                            </tr>
                        `;
                        document.getElementById('raw-session-data').textContent = 'No data';
                        return;
                    }
                    
                    let html = '';
                    data.forEach(entry => {
                        const statusClass = entry.status === 'moving' ? 'badge-moving' : entry.status === 'stopped' ? 'badge-stopped' : 'badge-idle';
                        html += '<tr>' +
                            '<td><strong>' + entry.vehicle_id + '</strong></td>' +
                            '<td>' + entry.license_plate + '</td>' +
                            '<td><code>' + entry.latitude.toFixed(6) + '</code></td>' +
                            '<td><code>' + entry.longitude.toFixed(6) + '</code></td>' +
                            '<td>' + formatTimestamp(entry.timestamp) + '</td>' +
                            '<td><span class="badge ' + statusClass + '">' + entry.status.toUpperCase() + '</span></td>' +
                            '</tr>';
                    });
                    
                    tbody.innerHTML = html;
                    document.getElementById('raw-session-data').textContent = JSON.stringify(data, null, 2);
                }
                
                renderLiveTracking();
                
                document.getElementById('refresh-live-data').addEventListener('click', renderLiveTracking);
                
                document.getElementById('clear-session-data').addEventListener('click', function() {
                    if (confirm('Are you sure you want to clear all session GPS data?')) {
                        sessionStorage.removeItem(GPS_DATA_KEY);
                        sessionStorage.setItem(GPS_DATA_KEY, JSON.stringify([]));
                        renderLiveTracking();
                        alert('Session data cleared');
                    }
                });
            </script>
        </body>
        </html>
        """
        return request.make_response(html_content, headers=[('Content-Type', 'text/html')])
