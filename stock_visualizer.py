#!/usr/bin/env python3
"""
Stock Data Visualizer - Python script for visualizing stock data with technical indicators
"""

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

class StockVisualizer:
    def __init__(self, data_file='stock_data.json'):
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self):
        """Load stock data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Data file '{self.data_file}' not found.")
            print("Please run the JavaScript script first to fetch data.")
            return None
    
    def create_comprehensive_chart(self):
        """Create a comprehensive stock chart with price and indicators"""
        if not self.data:
            return
        
        stock_data = self.data['stock_data']
        indicators = self.data['indicators']
        symbol = self.data['symbol']
        
        # Convert dates to datetime objects
        dates = [datetime.strptime(item['date'], '%Y-%m-%d') for item in stock_data]
        
        # Create subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12), 
                                           gridspec_kw={'height_ratios': [3, 1, 1]})
        
        # Plot 1: Price data with SMAs
        closes = [item['close'] for item in stock_data]
        ax1.plot(dates, closes, label='Close Price', linewidth=2, color='black')
        
        # Plot SMAs if available
        if indicators['sma20']:
            sma20_dates = [datetime.strptime(item['date'], '%Y-%m-%d') for item in indicators['sma20']]
            sma20_values = [item['sma'] for item in indicators['sma20']]
            ax1.plot(sma20_dates, sma20_values, label='SMA 20', linewidth=1.5, color='blue')
        
        if indicators['sma50']:
            sma50_dates = [datetime.strptime(item['date'], '%Y-%m-%d') for item in indicators['sma50']]
            sma50_values = [item['sma'] for item in indicators['sma50']]
            ax1.plot(sma50_dates, sma50_values, label='SMA 50', linewidth=1.5, color='red')
        
        ax1.set_title(f'{symbol} Stock Price with Technical Indicators', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Price ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: RSI
        if indicators['rsi']:
            rsi_dates = [datetime.strptime(item['date'], '%Y-%m-%d') for item in indicators['rsi']]
            rsi_values = [item['rsi'] for item in indicators['rsi']]
            ax2.plot(rsi_dates, rsi_values, label='RSI', linewidth=2, color='purple')
            ax2.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought (70)')
            ax2.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold (30)')
            ax2.set_ylabel('RSI')
            ax2.set_ylim(0, 100)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        # Plot 3: Volume
        volumes = [item['volume'] for item in stock_data]
        # Use different colors for up/down days
        colors = ['green' if stock_data[i]['close'] >= stock_data[i]['open'] else 'red' 
                 for i in range(len(stock_data))]
        
        ax3.bar(dates, volumes, color=colors, alpha=0.7)
        ax3.set_ylabel('Volume')
        ax3.set_xlabel('Date')
        ax3.grid(True, alpha=0.3)
        
        # Format x-axis
        for ax in [ax1, ax2, ax3]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def create_simple_chart(self):
        """Create a simple price chart"""
        if not self.data:
            return
        
        stock_data = self.data['stock_data']
        symbol = self.data['symbol']
        
        dates = [datetime.strptime(item['date'], '%Y-%m-%d') for item in stock_data]
        closes = [item['close'] for item in stock_data]
        volumes = [item['volume'] for item in stock_data]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Price chart
        ax1.plot(dates, closes, linewidth=2, color='blue')
        ax1.set_title(f'{symbol} Stock Price', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Price ($)')
        ax1.grid(True, alpha=0.3)
        
        # Volume chart
        ax2.bar(dates, volumes, color='gray', alpha=0.7)
        ax2.set_ylabel('Volume')
        ax2.set_xlabel('Date')
        ax2.grid(True, alpha=0.3)
        
        # Format dates
        for ax in [ax1, ax2]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def print_summary(self):
        """Print a summary of the stock data"""
        if not self.data:
            return
        
        stock_data = self.data['stock_data']
        symbol = self.data['symbol']
        
        latest = stock_data[-1]
        oldest = stock_data[0]
        
        print(f"\n=== {symbol} Stock Analysis Summary ===")
        print(f"Analysis Period: {oldest['date']} to {latest['date']}")
        print(f"Total Data Points: {len(stock_data)}")
        print(f"\nLatest Data ({latest['date']}):")
        print(f"  Close: ${latest['close']:.2f}")
        print(f"  Open: ${latest['open']:.2f}")
        print(f"  High: ${latest['high']:.2f}")
        print(f"  Low: ${latest['low']:.2f}")
        print(f"  Volume: {latest['volume']:,}")
        
        # Calculate price change
        price_change = latest['close'] - oldest['close']
        percent_change = (price_change / oldest['close']) * 100
        print(f"\nPeriod Change: ${price_change:.2f} ({percent_change:+.2f}%)")

def main():
    visualizer = StockVisualizer()
    
    if visualizer.data:
        visualizer.print_summary()
        
        print("\nChoose visualization type:")
        print("1. Comprehensive Chart (Price + Indicators)")
        print("2. Simple Price Chart")
        
        try:
            choice = input("Enter your choice (1 or 2): ").strip()
            if choice == '1':
                visualizer.create_comprehensive_chart()
            elif choice == '2':
                visualizer.create_simple_chart()
            else:
                print("Invalid choice. Showing comprehensive chart.")
                visualizer.create_comprehensive_chart()
        except KeyboardInterrupt:
            print("\nExiting...")

if __name__ == "__main__":
    main()