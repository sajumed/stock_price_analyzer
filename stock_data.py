import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class StockDataFetcher:
    def __init__(self):
        self.data = None
    
    def fetch_data(self, symbol, period="1y"):
        """
        Fetch stock data from Yahoo Finance
        """
        try:
            stock = yf.Ticker(symbol)
            self.data = stock.history(period=period)
            return True
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False
    
    def calculate_sma(self, window=20):
        """
        Calculate Simple Moving Average
        """
        if self.data is not None:
            self.data[f'SMA_{window}'] = self.data['Close'].rolling(window=window).mean()
            return self.data[f'SMA_{window}']
        return None
    
    def calculate_ema(self, window=20):
        """
        Calculate Exponential Moving Average
        """
        if self.data is not None:
            self.data[f'EMA_{window}'] = self.data['Close'].ewm(span=window, adjust=False).mean()
            return self.data[f'EMA_{window}']
        return None
    
    def calculate_rsi(self, window=14):
        """
        Calculate Relative Strength Index
        """
        if self.data is not None:
            delta = self.data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            self.data['RSI'] = 100 - (100 / (1 + rs))
            return self.data['RSI']
        return None
    
    def calculate_macd(self):
        """
        Calculate MACD (Moving Average Convergence Divergence)
        """
        if self.data is not None:
            ema_12 = self.data['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = self.data['Close'].ewm(span=26, adjust=False).mean()
            self.data['MACD'] = ema_12 - ema_26
            self.data['MACD_Signal'] = self.data['MACD'].ewm(span=9, adjust=False).mean()
            self.data['MACD_Histogram'] = self.data['MACD'] - self.data['MACD_Signal']
            return self.data['MACD'], self.data['MACD_Signal'], self.data['MACD_Histogram']
        return None
    
    def get_data(self):
        """
        Return the processed data
        """
        return self.data
    
    def get_latest_price(self):
        """
        Get the latest closing price
        """
        if self.data is not None and not self.data.empty:
            return self.data['Close'].iloc[-1]
        return None