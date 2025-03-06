document.addEventListener('DOMContentLoaded', () => {
    // Initialize charts
    function initCharts() {
        // Get colors from CSS variables to ensure consistency
        const getStyleVariable = (varName) => {
            return getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
        };
        
        // Set up colors based on current theme
        const solarColor = getStyleVariable('--color-solar');
        const windColor = getStyleVariable('--color-wind');
        const hydrogenColor = getStyleVariable('--color-hydrogen');
        const textColor = getStyleVariable('--color-text-primary');
        const gridColor = getStyleVariable('--color-border');
        const bgColor = 'rgba(0,0,0,0)';
        
        // Time Series Chart - shows dummy data initially
        const timeSeriesData = [{
            x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            y: [4.5, 5.2, 5.7, 6.3, 6.8, 7.1, 7.0, 6.6, 6.1, 5.5, 4.8, 4.3],
            type: 'scatter',
            mode: 'lines+markers',
            line: {
                color: solarColor,
                width: 3,
                shape: 'spline'
            },
            marker: {
                color: solarColor,
                size: 6
            },
            name: 'Monthly Average'
        }];

        const timeSeriesLayout = {
            paper_bgcolor: bgColor,
            plot_bgcolor: bgColor,
            margin: { t: 20, r: 20, b: 40, l: 50 },
            xaxis: {
                title: 'Month',
                titlefont: {
                    size: 12,
                    color: textColor
                },
                tickfont: {
                    color: textColor
                },
                gridcolor: gridColor,
                gridwidth: 1,
                zeroline: false
            },
            yaxis: {
                title: 'kWh/m²',
                titlefont: {
                    size: 12,
                    color: textColor
                },
                tickfont: {
                    color: textColor
                },
                gridcolor: gridColor,
                gridwidth: 1,
                zeroline: false
            },
            font: {
                color: textColor
            },
            showlegend: false,
            autosize: true,
            hovermode: 'closest'
        };

        Plotly.newPlot('timeSeriesChartContainer', timeSeriesData, timeSeriesLayout, {
            responsive: true,
            useResizeHandler: true,
            displayModeBar: false
        });

        // Comparative Chart - shows dummy data initially
        const comparativeData = [{
            x: ['Adrar', 'Biskra', 'Ghardaïa', 'Tamanrasset', 'Ouargla'],
            y: [7.2, 6.1, 5.8, 6.9, 6.5],
            type: 'bar',
            marker: {
                color: solarColor,
                opacity: 0.8
            },
            name: 'Solar Potential (kWh/m²)'
        }];

        const comparativeLayout = {
            paper_bgcolor: bgColor,
            plot_bgcolor: bgColor,
            margin: { t: 20, r: 20, b: 70, l: 50 },
            xaxis: {
                tickangle: -45,
                tickfont: {
                    size: 10,
                    color: textColor
                },
                gridcolor: gridColor,
                gridwidth: 1,
                zeroline: false
            },
            yaxis: {
                title: 'kWh/m²',
                titlefont: {
                    size: 12,
                    color: textColor
                },
                tickfont: {
                    color: textColor
                },
                gridcolor: gridColor,
                gridwidth: 1,
                zeroline: false
            },
            font: {
                color: textColor
            },
            showlegend: false,
            autosize: true,
            hovermode: 'closest',
            bargap: 0.15
        };

        Plotly.newPlot('comparativeChartContainer', comparativeData, comparativeLayout, {
            responsive: true,
            useResizeHandler: true,
            displayModeBar: false
        });
    }

    initCharts();

    // Update charts when theme changes
    document.getElementById('theme-toggle').addEventListener('click', () => {
        setTimeout(initCharts, 300);
    });

    // Handle window resize to ensure charts resize properly
    function handleResize() {
        Plotly.Plots.resize('timeSeriesChartContainer');
        Plotly.Plots.resize('comparativeChartContainer');
    }
    
    // Add resize event listener
    window.addEventListener('resize', handleResize);
    
    // Also handle resize when the dashboard container is scrolled
    const dashboardContainer = document.querySelector('.dashboard-container');
    if (dashboardContainer) {
        dashboardContainer.addEventListener('scroll', function() {
            // Debounce the resize to avoid too many calls
            if (this.scrollTimer) clearTimeout(this.scrollTimer);
            this.scrollTimer = setTimeout(handleResize, 100);
        });
    }

    // Populate wilaya dropdown with data
    const wilayas = [
        'Adrar', 'Chlef', 'Laghouat', 'Oum El Bouaghi', 'Batna', 'Béjaïa', 'Biskra', 'Béchar', 
        'Blida', 'Bouira', 'Tamanrasset', 'Tébessa', 'Tlemcen', 'Tiaret', 'Tizi Ouzou', 
        'Algiers', 'Djelfa', 'Jijel', 'Sétif', 'Saïda', 'Skikda', 'Sidi Bel Abbès', 'Annaba', 
        'Guelma', 'Constantine', 'Médéa', 'Mostaganem', 'M\'Sila', 'Mascara', 'Ouargla', 'Oran', 
        'El Bayadh', 'Illizi', 'Bordj Bou Arréridj', 'Boumerdès', 'El Tarf', 'Tindouf', 
        'Tissemsilt', 'El Oued', 'Khenchela', 'Souk Ahras', 'Tipaza', 'Mila', 'Aïn Defla', 
        'Naâma', 'Aïn Témouchent', 'Ghardaïa', 'Relizane'
    ];
    
    const wilayaFilter = document.getElementById('wilayaFilter');
    wilayas.forEach(wilaya => {
        const option = document.createElement('option');
        option.value = wilaya.toLowerCase().replace(/\s+/g, '_');
        option.text = wilaya;
        wilayaFilter.appendChild(option);
    });

    // Handle wilaya selection from the filter
    wilayaFilter.addEventListener('change', function() {
        const selectedWilaya = this.options[this.selectedIndex].text;
        if (selectedWilaya && this.value !== '') {
            updateDashboardWithWilayaData(selectedWilaya);
        }
    });
    
    // Add click event to the map (will be implemented in map_init.js)
    // This function will be called from map_init.js when a wilaya is clicked
    window.updateDashboardFromMap = function(wilayaName) {
        // Update the wilaya filter dropdown to match the map selection
        const wilayaOption = Array.from(wilayaFilter.options).find(option => 
            option.text.toLowerCase() === wilayaName.toLowerCase()
        );
        
        if (wilayaOption) {
            wilayaFilter.value = wilayaOption.value;
            updateDashboardWithWilayaData(wilayaOption.text);
        }
    };
    
    // Initial resize after a short delay to ensure proper rendering
    setTimeout(handleResize, 300);
    
    // Also handle resize when the page becomes visible (tab switching)
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'visible') {
            setTimeout(handleResize, 300);
        }
    });
});

