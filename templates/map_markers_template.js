document.addEventListener('DOMContentLoaded', () => {
    const map = {{ map_var }};
    const cluster = {{ cluster_var }};
    const markerDataByMonth = {{ markers_by_month | tojson }};
    const tooltip = new L.Tooltip().setContent('Click to select');
    let markersByMonth = [];
    Object.entries(markerDataByMonth).forEach(([month, markers], index) => {
        markersByMonth[index] = [];
        let popup = new L.Popup().setContent(markers[0].popup);
        markers.forEach(data => {
            const marker = L.marker(data.location);
            if (data.hasOwnProperty("popup")) {
                popup = new L.Popup().setContent(data.popup);
            }
            marker.bindPopup(popup).bindTooltip(tooltip);
            if (index === 0) {
                marker.addTo(cluster);
            }
            markersByMonth[index].push(marker);
        });
    });

    let currentIndex = 0;

    map.timeDimension.on('timeload', function(e) {
        let newIndex = e.time - 1;
        if (newIndex === currentIndex) return;
        if (currentIndex === markersByMonth.length) {
            markersByMonth.forEach((monthMarkers, monthIndex) => {
                if (monthIndex !== newIndex) {
                    monthMarkers.forEach(marker => cluster.removeLayer(marker));
                }
            });
        } else if (newIndex !== markersByMonth.length) {
            markersByMonth[currentIndex].forEach(marker => cluster.removeLayer(marker));
        }

        if (newIndex === markersByMonth.length) {
            markersByMonth.forEach((monthMarkers, monthIndex) => {
                if (monthIndex !== currentIndex) {
                    monthMarkers.forEach(marker => cluster.addLayer(marker));
                }
            });
        } else if (currentIndex !== markersByMonth.length) {
            markersByMonth[newIndex].forEach(marker => cluster.addLayer(marker));
        }

        currentIndex = newIndex;
    });
});