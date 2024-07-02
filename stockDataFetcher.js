const axios = require('axios');

class StockDataFetcher {
    constructor() {
        this.baseURL = 'https://www.alphavantage.co/query';
        // You need to get a free API key from https://www.alphavantage.co/support/#api-key
        this.apiKey = 'YOUR_API_KEY_HERE'; // Replace with your actual API key
    }

    /**
     * Fetch stock data from Alpha Vantage API
     * @param {string} symbol - Stock symbol (e.g., 'AAPL', 'MSFT')
     * @param {string} interval - Time interval ('1min', '5min', '15min', '30min', '60min', 'daily')
     * @param {string} outputSize - 'compact' (last 100 data points) or 'full'
     * @returns {Promise<Array>} Array of stock data objects
     */
    async fetchStockData(symbol, interval = 'daily', outputSize = 'compact') {
        try {
            const response = await axios.get(this.baseURL, {
                params: {
                    function: interval === 'daily' ? 'TIME_SERIES_DAILY' : `TIME_SERIES_INTRADAY`,
                    symbol: symbol,
                    interval: interval !== 'daily' ? interval : undefined,
                    outputsize: outputSize,
                    apikey: this.apiKey
                }
            });

            const timeSeriesKey = interval === 'daily' 
                ? 'Time Series (Daily)' 
                : `Time Series (${interval})`;

            const timeSeries = response.data[timeSeriesKey];
            
            if (!timeSeries) {
                throw new Error('No data received from API');
            }

            // Convert the object to an array and format the data
            const formattedData = Object.keys(timeSeries).map(date => {
                const data = timeSeries[date];
                return {
                    date: new Date(date),
                    open: parseFloat(data['1. open']),
                    high: parseFloat(data['2. high']),
                    low: parseFloat(data['3. low']),
                    close: parseFloat(data['4. close']),
                    volume: parseFloat(data['5. volume'])
                };
            });

            // Sort by date ascending
            return formattedData.sort((a, b) => a.date - b.date);

        } catch (error) {
            console.error('Error fetching stock data:', error.message);
            throw error;
        }
    }

    /**
     * Get available stock symbols (mock data for demonstration)
     * @returns {Array} Array of stock symbols
     */
    getAvailableSymbols() {
        return [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
            'META', 'NVDA', 'NFLX', 'AMD', 'INTC'
        ];
    }
}

module.exports = StockDataFetcher;