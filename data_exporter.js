// Data Exporter - Exports stock data to JSON file for Python processing
const fs = require('fs');
const path = require('path');

class DataExporter {
    static exportToJSON(data, filename = 'stock_data.json') {
        try {
            const filePath = path.join(__dirname, filename);
            fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
            console.log(`Data exported to ${filePath}`);
            return filePath;
        } catch (error) {
            console.error('Error exporting data:', error.message);
            return null;
        }
    }

    static prepareDataForPython(analysisData) {
        const pythonData = {
            symbol: analysisData.symbol,
            stock_data: analysisData.stockData,
            indicators: analysisData.indicators
        };
        
        return pythonData;
    }
}

module.exports = DataExporter;