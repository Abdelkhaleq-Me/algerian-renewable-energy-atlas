document.addEventListener('DOMContentLoaded', () => {
    const map = window.atlasMap;  // Get map instance from map_init.js
    
    // Create layer groups
    const solarLayer = L.layerGroup();
    const windLayer = L.layerGroup();
    const greenHydrogenLayer = L.layerGroup();

    document.getElementById('solarLayerToggle').addEventListener('change', function() {
        if (this.checked) {
            solarLayer.addTo(map);
            // Add solar data to the layer (implement actual data loading)
        } else {
            solarLayer.remove();
        }
    });

    document.getElementById('windLayerToggle').addEventListener('change', function() {
        if (this.checked) {
            windLayer.addTo(map);
            // Add wind data to the layer (implement actual data loading)
        } else {
            windLayer.remove();
        }
    });

    document.getElementById('greenHydrogenLayerToggle').addEventListener('change', function() {
        if (this.checked) {
            greenHydrogenLayer.addTo(map);
            // Add green hydrogen data to the layer (implement actual data loading)
        } else {
            greenHydrogenLayer.remove();
        }
    });
});