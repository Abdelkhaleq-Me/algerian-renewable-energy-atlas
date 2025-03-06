document.addEventListener('DOMContentLoaded', () => {
    // Initialize charts
    function initCharts() {
        // Time Series Chart
        const timeSeriesData = [{
            x: ['2020', '2021', '2022', '2023'],
            y: [0, 0, 0, 0],
            type: 'scatter',
            name: 'Solar Irradiance'
        }];

        Plotly.newPlot('timeSeriesChartContainer', timeSeriesData, {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {
                color: document.documentElement.getAttribute('data-theme') === 'dark' ? '#e5e7eb' : '#374151'
            }
        });

        // Comparative Chart
        const comparativeData = [{
            x: ['Solar', 'Wind', 'Green Hydrogen'],
            y: [0, 0, 0],
            type: 'bar',
            marker: {
                color: ['var(--color-primary)', 'var(--color-secondary)', 'var(--color-tertiary)']
            }
        }];

        Plotly.newPlot('comparativeChartContainer', comparativeData, {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {
                color: document.documentElement.getAttribute('data-theme') === 'dark' ? '#e5e7eb' : '#374151'
            }
        });
    }

    initCharts();

    // Update charts when theme changes
    document.getElementById('theme-toggle').addEventListener('click', () => {
        setTimeout(initCharts, 100);
    });

    // Populate region selector with data
    const regions = ['Adrar', 'Chlef', 'Laghouat', 'Oum El Bouaghi', 'Batna', 'Béjaïa', 'Biskra', 'Béchar', 'Blida', 'Bouira', 'Tamanrasset', 'Tébessa', 'Tlemcen', 'Tiaret', 'Tizi Ouzou', 'Algiers', 'Djelfa', 'Jijel', 'Sétif', 'Saïda', 'Skikda', 'Sidi Bel Abbès', 'Annaba', 'Guelma', 'Constantine', 'Médéa', 'Mostaganem', 'M\'Sila', 'Mascara', 'Ouargla', 'Oran', 'El Bayadh', 'Illizi', 'Bordj Bou Arréridj', 'Boumerdès', 'El Tarf', 'Tindouf', 'Tissemsilt', 'El Oued', 'Khenchela', 'Souk Ahras', 'Tipaza', 'Mila', 'Aïn Defla', 'Naâma', 'Aïn Témouchent', 'Ghardaïa', 'Relizane'];
    
    const regionSelector = document.getElementById('regionSelector');
    regions.forEach(region => {
        const option = document.createElement('option');
        option.value = region;
        option.text = region;
        regionSelector.appendChild(option);
    });

    // Handle region selection
    regionSelector.addEventListener('change', function() {
        const selectedRegion = this.value;
        if (selectedRegion) {
            // Update dashboard with region data (implement actual data loading)
            updateDashboardData(selectedRegion);
        }
    });
});

function updateDashboardData(region) {
    // Implement dashboard data update logic
    console.log(`Updating dashboard data for region: ${region}`);
    // Update stats cards and charts with actual data
}