// Function to update the dashboard with data for the selected wilaya
function updateDashboardWithWilayaData(wilayaName) {
    // Update the wilaya name display
    document.getElementById('selectedWilayaName').textContent = wilayaName;
    
    // In a real implementation, you would fetch data from the API
    // For now, generate some sample data
    const getRandomValue = (min, max) => (Math.random() * (max - min) + min).toFixed(2);
    
    // Get the current energy type
    const energyType = document.getElementById('energyTypeFilter').value;
    
    // Get colors from CSS variables
    const getStyleVariable = (varName) => {
        return getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
    };
    
    // Set color based on energy type
    let color, chartTitle, yAxisTitle, valueRange;
    if (energyType === 'solar') {
        color = getStyleVariable('--color-solar');
        chartTitle = 'Monthly Solar Potential';
        yAxisTitle = 'kWh/m²';
        valueRange = { min: 4.0, max: 7.5 };
    } else if (energyType === 'wind') {
        color = getStyleVariable('--color-wind');
        chartTitle = 'Monthly Wind Speed';
        yAxisTitle = 'm/s';
        valueRange = { min: 3.0, max: 8.0 };
    } else {
        color = getStyleVariable('--color-hydrogen');
        chartTitle = 'Monthly Green Hydrogen Potential';
        yAxisTitle = 'kg/kWh';
        valueRange = { min: 0.05, max: 0.15 };
    }
    
    // Generate values based on energy type
    const solarValue = getRandomValue(4.0, 7.5);
    const windValue = getRandomValue(3.0, 8.0);
    const hydrogenValue = getRandomValue(0.05, 0.15);
    
    // Update the stat cards with values
    document.getElementById('solarPotentialValue').textContent = solarValue;
    document.getElementById('windSpeedValue').textContent = windValue;
    document.getElementById('hydrogenPotentialValue').textContent = hydrogenValue;
    
    // Update time series chart with realistic seasonal patterns
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    let timeSeriesValues;
    
    // Create realistic seasonal patterns based on energy type
    if (energyType === 'solar') {
        // Solar peaks in summer months
        const baseValue = parseFloat(solarValue);
        timeSeriesValues = [
            baseValue * 0.7,  // Jan
            baseValue * 0.8,  // Feb
            baseValue * 0.9,  // Mar
            baseValue * 1.0,  // Apr
            baseValue * 1.1,  // May
            baseValue * 1.2,  // Jun
            baseValue * 1.2,  // Jul
            baseValue * 1.1,  // Aug
            baseValue * 1.0,  // Sep
            baseValue * 0.9,  // Oct
            baseValue * 0.8,  // Nov
            baseValue * 0.7   // Dec
        ];
    } else if (energyType === 'wind') {
        // Wind often stronger in winter/spring
        const baseValue = parseFloat(windValue);
        timeSeriesValues = [
            baseValue * 1.1,  // Jan
            baseValue * 1.2,  // Feb
            baseValue * 1.1,  // Mar
            baseValue * 1.0,  // Apr
            baseValue * 0.9,  // May
            baseValue * 0.8,  // Jun
            baseValue * 0.8,  // Jul
            baseValue * 0.9,  // Aug
            baseValue * 1.0,  // Sep
            baseValue * 1.1,  // Oct
            baseValue * 1.2,  // Nov
            baseValue * 1.1   // Dec
        ];
    } else {
        // Hydrogen potential (depends on both solar and wind)
        const baseValue = parseFloat(hydrogenValue);
        timeSeriesValues = [
            baseValue * 0.9,  // Jan
            baseValue * 1.0,  // Feb
            baseValue * 1.1,  // Mar
            baseValue * 1.1,  // Apr
            baseValue * 1.0,  // May
            baseValue * 1.0,  // Jun
            baseValue * 1.0,  // Jul
            baseValue * 1.0,  // Aug
            baseValue * 1.0,  // Sep
            baseValue * 1.0,  // Oct
            baseValue * 1.0,  // Nov
            baseValue * 0.9   // Dec
        ];
    }
    
    // Add slight randomness to make the chart look more realistic
    timeSeriesValues = timeSeriesValues.map(val => val * (0.95 + Math.random() * 0.1));
    
    // Update time series chart
    Plotly.update('timeSeriesChartContainer', {
        x: [months],
        y: [timeSeriesValues],
        'line.color': [color],
        'marker.color': [color]
    });
    
    // Update the layout with new titles
    Plotly.relayout('timeSeriesChartContainer', {
        'yaxis.title': yAxisTitle,
        'yaxis.range': [
            Math.min(...timeSeriesValues) * 0.9,
            Math.max(...timeSeriesValues) * 1.1
        ]
    });
    
    // Update comparative chart
    // For the comparative chart, we'll show wilayas with similar characteristics
    // These would be fetched from API in a real implementation
    const topWilayas = ['Adrar', 'Béchar', 'Tamanrasset', 'Ouargla', 'Biskra'];
    
    // Generate comparative values with the selected wilaya having a standout value
    let comparativeValues = [];
    const selectedIndex = topWilayas.indexOf(wilayaName);
    
    for (let i = 0; i < topWilayas.length; i++) {
        // If the current wilaya is selected, use our known value
        if (topWilayas[i] === wilayaName) {
            if (energyType === 'solar') {
                comparativeValues.push(parseFloat(solarValue));
            } else if (energyType === 'wind') {
                comparativeValues.push(parseFloat(windValue));
            } else {
                comparativeValues.push(parseFloat(hydrogenValue));
            }
        } else {
            // Otherwise generate a random value
            if (energyType === 'solar') {
                comparativeValues.push(parseFloat(getRandomValue(4.0, 7.0)));
            } else if (energyType === 'wind') {
                comparativeValues.push(parseFloat(getRandomValue(3.0, 7.5)));
            } else {
                comparativeValues.push(parseFloat(getRandomValue(0.06, 0.14)));
            }
        }
    }
    
    // Generate color array where the selected wilaya stands out
    const barColors = Array(topWilayas.length).fill(color);
    
    // If the selected wilaya is in our top list, highlight it
    if (selectedIndex >= 0) {
        // Make the selected wilaya's bar a darker shade
        barColors[selectedIndex] = color; 
        
        // Make other bars more transparent
        for (let i = 0; i < barColors.length; i++) {
            if (i !== selectedIndex) {
                barColors[i] = color + '80'; // Add 50% transparency
            }
        }
    }
    
    // Update comparative chart
    Plotly.update('comparativeChartContainer', {
        x: [topWilayas],
        y: [comparativeValues],
        'marker.color': [barColors]
    });
    
    Plotly.relayout('comparativeChartContainer', {
        'yaxis.title': yAxisTitle,
        'yaxis.range': [
            Math.min(...comparativeValues) * 0.9,
            Math.max(...comparativeValues) * 1.1
        ]
    });
    
    // Resize charts to ensure they fit properly
    setTimeout(() => {
        Plotly.Plots.resize('timeSeriesChartContainer');
        Plotly.Plots.resize('comparativeChartContainer');
    }, 100);
    
    console.log(`Dashboard updated with data for ${wilayaName}, energy type: ${energyType}`);
}