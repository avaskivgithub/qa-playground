import yfinance as yf
import pandas as pd
import os

"""
    Fetch historical stock data for all symbols from the list.
    
    Parameters:
        symbol (str): Stock ticker symbol (e.g., 'VTI', 'AAPL').
        start (str): Start date in 'YYYY-MM-DD' format.
        end (str): End date in 'YYYY-MM-DD' format.
        interval (str): Data interval ('1d', '1wk', '1mo').
    
    ticker = yf.Ticker(symbol)
    data = ticker.history(start=start, end=end, interval=interval)
    
    Returns:
        pandas.DataFrame: Historical OHLCV data.
        
"""
if __name__ == "__main__":
    
    portfolio_list = ["NVDA", "VTI"]
    interval="1d"
    (start, end) = ("2025-01-01", "2025-12-01")

    result_file_name = f"portfolio_historical_{start}_{end}".replace('-','')

    for symbol in portfolio_list:
        sheet_name=f"{symbol}"

        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start, end=end, interval=interval)
        
        print(data.head())  # Show first 5 rows

        # Reset index so 'Date' becomes a column
        # And convert Date column to YYYY-MM-DD (remove timezone)
        data = data.reset_index()
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        data['Date'] = data['Date'].dt.strftime("%Y-%m-%d")

        # Save to Excel
        filename = f"{result_file_name}.xlsx"
        mode = "w" if not os.path.exists(filename) else "a"
        with pd.ExcelWriter(filename, engine="openpyxl", mode=mode) as writer:
            data.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Data saved to {filename}")