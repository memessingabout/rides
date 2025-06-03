<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Route Tracker</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        #map {
            height: 500px;
            width: 100%;
        }
        body {
            font-family: Arial, sans-serif;
        }
    </style>
</head>
<body>
    <h2>Route Tracker</h2>
    <div id="map"></div>
    <button onclick="startTracking()">Start Tracking</button>
    <button onclick="stopTracking()">Stop Tracking</button>
    <p id="status">Status: Ready</p>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        // Initialize the map
        const map = L.map('map').setView([0, 0], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        let tracking = false;
        let routeCoordinates = [];
        let polyline;
        let watchId;

        // Start tracking location
        function startTracking() {
            if (!tracking) {
                if (navigator.geolocation) {
                    tracking = true;
                    document.getElementById('status').innerText = 'Status: Tracking...';
                    watchId = navigator.geolocation.watchPosition(
                        position => {
                            const { latitude, longitude } = position.coords;
                            const coords = [latitude, longitude];
                            routeCoordinates.push(coords);
                            
                            // Update map view to current position
                            map.setView(coords, 13);
                            
                            // Add a marker for the current position
                            L.marker(coords).addTo(map)
                                .bindPopup(`Lat: ${latitude}, Lon: ${longitude}`)
                                .openPopup();
                            
                            // Draw or update the route
                            if (polyline) {
                                polyline.setLatLngs(routeCoordinates);
                            } else {
                                polyline = L.polyline(routeCoordinates, { color: 'blue' }).addTo(map);
                            }
                        },
                        error => {
                            document.getElementById('status').innerText = 'Status: Error - ' + error.message;
                        },
                        { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
                    );
                } else {
                    document.getElementById('status').innerText = 'Status: Geolocation not supported';
                }
            }
        }

        // Stop tracking location
        function stopTracking() {
            if (tracking) {
                navigator.geolocation.clearWatch(watchId);
                tracking = false;
                document.getElementById('status').innerText = 'Status: Stopped';
            }
        }
    </script>
</body>
</html>