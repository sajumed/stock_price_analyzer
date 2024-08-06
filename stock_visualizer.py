"""
Stock Data Visualizer - Creates charts from stock data JSON files
"""

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import sys

class StockVisualizer:
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        self.fig = None
        self.axes = None
        
    def load_data(self, filename):
        """Load stock data from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            print(f"Loaded {len(data)} data points from {filename}")
            return data
        except FileNotFoundError:
            print(f"Error: File {filename} not found")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {filename}")
            return None
    
    def create_charts(self, data, symbol="STOCK"):
        """Create comprehensive stock analysis charts"""
        if not data:
            return
        
        # Convert dates to datetime objects
        dates = [datetime.strptime(d['date'], '%Y-%m-%d') for d in data]
        
        # Extract price data
        closes = [d['close'] for d in data]
        opens = [d['open'] for d in data]
        highs = [d['high'] for d in data]
        lows = [d['low'] for d in data]
        
        # Create subplots
        self.fig, self.axes = plt.subplots(4, 1, figsize=(12, 14))
        self.fig.suptitle(f'Stock Analysis - {symbol}', fontsize=16, fontweight='bold')
        
        # Plot 1: Price and SMA
        self.plot_price_sma(self.axes[0], dates, data, symbol)
        
        # Plot 2: RSI
        self.plot_rsi(self.axes[1], dates, data)
        
        # Plot 3: MACD
        self.plot_macd(self.axes[2], dates, data)
        
        # Plot 4: Volume
        self.plot_volume(self.axes[3], dates, data)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.94)
        
    def plot_price_sma(self, ax, dates, data, symbol):
        """Plot price data and SMA"""
        closes = [d['close'] for d in data]
        sma_values = [d.get('sma', None) for d in data]
        
        ax.plot(dates, closes, label='Close Price', linewidth=2, color='blue', alpha=0.7)
        
        # Plot SMA if available
        sma_dates = [date for date, sma in zip(dates, sma_values) if sma is not None]
        sma_clean = [sma for sma in sma_values if sma is not None]
        if sma_clean:
            ax.plot(sma_dates, sma_clean, label='20-day SMA', linewidth=2, color='red', alpha=0.7)
        
        ax.set_title(f'{symbol} - Price and Moving Average')
        ax.set_ylabel('Price ($)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def plot_rsi(self, ax, dates, data):
        """Plot RSI indicator"""
        rsi_values = [d.get('rsi', None) for d in data]
        rsi_dates = [date for date, rsi in zip(dates, rsi_values) if rsi is not None]
        rsi_clean = [rsi for rsi in rsi_values if rsi is not None]
        
        if rsi_clean:
            ax.plot(rsi_dates, rsi_clean, label='RSI (14)', linewidth=2, color='purple')
            ax.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought (70)')
            ax.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold (30)')
            ax.axhline(y=50, color='gray', linestyle='-', alpha=0.5)
            ax.fill_between(rsi_dates, 70, 100, alpha=0.2, color='red')
            ax.fill_between(rsi_dates, 0, 30, alpha=0.2, color='green')
        
        ax.set_title('Relative Strength Index (RSI)')
        ax.set_ylabel('RSI')
        ax.set_ylim(0, 100)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def plot_macd(self, ax, dates, data):
        """Plot MACD indicator"""
        macd_values = [d.get('macd', None) for d in data]
        signal_values = [d.get('signal', None) for d in data]
        histogram_values = [d.get('histogram', None) for d in data]
        
        # Filter out None values
        valid_indices = [i for i, (m, s, h) in enumerate(zip(macd_values, signal_values, histogram_values)) 
                        if m is not None and s is not None and h is not None]
        
        if valid_indices:
            macd_dates = [dates[i] for i in valid_indices]
            macd_clean = [macd_values[i] for i in valid_indices]
            signal_clean = [signal_values[i] for i in valid_indices]
            histogram_clean = [histogram_values[i] for i in valid_indices]
            
            # Plot MACD and Signal line
            ax.plot(macd_dates, macd_clean, label='MACD', linewidth=2, color='blue')
            ax.plot(macd_dates, signal_clean, label='Signal Line', linewidth=2, color='red')
            
            # Plot histogram
            colors = ['green' if h >= 0 else 'red' for h in histogram_clean]
            ax.bar(macd_dates, histogram_clean, color=colors, alpha=0.5, label='Histogram', width=2)
            
            ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        ax.set_title('MACD Indicator')
        ax.set_ylabel('MACD')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def plot_volume(self, ax, dates, data):
        """Plot trading volume"""
        volumes = [d['volume'] for d in data]
        
        # Color volume bars based on price movement
        colors = []
        for i in range(len(data)):
            if i == 0:
                colors.append('gray')
            else:
                colors.append('green' if data[i]['close'] > data[i-1]['close'] else 'red')
        
        ax.bar(dates, volumes, color=colors, alpha=0.7, width=1)
        ax.set_title('Trading Volume')
        ax.set_ylabel('Volume')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def save_plot(self, filename='stock_analysis.png'):
        """Save the plot to file"""
        if self.fig:
            self.fig.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Plot saved as {filename}")
    
    def show_plot(self):
        """Display the plot"""
        if self.fig:
            plt.show()

def main():
    if len(sys.argv) < 2:
        print("Usage: python stock_visualizer.py <json_filename>")
        print("Example: python stock_visualizer.py ibm_data.json")
        return
    
    filename = sys.argv[1]
    symbol = filename.split('_')[0].upper()
    
    visualizer = StockVisualizer()
    data = visualizer.load_data(filename)
    
    if data:
        visualizer.create_charts(data, symbol)
        visualizer.save_plot(f"{symbol}_analysis.png")
        visualizer.show_plot()

if __name__ == "__main__":
    main()