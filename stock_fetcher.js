/**
 * Stock Data Fetcher - Fetches stock data and calculates basic technical indicators
 * Usage: node stock_fetcher.js SYMBOL DAYS
 * Example: node stock_fetcher.js AAPL 30
 */

const https = require('https');
const fs = require('fs');

class StockFetcher {
    constructor() {
        this.baseUrl = 'https://query1.finance.yahoo.com/v8/finance/chart/';
    }

    async fetchStockData(symbol, days = 30) {
        return new Promise((resolve, reject) => {
            const period1 = Math.floor(Date.now() / 1000) - (days * 24 * 60 * 60);
            const period2 = Math.floor(Date.now() / 1000);
            
            const url = `${this.baseUrl}${symbol}?period1=${period1}&period2=${period2}&interval=1d`;
            
            https.get(url, (response) => {
                let data = '';
                
                response.on('data', (chunk) => {
                    data += chunk;
                });
                
                response.on('end', () => {
                    try {
                        const result = JSON.parse(data);
                        const stockData = this.processData(result, symbol);
                        resolve(stockData);
                    } catch (error) {
                        reject(new Error('Failed to parse stock data'));
                    }
                });
                
            }).on('error', (error) => {
                reject(error);
            });
        });
    }

    processData(data, symbol) {
        if (!data.chart || !data.chart.result || !data.chart.result[0]) {
            throw new Error('Invalid stock data received');
        }

        const result = data.chart.result[0];
        const timestamps = result.timestamp;
        const quotes = result.indicators.quote[0];
        
        const stockData = [];
        
        for (let i = 0; i < timestamps.length; i++) {
            if (quotes.open[i] && quotes.high[i] && quotes.low[i] && quotes.close[i]) {
                stockData.push({
                    date: new Date(timestamps[i] * 1000).toISOString().split('T')[0],
                    open: quotes.open[i],
                    high: quotes.high[i],
                    low: quotes.low[i],
                    close: quotes.close[i],
                    volume: quotes.volume[i] || 0
                });
            }
        }
        
        // Calculate technical indicators
        const dataWithIndicators = this.calculateIndicators(stockData);
        
        return {
            symbol: symbol,
            data: dataWithIndicators
        };
    }

    calculateIndicators(data) {
        // Calculate Simple Moving Average (SMA)
        for (let i = 0; i < data.length; i++) {
            // SMA 20
            if (i >= 19) {
                let sum = 0;
                for (let j = i - 19; j <= i; j++) {
                    sum += data[j].close;
                }
                data[i].sma_20 = sum / 20;
            }
            
            // SMA 50
            if (i >= 49) {
                let sum = 0;
                for (let j = i - 49; j <= i; j++) {
                    sum += data[j].close;
                }
                data[i].sma_50 = sum / 50;
            }
            
            // RSI (simplified calculation)
            if (i > 0) {
                const change = data[i].close - data[i-1].close;
                data[i].price_change = change;
            }
        }
        
        // Calculate RSI (14-period)
        for (let i = 14; i < data.length; i++) {
            let gains = 0;
            let losses = 0;
            
            for (let j = i - 13; j <= i; j++) {
                if (data[j].price_change > 0) {
                    gains += data[j].price_change;
                } else {
                    losses += Math.abs(data[j].price_change);
                }
            }
            
            const avgGain = gains / 14;
            const avgLoss = losses / 14;
            const rs = avgGain / avgLoss;
            data[i].rsi = 100 - (100 / (1 + rs));
        }
        
        return data;
    }

    saveToJSON(data, filename = 'stock_data.json') {
        fs.writeFileSync(filename, JSON.stringify(data, null, 2));
        console.log(`Data saved to ${filename}`);
    }
}

// Main execution
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length < 1) {
        console.log('Usage: node stock_fetcher.js <SYMBOL> [DAYS]');
        console.log('Example: node stock_fetcher.js AAPL 30');
        process.exit(1);
    }
    
    const symbol = args[0].toUpperCase();
    const days = args[1] ? parseInt(args[1]) : 30;
    
    const fetcher = new StockFetcher();
    
    console.log(`Fetching ${days} days of data for ${symbol}...`);
    
    fetcher.fetchStockData(symbol, days)
        .then(data => {
            console.log(`Successfully fetched ${data.data.length} days of data for ${symbol}`);
            fetcher.saveToJSON(data);
        })
        .catch(error => {
            console.error('Error:', error.message);
        });
}

module.exports = StockFetcher;