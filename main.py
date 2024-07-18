import argparse
import sys
from stock_data import StockDataFetcher
from stock_visualizer import StockVisualizer

def main():
    """
    Main function to run the stock analysis tool
    """
    parser = argparse.ArgumentParser(description='Stock Data Analysis Tool')
    parser.add_argument('symbol', help='Stock symbol (e.g., AAPL, TSLA, GOOGL)')
    parser.add_argument('--period', default='1y', 
                       help='Time period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max')
    parser.add_argument('--save', action='store_true', 
                       help='Save plot to file')
    parser.add_argument('--filename', default='stock_analysis.png',
                       help='Filename for saved plot')
    
    args = parser.parse_args()
    
    print(f"Fetching data for {args.symbol}...")
    
    # Fetch stock data
    fetcher = StockDataFetcher()
    success = fetcher.fetch_stock_data(args.symbol, args.period)
    
    if not success:
        print("Failed to fetch stock data. Please check the symbol and try again.")
        sys.exit(1)
    
    data = fetcher.get_data()
    
    # Display summary statistics
    stats = fetcher.get_summary_stats()
    if stats:
        print("\n" + "="*50)
        print(f"SUMMARY STATISTICS FOR {args.symbol}")
        print("="*50)
        print(f"Current Price: ${stats['current_price']:.2f}")
        print(f"SMA 20: ${stats['sma_20']:.2f}")
        print(f"SMA 50: ${stats['sma_50']:.2f}")
        print(f"RSI: {stats['rsi']:.2f}")
        print(f"MACD: {stats['macd']:.4f}")
        print(f"Volume: {stats['volume']:,}")
        print("="*50)
    
    # Create visualization
    print("Creating visualization...")
    visualizer = StockVisualizer()
    visualizer.create_dashboard(data, args.symbol)
    
    if args.save:
        visualizer.save_plot(args.filename)
    
    visualizer.show_plot()

if __name__ == "__main__":
    main()