#!/usr/bin/env python3
"""
Stock Data Fetcher - Fetches historical stock data from Alpha Vantage API
"""

import requests
import pandas as pd
import json
import sys
from datetime import datetime, timedelta

class StockFetcher:
    def __init__(self, api_key=None):
        # Use demo key or provide your own Alpha Vantage API key
        self.api_key = api_key or "demo"
        self.base_url = "https://www.alphavantage.co/query"
    
    def fetch_stock_data(self, symbol, period="3month"):
        """
        Fetch historical stock data for a given symbol
        Periods: 1month, 3month, 1year, 2year
        """
        try:
            # Map periods to Alpha Vantage function
            period_map = {
                "1month": "TIME_SERIES_DAILY",
                "3month": "TIME_SERIES_DAILY", 
                "1year": "TIME_SERIES_WEEKLY",
                "2year": "TIME_SERIES_WEEKLY"
            }
            
            function = period_map.get(period, "TIME_SERIES_DAILY")
            
            params = {
                "function": function,
                "symbol": symbol,
                "apikey": self.api_key,
                "outputsize": "compact" if period == "1month" else "full"
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if "Error Message" in data:
                return {"error": f"Invalid symbol: {symbol}"}
            
            # Extract time series data
            time_series_key = "Time Series (Daily)" if "Daily" in function else "Weekly Time Series"
            
            if time_series_key not in data:
                return {"error": f"No data found for symbol: {symbol}"}
            
            time_series = data[time_series_key]
            
            # Convert to DataFrame and calculate technical indicators
            df = self._process_data(time_series, symbol)
            return df.to_dict('records')
            
        except Exception as e:
            return {"error": f"Error fetching data: {str(e)}"}
    
    def _process_data(self, time_series, symbol):
        """Process raw time series data and calculate technical indicators"""
        records = []
        
        for date, values in time_series.items():
            records.append({
                "date": date,
                "symbol": symbol,
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": int(values["5. volume"])
            })
        
        df = pd.DataFrame(records)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Calculate technical indicators
        df = self._calculate_technical_indicators(df)
        return df
    
    def _calculate_technical_indicators(self, df):
        """Calculate basic technical indicators"""
        # Simple Moving Averages
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        # RSI (Relative Strength Index)
        df['rsi'] = self._calculate_rsi(df['close'])
        
        # MACD
        df['macd'], df['macd_signal'] = self._calculate_macd(df['close'])
        
        # Bollinger Bands
        df['bb_upper'], df['bb_lower'] = self._calculate_bollinger_bands(df['close'])
        
        return df
    
    def _calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD indicator"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        return macd, macd_signal
    
    def _calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, lower_band

def main():
    if len(sys.argv) < 2:
        print("Usage: python stock_fetcher.py <symbol> [period]")
        print("Example: python stock_fetcher.py AAPL 3month")
        sys.exit(1)
    
    symbol = sys.argv[1]
    period = sys.argv[2] if len(sys.argv) > 2 else "3month"
    
    fetcher = StockFetcher()
    data = fetcher.fetch_stock_data(symbol, period)
    
    if "error" in data:
        print(f"Error: {data['error']}")
        sys.exit(1)
    
    # Save data to JSON file for JavaScript to use
    output_file = f"{symbol.lower()}_data.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    print(f"Data saved to {output_file}")
    print(f"Fetched {len(data)} records for {symbol}")

if __name__ == "__main__":
    main()