/**
 * Stock Data Fetcher - Fetches stock data from Alpha Vantage API
 * Usage: node stock_data_fetcher.js SYMBOL
 */

const axios = require('axios');
const fs = require('fs');

class StockDataFetcher {
    constructor(apiKey = 'demo') {
        this.apiKey = apiKey;
        this.baseURL = 'https://www.alphavantage.co/query';
    }

    async fetchStockData(symbol, outputSize = 'compact') {
        try {
            console.log(`Fetching data for ${symbol}...`);
            
            const response = await axios.get(this.baseURL, {
                params: {
                    function: 'TIME_SERIES_DAILY',
                    symbol: symbol,
                    outputsize: outputSize,
                    apikey: this.apiKey
                }
            });

            if (response.data['Error Message']) {
                throw new Error('Invalid API call or symbol');
            }

            const timeSeries = response.data['Time Series (Daily)'];
            if (!timeSeries) {
                throw new Error('No data found for symbol');
            }

            // Convert to array and calculate technical indicators
            const stockData = this.processStockData(timeSeries);
            return stockData;

        } catch (error) {
            console.error('Error fetching stock data:', error.message);
            return null;
        }
    }

    processStockData(timeSeries) {
        const dates = Object.keys(timeSeries).sort();
        const processedData = [];

        for (let i = 0; i < dates.length; i++) {
            const date = dates[i];
            const dailyData = timeSeries[date];
            
            const dataPoint = {
                date: date,
                open: parseFloat(dailyData['1. open']),
                high: parseFloat(dailyData['2. high']),
                low: parseFloat(dailyData['3. low']),
                close: parseFloat(dailyData['4. close']),
                volume: parseInt(dailyData['5. volume'])
            };

            processedData.push(dataPoint);
        }

        // Calculate technical indicators
        return this.calculateIndicators(processedData.reverse());
    }

    calculateIndicators(data) {
        // Calculate Simple Moving Average (SMA)
        this.calculateSMA(data, 20);
        
        // Calculate Relative Strength Index (RSI)
        this.calculateRSI(data, 14);
        
        // Calculate Moving Average Convergence Divergence (MACD)
        this.calculateMACD(data);
        
        return data;
    }

    calculateSMA(data, period) {
        for (let i = period - 1; i < data.length; i++) {
            let sum = 0;
            for (let j = 0; j < period; j++) {
                sum += data[i - j].close;
            }
            data[i].sma = sum / period;
        }
    }

    calculateRSI(data, period) {
        // Calculate price changes
        const gains = [];
        const losses = [];

        for (let i = 1; i < data.length; i++) {
            const change = data[i].close - data[i - 1].close;
            gains.push(change > 0 ? change : 0);
            losses.push(change < 0 ? Math.abs(change) : 0);
        }

        // Calculate RSI
        for (let i = period; i < data.length; i++) {
            let avgGain = 0;
            let avgLoss = 0;

            for (let j = 0; j < period; j++) {
                avgGain += gains[i - 1 - j];
                avgLoss += losses[i - 1 - j];
            }

            avgGain /= period;
            avgLoss /= period;

            const rs = avgLoss === 0 ? 100 : avgGain / avgLoss;
            data[i].rsi = 100 - (100 / (1 + rs));
        }
    }

    calculateMACD(data) {
        // Calculate 12-day and 26-day EMA
        this.calculateEMA(data, 12, 'ema12');
        this.calculateEMA(data, 26, 'ema26');
        
        // Calculate MACD line
        for (let i = 25; i < data.length; i++) {
            if (data[i].ema12 && data[i].ema26) {
                data[i].macd = data[i].ema12 - data[i].ema26;
            }
        }

        // Calculate Signal line (9-day EMA of MACD)
        const macdValues = data.map(d => d.macd).filter(val => val !== undefined);
        const signalLine = this.calculateEMAForArray(macdValues, 9);
        
        // Add signal line to data
        for (let i = 0; i < signalLine.length; i++) {
            const dataIndex = data.length - signalLine.length + i;
            if (dataIndex >= 0) {
                data[dataIndex].signal = signalLine[i];
                data[dataIndex].histogram = data[dataIndex].macd - signalLine[i];
            }
        }
    }

    calculateEMA(data, period, fieldName) {
        const multiplier = 2 / (period + 1);
        let ema = data[period - 1].close;

        data[period - 1][fieldName] = ema;

        for (let i = period; i < data.length; i++) {
            ema = (data[i].close - ema) * multiplier + ema;
            data[i][fieldName] = ema;
        }
    }

    calculateEMAForArray(values, period) {
        const multiplier = 2 / (period + 1);
        const emaValues = [];
        let ema = values[period - 1];

        emaValues.push(ema);

        for (let i = period; i < values.length; i++) {
            ema = (values[i] - ema) * multiplier + ema;
            emaValues.push(ema);
        }

        return emaValues;
    }

    async saveToJSON(data, filename) {
        try {
            fs.writeFileSync(filename, JSON.stringify(data, null, 2));
            console.log(`Data saved to ${filename}`);
            return true;
        } catch (error) {
            console.error('Error saving data:', error.message);
            return false;
        }
    }
}

// Main execution
async function main() {
    const symbol = process.argv[2] || 'IBM';
    const fetcher = new StockDataFetcher();
    
    const stockData = await fetcher.fetchStockData(symbol);
    
    if (stockData) {
        const filename = `${symbol.toLowerCase()}_data.json`;
        await fetcher.saveToJSON(stockData, filename);
        console.log(`Fetched ${stockData.length} days of data for ${symbol}`);
    }
}

if (require.main === module) {
    main();
}

module.exports = StockDataFetcher;