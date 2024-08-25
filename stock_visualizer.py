import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
import seaborn as sns

class StockVisualizer:
    def __init__(self):
        style.use('seaborn-v0_8')
        self.fig = None
        self.axs = None
    
    def create_price_chart(self, data, symbol, show_indicators=True):
        """
        Create a comprehensive stock price chart with indicators
        """
        fig, axs = plt.subplots(3, 1, figsize=(15, 12))
        fig.suptitle(f'Stock Analysis: {symbol}', fontsize=16, fontweight='bold')
        
        # Price chart with moving averages
        axs[0].plot(data.index, data['Close'], label='Close Price', linewidth=2, color='black')
        axs[0].plot(data.index, data['SMA_20'], label='SMA 20', linewidth=1, color='blue', alpha=0.7)
        axs[0].plot(data.index, data['EMA_20'], label='EMA 20', linewidth=1, color='red', alpha=0.7)
        axs[0].set_title('Price with Moving Averages')
        axs[0].set_ylabel('Price ($)')
        axs[0].legend()
        axs[0].grid(True, alpha=0.3)
        
        # RSI
        axs[1].plot(data.index, data['RSI'], label='RSI', linewidth=2, color='purple')
        axs[1].axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought (70)')
        axs[1].axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold (30)')
        axs[1].set_title('Relative Strength Index (RSI)')
        axs[1].set_ylabel('RSI')
        axs[1].set_ylim(0, 100)
        axs[1].legend()
        axs[1].grid(True, alpha=0.3)
        
        # MACD
        axs[2].plot(data.index, data['MACD'], label='MACD', linewidth=2, color='blue')
        axs[2].plot(data.index, data['MACD_Signal'], label='Signal Line', linewidth=1, color='red')
        axs[2].bar(data.index, data['MACD_Histogram'], label='Histogram', alpha=0.3, color='gray')
        axs[2].set_title('MACD')
        axs[2].set_ylabel('MACD')
        axs[2].set_xlabel('Date')
        axs[2].legend()
        axs[2].grid(True, alpha=0.3)
        
        # Format x-axis
        for ax in axs:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
        
        plt.tight_layout()
        return fig, axs
    
    def create_simple_chart(self, data, symbol):
        """
        Create a simple price chart only
        """
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['Close'], linewidth=2, color='blue')
        plt.title(f'{symbol} Stock Price')
        plt.ylabel('Price ($)')
        plt.xlabel('Date')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt.gcf()
    
    def show_chart(self):
        """
        Display the chart
        """
        plt.show()
    
    def save_chart(self, filename='stock_analysis.png'):
        """
        Save the chart to file
        """
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Chart saved as {filename}")