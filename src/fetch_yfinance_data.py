import yfinance as yf
import pandas as pd

def fetch_crypto_data(symbol, start_date, end_date, interval='1h'):
    """
    Fetch cryptocurrency data using yfinance.

    :param symbol: Cryptocurrency symbol (e.g., 'BTC-USD' for Bitcoin/USD)
    :param start_date: Start date for historical data (YYYY-MM-DD)
    :param end_date: End date for historical data (YYYY-MM-DD)
    :param interval: Data interval ('1m', '5m', '1h', '1d', etc.)
    :return: DataFrame with cryptocurrency data
    """
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, end=end_date, interval=interval)
    return df

def read_symbols_from_file(file_path):
    """
    Read cryptocurrency symbols from a text file.

    :param file_path: Path to the text file containing the symbols
    :return: List of cryptocurrency symbols
    """
    with open(file_path, 'r') as file:
        symbols = [line.strip() + '-USD' for line in file if line.strip()]  # Append '-USD' to each symbol
    return symbols

if __name__ == "__main__":
    # Read the symbols from a text file
    symbol_file_path = 'C:/Users/Naushik/Downloads/csc582-asg1-master/Cryptocurrency-Volatility-Stabilizer/src/symbol.txt'  # Make sure to create this file with the symbols
    symbols = read_symbols_from_file(symbol_file_path)

    # Fetch cryptocurrency data for each symbol
    for symbol in symbols:
        df = fetch_crypto_data(symbol, start_date='2023-01-01', end_date='2024-12-01', interval='1h')
        df.to_csv(f'data/raw/{symbol}_data.csv')
        print(f"Data for {symbol} saved successfully!")