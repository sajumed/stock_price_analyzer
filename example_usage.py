"""
Example usage of the stock analysis tool
"""

from stock_data import StockDataFetcher
from stock_visualizer import StockVisualizer

def example_analysis():
    """
    Example of how to use the stock analysis classes
    """
    # Initialize classes
    fetcher = StockDataFetcher()
    visualizer = StockVisualizer()
    
    # Example stocks to analyze
    stocks = ['AAPL', 'TSLA', 'GOOGL']
    
    for symbol in stocks:
        print(f"\nAnalyzing {symbol}...")
        
        # Fetch data
        if fetcher.fetch_stock_data(symbol, period="6mo"):
            data = fetcher.get_data()
            
            # Get summary statistics
            stats = fetcher.get_summary_stats()
            if stats:
                print(f"Current RSI: {stats['rsi']:.2f}")
                print(f"Price vs SMA20: {((stats['current_price'] - stats['sma_20']) / stats['sma_20'] * 100):.2f}%")
            
            # Create and save visualization
            visualizer.create_dashboard(data, symbol)
            visualizer.save_plot(f"{symbol}_analysis.png")
            print(f"Analysis saved as {symbol}_analysis.png")

if __name__ == "__main__":
    example_analysis()