from setup_portfolio import *
import yfinance as yf
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
#from sklearn.tree import DecisionTreeRegressor
from datetime import datetime, timedelta

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
def read_yfinanace_or_cached_csv(symbol, start, end, interval='1d'):

    result_file_name = f"portfolio_historical_{start}_{end}".replace('-','')
    cvs_file_name = f"{result_file_name}_{symbol}.csv"
    os.makedirs("data", exist_ok=True)
    cvs_file_path = os.path.join("data", cvs_file_name)

    if os.path.exists(cvs_file_path):
        print("Reading from CVS")
        data = pd.read_csv(cvs_file_path)
    else:
        print("Reading from API")
        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start, end=end, interval=interval)

        # Save to cvs with Date column
        data = data.reset_index().rename(columns={"index": "Date"})
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        data['Date'] = data['Date'].dt.strftime("%Y-%m-%d")

        data.to_csv(cvs_file_path, index=False)
        
    print(data.head())  # Show first 5 rows
    return data

def save_stock_data_to_excel(filename_excel, symbol, data):

    mode = "w" if not os.path.exists(filename_excel) else "a"
    with pd.ExcelWriter(filename_excel, engine="openpyxl", mode=mode) as writer:
        data.to_excel(writer, sheet_name=symbol, index=False)


if __name__ == "__main__":
    
    if os.path.exists(filename_excel):
        os.remove(filename_excel)

    # Read data api / cvs cache and store to xlsx
    for symbol in portfolio_list:

        data = read_yfinanace_or_cached_csv(symbol, start, end, interval)
        save_stock_data_to_excel(filename_excel, symbol, data)

        # "future" data to check predictions
        read_yfinanace_or_cached_csv(symbol, start_future, end_future, interval)

    print(f"Data saved to {filename_excel}")