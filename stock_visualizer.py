import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
import seaborn as sns

class StockVisualizer:
    def __init__(self):
        style.use('seaborn-v0_8')
        self.fig = None
        self.colors = {
            'price': '#1f77b4',
            'sma_20': '#ff7f0e',
            'sma_50': '#2ca02c',
            'ema_12': '#d62728',
            'volume': '#7f7f7f',
            'rsi': '#9467bd',
            'macd': '#17becf',
            'signal': '#e377c2'
        }
    
    def create_dashboard(self, data, symbol):
        """
        Create a comprehensive stock analysis dashboard
        """
        self.fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        self.fig.suptitle(f'Stock Analysis: {symbol}', fontsize=16, fontweight='bold')
        
        # Plot 1: Price and Moving Averages
        self._plot_price_indicators(axes[0], data, symbol)
        
        # Plot 2: Volume
        self._plot_volume(axes[1], data)
        
        # Plot 3: RSI
        self._plot_rsi(axes[2], data)
        
        # Plot 4: MACD
        self._plot_macd(axes[3], data)
        
        plt.tight_layout()
        return self.fig
    
    def _plot_price_indicators(self, ax, data, symbol):
        """
        Plot price data with moving averages and Bollinger Bands
        """
        # Price and Moving Averages
        ax.plot(data.index, data['Close'], label='Close Price', 
                color=self.colors['price'], linewidth=2)
        ax.plot(data.index, data['SMA_20'], label='SMA 20', 
                color=self.colors['sma_20'], alpha=0.7)
        ax.plot(data.index, data['SMA_50'], label='SMA 50', 
                color=self.colors['sma_50'], alpha=0.7)
        ax.plot(data.index, data['EMA_12'], label='EMA 12', 
                color=self.colors['ema_12'], alpha=0.7)
        
        # Bollinger Bands
        ax.fill_between(data.index, data['BB_Upper'], data['BB_Lower'], 
                       alpha=0.2, color='gray', label='Bollinger Bands')
        
        ax.set_title('Price and Technical Indicators')
        ax.set_ylabel('Price ($)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
    
    def _plot_volume(self, ax, data):
        """
        Plot trading volume
        """
        ax.bar(data.index, data['Volume'], color=self.colors['volume'], alpha=0.7)
        ax.set_title('Trading Volume')
        ax.set_ylabel('Volume')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
    
    def _plot_rsi(self, ax, data):
        """
        Plot RSI indicator
        """
        ax.plot(data.index, data['RSI'], color=self.colors['rsi'], linewidth=2)
        ax.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought (70)')
        ax.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold (30)')
        ax.axhline(y=50, color='gray', linestyle='-', alpha=0.3)
        ax.fill_between(data.index, 70, data['RSI'], where=(data['RSI'] >= 70), 
                       color='red', alpha=0.3)
        ax.fill_between(data.index, 30, data['RSI'], where=(data['RSI'] <= 30), 
                       color='green', alpha=0.3)
        ax.set_title('Relative Strength Index (RSI)')
        ax.set_ylabel('RSI')
        ax.set_ylim(0, 100)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
    
    def _plot_macd(self, ax, data):
        """
        Plot MACD indicator
        """
        ax.plot(data.index, data['MACD'], label='MACD', 
                color=self.colors['macd'], linewidth=2)
        ax.plot(data.index, data['MACD_Signal'], label='Signal Line', 
                color=self.colors['signal'], linewidth=2)
        
        # Plot histogram
        macd_histogram = data['MACD'] - data['MACD_Signal']
        colors = ['green' if x >= 0 else 'red' for x in macd_histogram]
        ax.bar(data.index, macd_histogram, color=colors, alpha=0.3, label='Histogram')
        
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax.set_title('MACD')
        ax.set_ylabel('MACD')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
    
    def save_plot(self, filename='stock_analysis.png'):
        """
        Save the current plot to file
        """
        if self.fig:
            self.fig.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Plot saved as {filename}")
    
    def show_plot(self):
        """
        Display the plot
        """
        if self.fig:
            plt.show()