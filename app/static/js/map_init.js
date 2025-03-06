// Function to toggle control sections
function toggleSection(sectionId) {
    const content = document.getElementById(sectionId + 'Content');
    const arrow = content.parentElement.querySelector('.control-minimize');
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        arrow.classList.remove('minimized');
    } else {
        content.style.display = 'none';
        arrow.classList.add('minimized');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Initialize map
    const map = L.map('map').setView([28.0339, 1.6596], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Hide loading indicator
    document.getElementById('mapLoadingIndicator').style.display = 'none';

    // Make floating controls draggable
    const floatingControls = document.querySelector('.floating-controls');
    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;

    floatingControls.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', dragEnd);

    function dragStart(e) {
        if (e.target.closest('.control-content') || e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {
            return;
        }
        
        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;

        if (e.target === floatingControls || e.target.closest('.control-header')) {
            isDragging = true;
        }
    }

    function drag(e) {
        if (isDragging) {
            e.preventDefault();
            
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;

            xOffset = currentX;
            yOffset = currentY;

            setTranslate(currentX, currentY, floatingControls);
        }
    }

    function dragEnd(e) {
        initialX = currentX;
        initialY = currentY;
        isDragging = false;
    }

    function setTranslate(xPos, yPos, el) {
        el.style.transform = `translate3d(${xPos}px, ${yPos}px, 0)`;
    }

    // Expose map object globally for other scripts to use
    window.atlasMap = map;
});