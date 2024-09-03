from stock_data import StockDataFetcher
from stock_visualizer import StockVisualizer

def example_usage():
    """
    Example usage of the stock analysis tool
    """
    print("=== Stock Analysis Tool Example ===")
    
    # Initialize classes
    fetcher = StockDataFetcher()
    visualizer = StockVisualizer()
    
    # Example stocks to analyze
    stocks = ['AAPL', 'TSLA', 'GOOGL']
    
    for symbol in stocks:
        print(f"\nAnalyzing {symbol}...")
        
        # Fetch data
        if fetcher.fetch_data(symbol, period="6mo"):
            # Calculate indicators
            fetcher.calculate_sma(20)
            fetcher.calculate_ema(20)
            fetcher.calculate_rsi(14)
            fetcher.calculate_macd()
            
            data = fetcher.get_data()
            latest_price = fetcher.get_latest_price()
            
            print(f"Latest price: ${latest_price:.2f}")
            print(f"RSI: {data['RSI'].iloc[-1]:.2f}")
            
            # Create and save chart
            fig, axs = visualizer.create_price_chart(data, symbol)
            visualizer.save_chart(f"{symbol}_analysis.png")
            print(f"Chart saved as {symbol}_analysis.png")
        else:
            print(f"Failed to fetch data for {symbol}")

if __name__ == "__main__":
    example_usage()