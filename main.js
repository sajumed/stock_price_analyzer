// Main script - Orchestrates the stock data fetching and export
const StockDataFetcher = require('./stock_data_fetcher');
const DataExporter = require('./data_exporter');

async function main() {
    // Replace with your Alpha Vantage API key
    const API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY';
    
    if (API_KEY === 'YOUR_ALPHA_VANTAGE_API_KEY') {
        console.log('Please replace YOUR_ALPHA_VANTAGE_API_KEY with your actual API key');
        console.log('Get a free API key from: https://www.alphavantage.co/support/#api-key');
        return;
    }

    const fetcher = new StockDataFetcher(API_KEY);
    
    // Example: Fetch data for Apple Inc.
    const symbol = 'AAPL';
    
    console.log(`Fetching stock data for ${symbol}...`);
    
    const analysisData = await fetcher.getStockDataWithIndicators(symbol);
    
    if (analysisData) {
        console.log(`Successfully fetched ${analysisData.stockData.length} data points`);
        console.log(`Calculated ${analysisData.indicators.sma20.length} SMA20 points`);
        console.log(`Calculated ${analysisData.indicators.sma50.length} SMA50 points`);
        console.log(`Calculated ${analysisData.indicators.rsi.length} RSI points`);
        
        // Export data for Python visualization
        const pythonData = DataExporter.prepareDataForPython(analysisData);
        const exportPath = DataExporter.exportToJSON(pythonData);
        
        if (exportPath) {
            console.log('\nData ready for Python visualization!');
            console.log(`Run: python stock_visualizer.py`);
        }
    } else {
        console.log('Failed to fetch stock data');
    }
}

// Handle command line arguments
const symbol = process.argv[2] || 'AAPL';
main(symbol).catch(console.error);