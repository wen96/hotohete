'use strict';

indexPage();

function indexPage() {
    var backgroundColors = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
    ];
    var borderColors = [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
    ];
    var mapLabels = Object.keys(GLOBAL_MAP_STATS);
    var mapsData = [];
    var mapsColors = [];
    var mapsBorders = [];
    for (var i = 0; i < mapLabels.length; i++) {
        var mapData = GLOBAL_MAP_STATS[mapLabels[i]];
        mapsData.push(mapData.played);
        var colorIndex = i % backgroundColors.length;
        mapsColors.push(backgroundColors[colorIndex]);
        mapsBorders.push(borderColors[colorIndex]);
    }

    var topMapsChart = new Chart(document.getElementById("topMapsChart").getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: mapLabels,
            datasets: [{
                data: mapsData,
                backgroundColor: mapsColors,
                borderColor: mapsBorders,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            legend: {
                display: false
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
    var topWeaponsChart = new Chart(document.getElementById("topWeaponsChart").getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ["M4", "USP", "Glock", "Negev", "AK-47", "Deagle"],
            datasets: [{
                label: '# of Votes',
                data: [33, 12, 33, 1, 56, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            legend: {
                display: false
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
}