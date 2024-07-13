import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class StockDataFetcher:
    def __init__(self):
        self.data = None
    
    def fetch_stock_data(self, symbol, period="1y"):
        """
        Fetch stock data from Yahoo Finance
        """
        try:
            stock = yf.Ticker(symbol)
            self.data = stock.history(period=period)
            
            if self.data.empty:
                print(f"No data found for symbol: {symbol}")
                return False
            
            # Calculate technical indicators
            self._calculate_indicators()
            return True
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False
    
    def _calculate_indicators(self):
        """
        Calculate basic technical indicators
        """
        # Simple Moving Averages
        self.data['SMA_20'] = self.data['Close'].rolling(window=20).mean()
        self.data['SMA_50'] = self.data['Close'].rolling(window=50).mean()
        
        # Exponential Moving Average
        self.data['EMA_12'] = self.data['Close'].ewm(span=12).mean()
        
        # Relative Strength Index (RSI)
        self.data['RSI'] = self._calculate_rsi(self.data['Close'])
        
        # Moving Average Convergence Divergence (MACD)
        self.data['MACD'], self.data['MACD_Signal'] = self._calculate_macd(self.data['Close'])
        
        # Bollinger Bands
        self.data['BB_Upper'], self.data['BB_Lower'] = self._calculate_bollinger_bands(self.data['Close'])
        
        # Clean up NaN values
        self.data = self.data.dropna()
    
    def _calculate_rsi(self, prices, period=14):
        """
        Calculate Relative Strength Index
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """
        Calculate MACD and Signal line
        """
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        return macd, macd_signal
    
    def _calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """
        Calculate Bollinger Bands
        """
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, lower_band
    
    def get_data(self):
        """
        Return the processed data
        """
        return self.data
    
    def get_summary_stats(self):
        """
        Get summary statistics for the stock
        """
        if self.data is None:
            return None
        
        latest = self.data.iloc[-1]
        return {
            'symbol': 'N/A',  # Would need to be passed separately
            'current_price': latest['Close'],
            'sma_20': latest['SMA_20'],
            'sma_50': latest['SMA_50'],
            'rsi': latest['RSI'],
            'macd': latest['MACD'],
            'volume': latest['Volume']
        }