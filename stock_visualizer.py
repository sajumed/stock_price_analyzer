#!/usr/bin/env python3
"""
Stock Data Visualizer - Creates charts for stock data with technical indicators
"""

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import argparse
import sys

class StockVisualizer:
    def __init__(self, data_file='stock_data.json'):
        self.data_file = data_file
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Load stock data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
            print(f"Loaded data for {self.data['symbol']} ({len(self.data['data'])} days)")
        except FileNotFoundError:
            print(f"Error: File {self.data_file} not found. Run stock_fetcher.js first.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.data_file}")
            sys.exit(1)
    
    def create_price_chart(self, save_path='stock_chart.png'):
        """Create a price chart with moving averages"""
        dates = [datetime.strptime(day['date'], '%Y-%m-%d') for day in self.data['data']]
        closes = [day['close'] for day in self.data['data']]
        
        # Prepare SMA data
        sma_20 = [day.get('sma_20') for day in self.data['data']]
        sma_50 = [day.get('sma_50') for day in self.data['data']]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})
        
        # Price and moving averages
        ax1.plot(dates, closes, label='Close Price', linewidth=2, color='black')
        ax1.plot(dates, sma_20, label='SMA 20', linewidth=1, color='blue', alpha=0.7)
        ax1.plot(dates, sma_50, label='SMA 50', linewidth=1, color='red', alpha=0.7)
        
        ax1.set_title(f'{self.data["symbol"]} Stock Price with Moving Averages')
        ax1.set_ylabel('Price ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Format x-axis
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        
        # RSI
        rsi_values = [day.get('rsi') for day in self.data['data']]
        ax2.plot(dates, rsi_values, label='RSI (14)', linewidth=2, color='purple')
        ax2.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought (70)')
        ax2.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold (30)')
        ax2.set_ylabel('RSI')
        ax2.set_ylim(0, 100)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Format x-axis for both subplots
        for ax in [ax1, ax2]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved as {save_path}")
        plt.show()
    
    def create_candlestick_chart(self, save_path='candlestick_chart.png'):
        """Create a candlestick chart (simplified)"""
        # Use last 20 days for better visibility
        recent_data = self.data['data'][-20:]
        
        dates = [datetime.strptime(day['date'], '%Y-%m-%d') for day in recent_data]
        opens = [day['open'] for day in recent_data]
        highs = [day['high'] for day in recent_data]
        lows = [day['low'] for day in recent_data]
        closes = [day['close'] for day in recent_data]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Simple candlestick representation
        for i, date in enumerate(dates):
            color = 'green' if closes[i] >= opens[i] else 'red'
            
            # High-low line
            ax.plot([date, date], [lows[i], highs[i]], color='black', linewidth=1)
            
            # Open-close rectangle
            ax.plot([date, date], [opens[i], closes[i]], color=color, linewidth=3)
        
        ax.set_title(f'{self.data["symbol"]} Candlestick Chart (Last 20 Days)')
        ax.set_ylabel('Price ($)')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Candlestick chart saved as {save_path}")
        plt.show()
    
    def print_summary(self):
        """Print a summary of the stock data"""
        if not self.data or not self.data['data']:
            print("No data available")
            return
        
        latest = self.data['data'][-1]
        first = self.data['data'][0]
        
        price_change = latest['close'] - first['close']
        percent_change = (price_change / first['close']) * 100
        
        print(f"\n=== {self.data['symbol']} Stock Summary ===")
        print(f"Period: {first['date']} to {latest['date']}")
        print(f"First Close: ${first['close']:.2f}")
        print(f"Latest Close: ${latest['close']:.2f}")
        print(f"Change: ${price_change:.2f} ({percent_change:+.2f}%)")
        
        if 'rsi' in latest:
            print(f"Latest RSI: {latest['rsi']:.2f}")
            rsi_status = "Overbought" if latest['rsi'] > 70 else "Oversold" if latest['rsi'] < 30 else "Neutral"
            print(f"RSI Status: {rsi_status}")

def main():
    parser = argparse.ArgumentParser(description='Stock Data Visualizer')
    parser.add_argument('--file', default='stock_data.json', help='Stock data JSON file')
    parser.add_argument('--chart-type', choices=['price', 'candlestick', 'both'], 
                       default='price', help='Type of chart to generate')
    
    args = parser.parse_args()
    
    visualizer = StockVisualizer(args.file)
    visualizer.print_summary()
    
    if args.chart_type in ['price', 'both']:
        visualizer.create_price_chart()
    
    if args.chart_type in ['candlestick', 'both']:
        visualizer.create_candlestick_chart()

if __name__ == '__main__':
    main()