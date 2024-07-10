const { ChartJSNodeCanvas } = require('chartjs-node-canvas');

class ChartGenerator {
    constructor(width = 1200, height = 800) {
        this.width = width;
        this.height = height;
        this.chartJSNodeCanvas = new ChartJSNodeCanvas({
            width, height,
            backgroundColour: 'white'
        });
    }

    /**
     * Generate stock chart with technical indicators
     * @param {Array} stockData - Stock data array
     * @param {Object} indicators - Technical indicators
     * @param {string} symbol - Stock symbol
     * @returns {Buffer} Chart image buffer
     */
    async generateStockChart(stockData, indicators, symbol) {
        const dates = stockData.map(data => 
            data.date.toISOString().split('T')[0]
        );
        const closingPrices = stockData.map(data => data.close);

        const configuration = {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'Closing Price',
                        data: closingPrices,
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        tension: 0.1,
                        fill: true
                    },
                    {
                        label: 'SMA 20',
                        data: this.padArray(indicators.sma20, closingPrices.length),
                        borderColor: 'rgb(255, 99, 132)',
                        borderDash: [5, 5],
                        tension: 0.1,
                        fill: false
                    },
                    {
                        label: 'SMA 50',
                        data: this.padArray(indicators.sma50, closingPrices.length),
                        borderColor: 'rgb(54, 162, 235)',
                        borderDash: [5, 5],
                        tension: 0.1,
                        fill: false
                    },
                    {
                        label: 'Bollinger Upper',
                        data: this.padArray(indicators.bollingerBands.upper, closingPrices.length),
                        borderColor: 'rgb(153, 102, 255)',
                        borderDash: [2, 2],
                        tension: 0.1,
                        fill: false
                    },
                    {
                        label: 'Bollinger Lower',
                        data: this.padArray(indicators.bollingerBands.lower, closingPrices.length),
                        borderColor: 'rgb(153, 102, 255)',
                        borderDash: [2, 2],
                        tension: 0.1,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: `${symbol} Stock Price with Technical Indicators`,
                        font: {
                            size: 18
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Price ($)'
                        }
                    }
                }
            }
        };

        return await this.chartJSNodeCanvas.renderToBuffer(configuration);
    }

    /**
     * Generate RSI chart
     * @param {Array} rsiData - RSI values
     * @param {Array} dates - Date labels
     * @param {string} symbol - Stock symbol
     * @returns {Buffer} RSI chart image buffer
     */
    async generateRSIChart(rsiData, dates, symbol) {
        const configuration = {
            type: 'line',
            data: {
                labels: dates.slice(-rsiData.length),
                datasets: [{
                    label: 'RSI (14)',
                    data: rsiData,
                    borderColor: 'rgb(255, 159, 64)',
                    tension: 0.1,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: `${symbol} Relative Strength Index (RSI)`,
                        font: {
                            size: 16
                        }
                    },
                    annotation: {
                        annotations: {
                            overbought: {
                                type: 'line',
                                yMin: 70,
                                yMax: 70,
                                borderColor: 'red',
                                borderWidth: 2,
                                borderDash: [5, 5]
                            },
                            oversold: {
                                type: 'line',
                                yMin: 30,
                                yMax: 30,
                                borderColor: 'green',
                                borderWidth: 2,
                                borderDash: [5, 5]
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        min: 0,
                        max: 100,
                        title: {
                            display: true,
                            text: 'RSI Value'
                        }
                    }
                }
            }
        };

        return await this.chartJSNodeCanvas.renderToBuffer(configuration);
    }

    /**
     * Pad array with null values to match desired length
     * @param {Array} array - Array to pad
     * @param {number} length - Desired length
     * @returns {Array} Padded array
     */
    padArray(array, length) {
        const padding = Array(length - array.length).fill(null);
        return padding.concat(array);
    }
}

module.exports = ChartGenerator;