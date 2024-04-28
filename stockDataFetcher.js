/**
 * Stock Data Fetcher - Fetches historical stock data from Alpha Vantage API
 */

class StockDataFetcher {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseUrl = 'https://www.alphavantage.co/query';
    }

    /**
     * Fetch daily stock data for a given symbol
     * @param {string} symbol - Stock symbol (e.g., 'AAPL')
     * @param {string} outputSize - 'compact' (last 100 days) or 'full' (20+ years)
     * @returns {Promise<Array>} Array of stock data objects
     */
    async fetchStockData(symbol, outputSize = 'compact') {
        try {
            const url = `${this.baseUrl}?function=TIME_SERIES_DAILY&symbol=${symbol}&outputsize=${outputSize}&apikey=${this.apiKey}`;
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (data['Error Message']) {
                throw new Error(`API Error: ${data['Error Message']}`);
            }
            
            if (data['Note']) {
                console.warn('API Limit Note:', data['Note']);
            }
            
            const timeSeries = data['Time Series (Daily)'];
            if (!timeSeries) {
                throw new Error('No time series data found in response');
            }
            
            return this.parseTimeSeries(timeSeries, symbol);
            
        } catch (error) {
            console.error('Error fetching stock data:', error);
            throw error;
        }
    }

    /**
     * Parse time series data into structured format
     */
    parseTimeSeries(timeSeries, symbol) {
        const data = [];
        
        for (const [date, values] of Object.entries(timeSeries)) {
            data.push({
                symbol: symbol,
                date: date,
                open: parseFloat(values['1. open']),
                high: parseFloat(values['2. high']),
                low: parseFloat(values['3. low']),
                close: parseFloat(values['4. close']),
                volume: parseInt(values['5. volume'])
            });
        }
        
        // Sort by date ascending
        return data.sort((a, b) => new Date(a.date) - new Date(b.date));
    }

    /**
     * Fetch data for multiple symbols
     */
    async fetchMultipleStocks(symbols, outputSize = 'compact') {
        const promises = symbols.map(symbol => this.fetchStockData(symbol, outputSize));
        return Promise.all(promises);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StockDataFetcher;
}