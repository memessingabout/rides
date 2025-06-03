<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Route Tracker</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        #map { height: 400px; width: 100%; }
        body { font-family: Arial, sans-serif; }
        .controls { margin: 10px 0; }
        .trip-list { margin-top: 10px; max-height: 200px; overflow-y: auto; }
        .trip-item { cursor: pointer; padding: 5px; border-bottom: 1px solid #ccc; }
        .trip-item:hover { background: #f0f0f0; }
    </style>
</head>
<body>
    <h2>Route Tracker</h2>
    <div class="controls">
        <button onclick="startTracking()">Start</button>
        <button onclick="pauseTracking()">Pause</button>
        <button onclick="stopTracking()">Stop</button>
        <label>Trip Type: 
            <select id="tripType">
                <option value="online">Online (Ride-Hailing)</option>
                <option value="offline">Offline</option>
            </select>
        </label>
        <label>Gross Fare (if applicable): <input type="number" id="grossFare" placeholder="e.g., 450"></label>
    </div>
    <p id="status">Status: Ready</p>
    <div id="map"></div>
    <div class="trip-list" id="tripList"></div>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        // Initialize map
        const map = L.map('map').setView([0, 0], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        let tracking = false;
        let paused = false;
        let watchId;
        let routeCoordinates = [];
        let tripPolyline;
        let deadheadCoordinates = [];
        let deadheadPolyline;
        let trips = [];
        let startTime;
        let currentPosition;
        const fuelEfficiency = 25; // km per liter, adjustable

        // Haversine formula for distance (in meters)
        function haversineDistance(coord1, coord2) {
            const R = 6371e3; // Earth radius in meters
            const lat1 = coord1[0] * Math.PI / 180;
            const lat2 = coord2[0] * Math.PI / 180;
            const deltaLat = (coord2[0] - coord1[0]) * Math.PI / 180;
            const deltaLon = (coord2[1] - coord1[1]) * Math.PI / 180;
            const a = Math.sin(deltaLat / 2) * Math.sin(deltaLat / 2) +
                      Math.cos(lat1) * Math.cos(lat2) *
                      Math.sin(deltaLon / 2) * Math.sin(deltaLon / 2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            return R * c; // Distance in meters
        }

        // Start tracking
        function startTracking() {
            if (!tracking) {
                tracking = true;
                paused = false;
                routeCoordinates = [];
                deadheadCoordinates = [];
                startTime = new Date();
                document.getElementById('status').innerText = 'Status: Tracking...';
                if (navigator.geolocation) {
                    watchId = navigator.geolocation.watchPosition(
                        position => {
                            if (paused) return;
                            const { latitude, longitude } = position.coords;
                            currentPosition = [latitude, longitude];
                            const isDeadhead = document.getElementById('tripType').value === 'online' && routeCoordinates.length < 2;
                            if (isDeadhead) {
                                deadheadCoordinates.push(currentPosition);
                                if (deadheadPolyline) {
                                    deadheadPolyline.setLatLngs(deadheadCoordinates);
                                } else {
                                    deadheadPolyline = L.polyline(deadheadCoordinates, { color: 'red' }).addTo(map);
                                }
                            } else {
                                routeCoordinates.push(currentPosition);
                                if (tripPolyline) {
                                    tripPolyline.setLatLngs(routeCoordinates);
                                } else {
                                    tripPolyline = L.polyline(routeCoordinates, { color: 'blue' }).addTo(map);
                                }
                            }
                            map.setView(currentPosition, 13);
                            L.marker(currentPosition).addTo(map)
                                .bindPopup(`Lat: ${latitude}, Lon: ${longitude}`).openPopup();
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

        // Pause tracking
        function pauseTracking() {
            if (tracking && !paused) {
                paused = true;
                document.getElementById('status').innerText = 'Status: Paused';
            } else if (tracking && paused) {
                paused = false;
                document.getElementById('status').innerText = 'Status: Tracking...';
            }
        }

        // Stop tracking and save trip
        function stopTracking() {
            if (tracking) {
                tracking = false;
                paused = false;
                navigator.geolocation.clearWatch(watchId);
                document.getElementById('status').innerText = 'Status: Stopped';
                
                // Calculate trip details
                const endTime = new Date();
                const durationSec = (endTime - startTime) / 1000; // seconds
                let tripDistance = 0;
                for (let i = 1; i < routeCoordinates.length; i++) {
                    tripDistance += haversineDistance(routeCoordinates[i - 1], routeCoordinates[i]);
                }
                let deadheadDistance = 0;
                for (let i = 1; i < deadheadCoordinates.length; i++) {
                    deadheadDistance += haversineDistance(deadheadCoordinates[i - 1], deadheadCoordinates[i]);
                }
                const totalDistanceKm = (tripDistance + deadheadDistance) / 1000; // km
                const fuelUsed = totalDistanceKm / fuelEfficiency; // liters
                const grossFare = parseFloat(document.getElementById('grossFare').value) || 0;
                const tripType = document.getElementById('tripType').value;
                
                // Fare breakdown (example)
                const commissionRate = tripType === 'online' ? 0.21 : 0; // 21% for online
                const commission = grossFare * commissionRate;
                const taxes = grossFare * 0.05; // 5% tax, adjustable
                const netEarnings = grossFare - commission - taxes;

                // Save trip
                const trip = {
                    id: trips.length + 1,
                    type: tripType,
                    date: startTime.toLocaleString(),
                    duration: durationSec.toFixed(1) + ' sec',
                    tripDistance: tripDistance.toFixed(2) + ' m',
                    deadheadDistance: deadheadDistance.toFixed(2) + ' m',
                    totalDistance: (totalDistanceKm * 1000).toFixed(2) + ' m',
                    fuelUsed: fuelUsed.toFixed(2) + ' L',
                    fare: {
                        gross: grossFare.toFixed(2),
                        commission: commission.toFixed(2),
                        taxes: taxes.toFixed(2),
                        net: netEarnings.toFixed(2)
                    },
                    coordinates: [...deadheadCoordinates, ...routeCoordinates]
                };
                trips.push(trip);
                updateTripList();
            }
        }

        // Update trip list
        function updateTripList() {
            const tripList = document.getElementById('tripList');
            tripList.innerHTML = '';
            trips.forEach(trip => {
                const div = document.createElement('div');
                div.className = 'trip-item';
                div.innerHTML = `Trip ${trip.id} (${trip.type}) - ${trip.date} - ${trip.duration} - ${trip.totalDistance}`;
                div.onclick = () => showTripDetails(trip);
                tripList.appendChild(div);
            });
        }

        // Show trip details and highlight route
        function showTripDetails(trip) {
            if (tripPolyline) map.removeLayer(tripPolyline);
            if (deadheadPolyline) map.removeLayer(deadheadPolyline);
            deadheadPolyline = L.polyline(trip.coordinates.slice(0, trip.coordinates.length - routeCoordinates.length), { color: 'red' }).addTo(map);
            tripPolyline = L.polyline(trip.coordinates.slice(trip.coordinates.length - routeCoordinates.length), { color: 'blue' }).addTo(map);
            map.fitBounds(trip.coordinates);
            alert(
                `Trip ${trip.id} (${trip.type})\n` +
                `Date: ${trip.date}\n` +
                `Duration: ${trip.duration}\n` +
                `Trip Distance: ${trip.tripDistance}\n` +
                `Deadhead Distance: ${trip.deadheadDistance}\n` +
                `Total Distance: ${trip.totalDistance}\n` +
                `Fuel Used: ${trip.fuelUsed}\n` +
                `Fare Breakdown:\n  Gross: ${trip.fare.gross}\n  Commission: ${trip.fare.commission}\n  Taxes: ${trip.fare.taxes}\n  Net: ${trip.fare.net}`
            );
        }
    </script>
</body>
</html>