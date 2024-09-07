import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class StockDataFetcher:
    def __init__(self):
        self.available_indicators = ['SMA', 'EMA', 'RSI', 'MACD', 'Bollinger_Bands']
    
    def fetch_stock_data(self, symbol, period='6mo'):
        """
        Fetch stock data using yfinance
        """
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            
            if data.empty:
                raise ValueError(f"No data found for symbol: {symbol}")
            
            return data
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def calculate_sma(self, data, window=20):
        """Calculate Simple Moving Average"""
        return data['Close'].rolling(window=window).mean()
    
    def calculate_ema(self, data, window=20):
        """Calculate Exponential Moving Average"""
        return data['Close'].ewm(span=window, adjust=False).mean()
    
    def calculate_rsi(self, data, window=14):
        """Calculate Relative Strength Index"""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, data):
        """Calculate MACD"""
        ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        return macd, signal, histogram
    
    def calculate_bollinger_bands(self, data, window=20):
        """Calculate Bollinger Bands"""
        sma = data['Close'].rolling(window=window).mean()
        std = data['Close'].rolling(window=window).std()
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)
        return upper_band, sma, lower_band
    
    def add_technical_indicators(self, data, indicators=None):
        """
        Add selected technical indicators to the data
        """
        if indicators is None:
            indicators = self.available_indicators
        
        data_with_indicators = data.copy()
        
        if 'SMA' in indicators:
            data_with_indicators['SMA_20'] = self.calculate_sma(data, 20)
            data_with_indicators['SMA_50'] = self.calculate_sma(data, 50)
        
        if 'EMA' in indicators:
            data_with_indicators['EMA_20'] = self.calculate_ema(data, 20)
        
        if 'RSI' in indicators:
            data_with_indicators['RSI'] = self.calculate_rsi(data)
        
        if 'MACD' in indicators:
            macd, signal, histogram = self.calculate_macd(data)
            data_with_indicators['MACD'] = macd
            data_with_indicators['MACD_Signal'] = signal
            data_with_indicators['MACD_Histogram'] = histogram
        
        if 'Bollinger_Bands' in indicators:
            upper, middle, lower = self.calculate_bollinger_bands(data)
            data_with_indicators['BB_Upper'] = upper
            data_with_indicators['BB_Middle'] = middle
            data_with_indicators['BB_Lower'] = lower
        
        return data_with_indicators
    
    def prepare_data_for_js(self, data):
        """
        Convert pandas DataFrame to JSON format for JavaScript
        """
        # Reset index to include Date as a column
        data_reset = data.reset_index()
        data_reset['Date'] = data_reset['Date'].dt.strftime('%Y-%m-%d')
        
        # Convert to dictionary
        data_dict = {
            'dates': data_reset['Date'].tolist(),
            'prices': {
                'open': data_reset['Open'].fillna(0).tolist(),
                'high': data_reset['High'].fillna(0).tolist(),
                'low': data_reset['Low'].fillna(0).tolist(),
                'close': data_reset['Close'].fillna(0).tolist(),
                'volume': data_reset['Volume'].fillna(0).tolist()
            }
        }
        
        # Add technical indicators if they exist
        if 'SMA_20' in data_reset.columns:
            data_dict['indicators'] = {
                'sma_20': data_reset['SMA_20'].fillna(0).tolist(),
                'sma_50': data_reset['SMA_50'].fillna(0).tolist(),
                'ema_20': data_reset['EMA_20'].fillna(0).tolist() if 'EMA_20' in data_reset.columns else [],
                'rsi': data_reset['RSI'].fillna(0).tolist() if 'RSI' in data_reset.columns else [],
                'macd': data_reset['MACD'].fillna(0).tolist() if 'MACD' in data_reset.columns else [],
                'macd_signal': data_reset['MACD_Signal'].fillna(0).tolist() if 'MACD_Signal' in data_reset.columns else [],
                'bb_upper': data_reset['BB_Upper'].fillna(0).tolist() if 'BB_Upper' in data_reset.columns else [],
                'bb_middle': data_reset['BB_Middle'].fillna(0).tolist() if 'BB_Middle' in data_reset.columns else [],
                'bb_lower': data_reset['BB_Lower'].fillna(0).tolist() if 'BB_Lower' in data_reset.columns else []
            }
        
        return data_dict

def main():
    fetcher = StockDataFetcher()
    
    # Example usage
    symbol = "AAPL"
    print(f"Fetching data for {symbol}...")
    
    # Fetch stock data
    data = fetcher.fetch_stock_data(symbol, period='6mo')
    
    if data is not None:
        # Add all technical indicators
        data_with_indicators = fetcher.add_technical_indicators(data)
        
        # Prepare data for JavaScript
        js_data = fetcher.prepare_data_for_js(data_with_indicators)
        
        # Save to JSON file
        with open('stock_data.json', 'w') as f:
            json.dump(js_data, f, indent=2)
        
        print(f"Data saved to stock_data.json")
        print(f"Total records: {len(data)}")
        print(f"Date range: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")
        
        # Display basic statistics
        print(f"\nBasic Statistics:")
        print(f"Current Price: ${data['Close'].iloc[-1]:.2f}")
        print(f"50-day SMA: ${data_with_indicators['SMA_50'].iloc[-1]:.2f}")
        if 'RSI' in data_with_indicators.columns:
            print(f"RSI: {data_with_indicators['RSI'].iloc[-1]:.2f}")
    else:
        print("Failed to fetch data")

if __name__ == "__main__":
    main()