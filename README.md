.md

# Stock Data Analysis Tool

A Python tool for fetching and visualizing stock price data with basic technical indicators.

## Features

- Fetch historical stock data from Yahoo Finance
- Calculate technical indicators:
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Relative Strength Index (RSI)
  - MACD (Moving Average Convergence Divergence)
- Interactive visualization with matplotlib
- Command-line interface
- Export charts to image files

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Basic usage:
```bash
python main.py AAPL
```

With custom period:
```bash
python main.py TSLA --period 2y
```

Simple chart (no indicators):
```bash
python main.py GOOGL --simple
```

Save chart to file:
```bash
python main.py MSFT --save microsoft_analysis.png
```

### Available Time Periods
- `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

### Python API

```python
from stock_data import StockDataFetcher
from stock_visualizer import StockVisualizer

# Fetch data
fetcher = StockDataFetcher()
fetcher.fetch_data('AAPL', '1y')

# Calculate indicators
fetcher.calculate_sma(20)
fetcher.calculate_ema(20)
fetcher.calculate_rsi(14)
fetcher.calculate_macd()

# Visualize
visualizer = StockVisualizer()
fig, axs = visualizer.create_price_chart(fetcher.get_data(), 'AAPL')
visualizer.show_chart()
```

## Example

Run the example script to see the tool in action:
```bash
python example_usage.py
```

This will analyze AAPL, TSLA, and GOOGL stocks and save charts for each.

## Output

The tool provides:
- Interactive charts with price and indicators
- Latest price information
- Technical indicator values
- Exportable chart images

## Requirements

- Python 3.7+
- yfinance
- pandas
- numpy
- matplotlib
- seaborn

## Notes

- Data is sourced from Yahoo Finance
- All calculations are based on closing prices
- Charts include buy/sell signals based on RSI levels
- MACD histogram shows momentum changes

## License

This project is for educational purposes.