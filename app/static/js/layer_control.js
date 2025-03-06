document.addEventListener('DOMContentLoaded', () => {
    const map = window.atlasMap;  // Get map instance from map_init.js
    
    // Create layer groups for each energy type
    const layers = {
        solar: {
            ghi: L.layerGroup(),
            dni: L.layerGroup(),
            dhi: L.layerGroup()
        },
        wind: {
            wind10: L.layerGroup(),
            wind50: L.layerGroup()
        },
        green_hydrogen: {
            hydrogen_potential: L.layerGroup()
        }
    };
    
    // Active layers tracking
    let activeEnergyType = 'solar';
    let activeLayers = {
        solar: 'ghi',
        wind: 'wind10',
        green_hydrogen: 'hydrogen_potential'
    };

    // Function to update map layers based on energy type and layer selection
    window.updateMapLayers = function(energyType, specificLayer = null) {
        // Show loading indicator
        document.getElementById('mapLoadingIndicator').classList.remove('hidden');
        
        // First, remove all existing layers
        Object.keys(layers).forEach(type => {
            Object.keys(layers[type]).forEach(layer => {
                map.removeLayer(layers[type][layer]);
            });
        });
        
        // Update active energy type
        activeEnergyType = energyType;
        
        // If a specific layer is provided, update the active layer for this energy type
        if (specificLayer) {
            activeLayers[activeEnergyType] = specificLayer;
        }
        
        // Add the currently selected layer
        const layerToShow = layers[activeEnergyType][activeLayers[activeEnergyType]];
        loadLayerData(activeEnergyType, activeLayers[activeEnergyType], layerToShow);
        
        // Update dashboard UI as well if type changes
        if (window.updateDashboardWithWilayaData && document.getElementById('selectedWilayaName')) {
            const wilayaName = document.getElementById('selectedWilayaName').textContent;
            if (wilayaName && wilayaName !== '{{ _('Select a wilaya on the map') }}') {
                setTimeout(() => window.updateDashboardWithWilayaData(wilayaName), 500);
            }
        }
        
        // Hide loading indicator after a short delay (simulating data loading)
        setTimeout(() => {
            document.getElementById('mapLoadingIndicator').classList.add('hidden');
        }, 1000);
    };
    
    // Function to load the actual data for a layer
    function loadLayerData(energyType, layerType, layerGroup) {
        // Clear the layer first
        layerGroup.clearLayers();
        
        // Add layer to map
        layerGroup.addTo(map);
        
        // Example: Load GeoJSON data based on energy and layer type
        // In a real implementation, this would make API calls to fetch the data
        console.log(`Loading ${layerType} data for ${energyType}`);
        
        // This is a placeholder - in a real implementation you would fetch and add actual data
        // Example of how this might look:
        /*
        fetch(`/api/data/${energyType}/${layerType}`)
            .then(response => response.json())
            .then(data => {
                L.geoJSON(data, {
                    style: function(feature) {
                        return {
                            fillColor: getColor(feature.properties.value),
                            weight: 1,
                            opacity: 1,
                            color: 'white',
                            fillOpacity: 0.7
                        };
                    }
                }).addTo(layerGroup);
            })
            .catch(error => console.error('Error loading data:', error))
            .finally(() => {
                document.getElementById('mapLoadingIndicator').classList.add('hidden');
            });
        */
        
        // For now, just add a colored rectangle for demonstration
        // Get colors from CSS variables
        const getComputedStyleVariable = (varName) => {
            return getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
        };
        
        // Use the appropriate colors based on energy type
        const colors = {
            // Solar colors
            ghi: getComputedStyleVariable('--color-solar'),
            dni: getComputedStyleVariable('--color-solar-dark'),
            dhi: getComputedStyleVariable('--color-solar-light'),
            
            // Wind colors
            wind10: getComputedStyleVariable('--color-wind'),
            wind50: getComputedStyleVariable('--color-wind-dark'),
            
            // Hydrogen colors
            hydrogen_potential: getComputedStyleVariable('--color-hydrogen')
        };
        
        // Create a rectangle covering Algeria's approximate bounds
        const bounds = [[18, -8], [38, 12]]; // Approximate bounds for Algeria
        L.rectangle(bounds, {
            color: colors[layerType] || '#888',
            weight: 1,
            fillColor: colors[layerType] || '#888',
            fillOpacity: 0.5
        }).addTo(layerGroup);
        
        // Add a legend based on the layer type
        addLegend(energyType, layerType);
    }
    
    // Function to add a legend to the map
    function addLegend(energyType, layerType) {
        // Remove existing legend if any
        if (map.legend) {
            map.removeControl(map.legend);
        }
        
        // Create new legend
        const legend = L.control({ position: 'bottomleft' });
        
        legend.onAdd = function(map) {
            const div = L.DomUtil.create('div', 'info legend bg-background-primary dark:bg-background-secondary p-3 rounded-lg shadow-md');
            
            // Set legend title based on energy type
            let title, grades, labels;
            
            if (energyType === 'solar') {
                title = 'Solar Irradiance';
                grades = [3, 4, 5, 6, 7];
                labels = ['< 3', '3-4', '4-5', '5-6', '6-7', '> 7'];
                unit = 'kWh/m²';
            } else if (energyType === 'wind') {
                title = 'Wind Speed';
                grades = [2, 4, 6, 8, 10];
                labels = ['< 2', '2-4', '4-6', '6-8', '8-10', '> 10'];
                unit = 'm/s';
            } else {
                title = 'Green Hydrogen Potential';
                grades = [0.05, 0.07, 0.09, 0.11, 0.13];
                labels = ['< 0.05', '0.05-0.07', '0.07-0.09', '0.09-0.11', '0.11-0.13', '> 0.13'];
                unit = 'kg/kWh';
            }
            
            div.innerHTML = `<div class="font-semibold mb-2">${title} (${unit})</div>`;
            
            // Generate color gradient based on energy type
            let baseColor;
            if (energyType === 'solar') {
                baseColor = getComputedStyle(document.documentElement).getPropertyValue('--color-solar').trim();
            } else if (energyType === 'wind') {
                baseColor = getComputedStyle(document.documentElement).getPropertyValue('--color-wind').trim();
            } else {
                baseColor = getComputedStyle(document.documentElement).getPropertyValue('--color-hydrogen').trim();
            }
            
            // Create color scale
            for (let i = 0; i < labels.length; i++) {
                const opacity = 0.2 + (i * 0.15);
                div.innerHTML += `
                <div class="flex items-center mb-1">
                    <i style="background: ${baseColor}; opacity: ${opacity};" class="w-6 h-4 mr-2"></i>
                    <span>${labels[i]}</span>
                </div>`;
            }
            
            return div;
        };
        
        // Add legend to map
        legend.addTo(map);
        map.legend = legend;
    }
    
    // Attach event listeners to radio buttons for solar layers
    document.querySelectorAll('input[name="solarLayer"]').forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                updateMapLayers('solar', this.value);
            }
        });
    });
    
    // Attach event listeners to radio buttons for wind layers
    document.querySelectorAll('input[name="windLayer"]').forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                updateMapLayers('wind', this.value);
            }
        });
    });
    
    // Attach event listeners to radio buttons for hydrogen layers
    document.querySelectorAll('input[name="hydrogenLayer"]').forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                updateMapLayers('green_hydrogen', this.value);
            }
        });
    });
    
    // Initialize the map with the default layer (solar GHI)
    updateMapLayers('solar', 'ghi');
});