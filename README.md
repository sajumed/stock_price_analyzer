## Stock Analysis Tool - JavaScript + Python Integration

A simple tool that fetches stock data using JavaScript and visualizes it using Python with technical indicators.

### Prerequisites

1. **Node.js** (v14 or higher)
2. **Python** (v3.7 or higher)
3. **Alpha Vantage API Key** (free from https://www.alphavantage.co/support/#api-key)

### Installation

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. **Get your API Key:**
   - Visit https://www.alphavantage.co/support/#api-key
   - Register for a free API key

2. **Update the API Key:**
   - Open `main.js`
   - Replace `'YOUR_ALPHA_VANTAGE_API_KEY'` with your actual API key

3. **Fetch Stock Data (JavaScript):**
   ```bash
   # Default: Fetch AAPL data
   npm start
   
   # Or fetch specific symbol
   node main.js MSFT
   ```

4. **Visualize Data (Python):**
   ```bash
   python stock_visualizer.py
   ```

### Features

- **Data Fetching:** Retrieves daily stock data from Alpha Vantage API
- **Technical Indicators:**
  - Simple Moving Average (SMA 20 & 50)
  - Relative Strength Index (RSI 14)
- **Visualizations:**
  - Comprehensive chart with price, SMAs, RSI, and volume
  - Simple price and volume chart
  - Data summary statistics

### File Structure

- `stock_data_fetcher.js` - Fetches and processes stock data
- `data_exporter.js` - Exports data to JSON format
- `main.js` - Main orchestration script
- `stock_visualizer.py` - Python visualization script
- `package.json` - Node.js dependencies
- `requirements.txt` - Python dependencies

### Example Output

The tool will:
1. Fetch stock data and calculate indicators
2. Export data to `stock_data.json`
3. Display interactive charts with:
   - Price line with SMA overlays
   - RSI indicator with overbought/oversold levels
   - Volume bars colored by