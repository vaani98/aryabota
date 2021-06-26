export const getChartJSData = () => {
    return {
        labels: [0, 1, 2, 3, 4, 5],
        datasets: [
            {
                fill: false,
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgba(255, 99, 132, 0.2)',
                pointRadius: 5,
            },
        ],
    };
}

export const getChartJSOptions = () => {
    return {
        animation: {
            duration: 0 // general animation time
        },
        scales: {
            y: {
            max: 10,
            min: 0,
            ticks: {
                stepSize: 1,
            }
            },
        },
    }
}