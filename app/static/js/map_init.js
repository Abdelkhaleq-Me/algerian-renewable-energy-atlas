// Function to toggle control sections
function toggleSection(sectionId) {
    const content = document.getElementById(sectionId + 'Content');
    const arrow = content.parentElement.querySelector('.control-minimize');
    
    if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        arrow.style.transform = 'rotate(0deg)';
    } else {
        content.classList.add('hidden');
        arrow.style.transform = 'rotate(-90deg)';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Initialize map
    const map = L.map('map', {
        zoomControl: false,
        attributionControl: false,
        maxBounds: [[15, -15], [40, 20]], // Limit panning to around Algeria
        minZoom: 4
    }).setView([28.0339, 1.6596], 5);
    
    // Add zoom control to bottom right
    L.control.zoom({
        position: 'bottomright'
    }).addTo(map);
    
    // Add attribution control to bottom left
    L.control.attribution({
        position: 'bottomleft',
        prefix: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Add basemap layers
    const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    });
    
    const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    });
    
    // Default to OSM
    osmLayer.addTo(map);
    
    // Add basemap control
    const baseMaps = {
        "Streets": osmLayer,
        "Satellite": satelliteLayer
    };
    
    L.control.layers(baseMaps, null, {
        position: 'bottomright',
        collapsed: false
    }).addTo(map);
    
    // Variable to store the GeoJSON layer for wilayas
    let wilayasLayer = null;
    
    // Variable to track the currently selected wilaya
    let selectedWilaya = null;
    
    // Function to load the wilaya boundaries
    function loadWilayaBoundaries() {
        // Show loading indicator
        document.getElementById('mapLoadingIndicator').classList.remove('hidden');
        
        // In a real implementation, fetch the GeoJSON from an API
        // For now, we'll simulate a fetch using a setTimeout
        setTimeout(() => {
            // This would be replaced with actual fetch in production
            // fetch('/api/boundaries/wilayas')
            //    .then(response => response.json())
            //    .then(data => { ... })
            
            // Placeholder: Create a simplified rectangle for Algeria
            const algeriaBounds = [
                [[19, -8], [19, 12], [38, 12], [38, -8], [19, -8]] // Simplified polygon for Algeria
            ];
            
            // Create a GeoJSON feature for Algeria
            const algeriaGeoJSON = {
                type: "FeatureCollection",
                features: [{
                    type: "Feature",
                    properties: {
                        name: "Algeria"
                    },
                    geometry: {
                        type: "Polygon",
                        coordinates: algeriaBounds
                    }
                }]
            };
            
            // Add the GeoJSON layer to the map
            wilayasLayer = L.geoJSON(algeriaGeoJSON, {
                style: function(feature) {
                    return {
                        fillColor: 'transparent',
                        weight: 2,
                        opacity: 1,
                        color: '#666',
                        dashArray: '3',
                        fillOpacity: 0.1
                    };
                },
                onEachFeature: function(feature, layer) {
                    // Add a popup with the wilaya name
                    layer.bindPopup(feature.properties.name);
                    
                    // Add click event to select the wilaya
                    layer.on('click', function(e) {
                        // Reset style of previously selected wilaya
                        if (selectedWilaya) {
                            wilayasLayer.resetStyle(selectedWilaya);
                        }
                        
                        // Set the new selected wilaya
                        selectedWilaya = this;
                        
                        // Highlight the selected wilaya
                        this.setStyle({
                            weight: 3,
                            color: '#0066cc',
                            dashArray: '',
                            fillOpacity: 0.2,
                            fillColor: '#0066cc'
                        });
                        
                        // Bring to front
                        this.bringToFront();
                        
                        // Update the dashboard with the selected wilaya
                        if (window.updateDashboardFromMap) {
                            window.updateDashboardFromMap(feature.properties.name);
                        }
                    });
                    
                    // Add hover effect
                    layer.on('mouseover', function(e) {
                        if (this !== selectedWilaya) {
                            this.setStyle({
                                weight: 3,
                                color: '#0066cc',
                                dashArray: '3',
                                fillOpacity: 0.1,
                                fillColor: '#0066cc'
                            });
                        }
                        
                        this.openPopup();
                    });
                    
                    layer.on('mouseout', function(e) {
                        if (this !== selectedWilaya) {
                            wilayasLayer.resetStyle(this);
                        }
                        
                        this.closePopup();
                    });
                }
            }).addTo(map);
            
            // Hide loading indicator
            document.getElementById('mapLoadingIndicator').classList.add('hidden');
        }, 1000);
    }
    
    // Load the wilaya boundaries when the map is ready
    loadWilayaBoundaries();
    
    // Update wilaya selection when the wilaya filter changes
    document.getElementById('wilayaFilter').addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const wilayaName = selectedOption.text;
        
        if (wilayasLayer && wilayaName && this.value !== '') {
            // Find the wilaya feature in the GeoJSON layer
            wilayasLayer.eachLayer(function(layer) {
                if (layer.feature.properties.name === wilayaName) {
                    // Simulate a click on the layer
                    layer.fire('click');
                    
                    // Pan to the wilaya
                    map.fitBounds(layer.getBounds());
                }
            });
        }
    });
    
    // Handle window resize to ensure map fills available space
    function handleResize() {
        // Force map to recalculate its size
        map.invalidateSize({
            animate: false,
            pan: false
        });
    }
    
    // Add resize event listener
    window.addEventListener('resize', handleResize);
    
    // Initial size calculation after a short delay to ensure DOM is fully loaded
    setTimeout(handleResize, 100);
    
    // Also handle resize when the page becomes visible (tab switching)
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'visible') {
            setTimeout(handleResize, 100);
        }
    });
    
    // Expose map object globally for other scripts to use
    window.atlasMap = map;
});