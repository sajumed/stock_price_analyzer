/**
 * Stock Data Visualizer - Creates interactive charts using Chart.js
 */

class StockVisualizer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.chart = null;
        this.ctx = this.canvas.getContext('2d');
    }

    /**
     * Create main price chart with technical indicators
     */
    createPriceChart(stockData, indicators = {}) {
        if (this.chart) {
            this.chart.destroy();
        }

        const dates = stockData.map(item => item.date);
        const prices = stockData.map(item => item.close);

        const datasets = [
            {
                label: 'Close Price',
                data: prices,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                borderWidth: 2,
                fill: false,
                yAxisID: 'y'
            }
        ];

        // Add SMA if available
        if (indicators.sma) {
            datasets.push({
                label: 'SMA (20)',
                data: this.alignDataWithDates(dates, indicators.sma),
                borderColor: 'rgb(255, 99, 132)',
                borderWidth: 1,
                borderDash: [5, 5],
                fill: false,
                yAxisID: 'y'
            });
        }

        // Add EMA if available
        if (indicators.ema) {
            datasets.push({
                label: 'EMA (12)',
                data: this.alignDataWithDates(dates, indicators.ema),
                borderColor: 'rgb(153, 102, 255)',
                borderWidth: 1,
                fill: false,
                yAxisID: 'y'
            });
        }

        // Add Bollinger Bands if available
        if (indicators.bollinger) {
            datasets.push(
                {
                    label: 'Bollinger Upper',
                    data: this.alignDataWithDates(dates, indicators.bollinger, 'upper'),
                    borderColor: 'rgb(255, 159, 64)',
                    borderWidth: 1,
                    borderDash: [2, 2],
                    fill: false,
                    yAxisID: 'y'
                },
                {
                    label: 'Bollinger Lower',
                    data: this.alignDataWithDates(dates, indicators.bollinger, 'lower'),
                    borderColor: 'rgb(255, 159, 64)',
                    borderWidth: 1,
                    borderDash: [2, 2],
                    fill: false,
                    yAxisID: 'y'
                }
            );
        }

        this.chart = new Chart(this.ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: datasets
            },
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day'
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left'
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Stock Price with Technical Indicators'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: $${context.parsed.y.toFixed(2)}`;
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Create RSI chart
     */
    createRSIChart(rsiData) {
        const rsiCanvas = document.getElementById('rsiChart');
        if (!rsiCanvas) return;

        const dates = rsiData.map(item => item.date);
        const rsiValues = rsiData.map(item => item.value);

        new Chart(rsiCanvas.getContext('2d'), {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'RSI (14)',
                    data: rsiValues,
                    borderColor: 'rgb(54, 162, 235)',
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    annotation: {
                        annotations: {
                            overbought: {
                                type: 'line',
                                yMin: 70,
                                yMax: 70,
                                borderColor: 'red',
                                borderWidth: 1,
                                borderDash: [5, 5]
                            },
                            oversold: {
                                type: 'line',
                                yMin: 30,
                                yMax: 30,
                                borderColor: 'green',
                                borderWidth: 1,
                                borderDash: [5, 5]
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Create MACD chart
     */
    createMACDChart(macdData) {
        const macdCanvas = document.getElementById('macdChart');
        if (!macdCanvas) return;

        const dates = macdData.macdLine.map(item => item.date);
        const macdLine = macdData.macdLine.map(item => item.value);
        const signalLine = macdData.signalLine.map(item => item.value);
        const histogram = macdData.histogram.map(item => item.value);

        new Chart(macdCanvas.getContext('2d'), {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'MACD Histogram',
                        data: histogram,
                        type: 'bar',
                        backgroundColor: histogram.map(val => 
                            val >= 0 ? 'rgba(75, 192, 192, 0.8)' : 'rgba(255, 99, 132, 0.8)'
                        ),
                        yAxisID: 'y'
                    },
                    {
                        label: 'MACD Line',
                        data: macdLine,
                        type: 'line',
                        borderColor: 'blue',
                        borderWidth: 2,
                        fill: false,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Signal Line',
                        data: signalLine,
                        type: 'line',
                        borderColor: 'red',
                        borderWidth: 2,
                        fill: false,
                        yAxisID: 'y'
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    /**
     * Helper function to align indicator data with price dates
     */
    alignDataWithDates(priceDates, indicatorData, field = 'value') {
        const alignedData = new Array(priceDates.length).fill(null);
        
        indicatorData.forEach(indicator => {
            const index = priceDates.indexOf(indicator.date);
            if (index !== -1) {
                alignedData[index] = indicator[field];
            }
        });
        
        return alignedData;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StockVisualizer;
}