// Initialize Leaflet map
var map = L.map('map').setView([28.0339, 1.6596], 6); // Algeria coordinates and zoom level

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Example: Add a marker (replace with dynamic data loading)
L.marker([28.0339, 1.6596]).addTo(map)
    .bindPopup('Algeria')
    .openPopup();

// Hide loading indicator after map is initialized
document.getElementById('mapLoadingIndicator').style.display = 'none';