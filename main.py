from stock_data import StockDataFetcher
from stock_visualizer import StockVisualizer
import argparse

def main():
    parser = argparse.ArgumentParser(description='Stock Data Analysis Tool')
    parser.add_argument('symbol', type=str, help='Stock symbol (e.g., AAPL, TSLA, GOOGL)')
    parser.add_argument('--period', type=str, default='1y', 
                       help='Time period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max')
    parser.add_argument('--simple', action='store_true', 
                       help='Show simple chart only (no indicators)')
    parser.add_argument('--save', type=str, 
                       help='Save chart to filename (e.g., --save my_chart.png)')
    
    args = parser.parse_args()
    
    # Fetch and process data
    print(f"Fetching data for {args.symbol}...")
    fetcher = StockDataFetcher()
    
    if fetcher.fetch_data(args.symbol, args.period):
        print("Data fetched successfully!")
        
        # Calculate indicators
        print("Calculating technical indicators...")
        fetcher.calculate_sma(20)
        fetcher.calculate_ema(20)
        fetcher.calculate_rsi(14)
        fetcher.calculate_macd()
        
        data = fetcher.get_data()
        latest_price = fetcher.get_latest_price()
        
        print(f"\nLatest {args.symbol} Price: ${latest_price:.2f}")
        print(f"Data points: {len(data)}")
        print(f"Date range: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")
        
        # Visualize data
        visualizer = StockVisualizer()
        
        if args.simple:
            fig = visualizer.create_simple_chart(data, args.symbol)
        else:
            fig, axs = visualizer.create_price_chart(data, args.symbol)
        
        # Save or show chart
        if args.save:
            visualizer.save_chart(args.save)
        else:
            visualizer.show_chart()
            
    else:
        print("Failed to fetch data. Please check the stock symbol and try again.")

if __name__ == "__main__":
    main()