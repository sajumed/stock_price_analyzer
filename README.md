## Stock Data Analysis Tool

A Python tool for fetching and visualizing stock price data with technical indicators.

### Features

- **Data Fetching**: Get historical stock data from Yahoo Finance
- **Technical Indicators**:
  - Simple Moving Averages (SMA 20, SMA 50)
  - Exponential Moving Average (EMA 12)
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
  - Bollinger Bands
- **Visualization**: Comprehensive dashboard with multiple plots
- **Command Line Interface**: Easy to use from terminal

### Installation

1. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Command Line Usage

```bash
# Basic usage
python main.py AAPL

# With custom period
python main.py TSLA --period 6mo

# Save plot to file
python main.py GOOGL --save --filename google_analysis.png

# All options
python main.py MSFT --period 2y --save --filename microsoft_analysis.png
```

#### Available Periods
- `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

#### Programmatic Usage

```python
from stock_data import StockDataFetcher
from stock_visualizer import StockVisualizer

# Fetch data
fetcher = StockDataFetcher()
fetcher.fetch_stock_data('AAPL', '1y')
data = fetcher.get_data()

# Create visualization
visualizer = StockVisualizer()
visualizer.create_dashboard(data, 'AAPL')
visualizer.show_plot()
visualizer.save_plot('apple_analysis.png')
```

### Output

The tool generates a comprehensive dashboard with:
1. **Price Chart**: Close price with moving averages and Bollinger Bands
2. **Volume**: Trading volume bars
3. **RSI**: Relative Strength Index with overbought/oversold levels
4. **MACD**: MACD line, signal line, and histogram

### Example Stock Symbols

- **AAPL** - Apple Inc.
- **TSLA** - Tesla Inc.
- **GOOGL** - Alphabet Inc. (Google)
- **MSFT** - Microsoft Corporation
- **AMZN** - Amazon.com Inc.
- **NFLX** - Netflix Inc.

### Notes

- Data is sourced from Yahoo Finance
- All calculations are based on closing prices
- The tool handles missing data automatically
- Plots are saved as high-resolution PNG files (300 DPI)

### Requirements

See `requirements.txt` for complete dependency list.