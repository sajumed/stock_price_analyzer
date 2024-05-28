// Stock Data Fetcher - Fetches stock data from Alpha Vantage API
const axios = require('axios');

class StockDataFetcher {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseURL = 'https://www.alphavantage.co/query';
    }

    async fetchStockData(symbol, interval = 'daily', outputSize = 'compact') {
        try {
            const response = await axios.get(this.baseURL, {
                params: {
                    function: `TIME_SERIES_${interval.toUpperCase()}`,
                    symbol: symbol,
                    apikey: this.apiKey,
                    outputsize: outputSize,
                    datatype: 'json'
                }
            });

            const timeSeriesKey = `Time Series (${interval.charAt(0).toUpperCase() + interval.slice(1)})`;
            const timeSeries = response.data[timeSeriesKey];
            
            if (!timeSeries) {
                throw new Error('No time series data found');
            }

            return this.processData(timeSeries, symbol);
        } catch (error) {
            console.error('Error fetching stock data:', error.message);
            return null;
        }
    }

    processData(timeSeries, symbol) {
        const data = [];
        
        for (const [date, values] of Object.entries(timeSeries)) {
            data.push({
                date: date,
                symbol: symbol,
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

    calculateSMA(data, period = 20) {
        const smaData = [];
        
        for (let i = period - 1; i < data.length; i++) {
            const slice = data.slice(i - period + 1, i + 1);
            const sum = slice.reduce((acc, item) => acc + item.close, 0);
            const sma = sum / period;
            
            smaData.push({
                date: data[i].date,
                sma: sma
            });
        }
        
        return smaData;
    }

    calculateRSI(data, period = 14) {
        const rsiData = [];
        const gains = [];
        const losses = [];

        // Calculate price changes
        for (let i = 1; i < data.length; i++) {
            const change = data[i].close - data[i - 1].close;
            gains.push(change > 0 ? change : 0);
            losses.push(change < 0 ? Math.abs(change) : 0);
        }

        // Calculate RSI
        for (let i = period; i < gains.length; i++) {
            const avgGain = gains.slice(i - period, i).reduce((a, b) => a + b) / period;
            const avgLoss = losses.slice(i - period, i).reduce((a, b) => a + b) / period;
            
            const rs = avgLoss === 0 ? 100 : avgGain / avgLoss;
            const rsi = 100 - (100 / (1 + rs));
            
            rsiData.push({
                date: data[i + 1].date, // +1 because we started from index 1 for changes
                rsi: rsi
            });
        }
        
        return rsiData;
    }

    async getStockDataWithIndicators(symbol) {
        const stockData = await this.fetchStockData(symbol);
        if (!stockData) return null;

        const sma20 = this.calculateSMA(stockData, 20);
        const sma50 = this.calculateSMA(stockData, 50);
        const rsi = this.calculateRSI(stockData, 14);

        return {
            symbol: symbol,
            stockData: stockData,
            indicators: {
                sma20: sma20,
                sma50: sma50,
                rsi: rsi
            }
        };
    }
}

module.exports = StockDataFetcher;