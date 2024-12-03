import requests
import pandas as pd

API_KEY = 'FLC20O90UELOZGTS'

def fetch_crypto_data(symbol, market='USD', interval='1min', outputsize='compact'):
    """
    Fetch cryptocurrency data from Alpha Vantage.

    :param symbol: Cryptocurrency symbol (e.g., 'BTC' for Bitcoin)
    :param market: Market pair (e.g., 'USD')
    :param interval: Data interval ('1min', '5min', '15min', '30min', '60min')
    :param outputsize: 'compact' (last 100 points) or 'full' (entire dataset)
    :return: DataFrame with cryptocurrency data
    """
    url = (f"https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol={symbol}"
           f"&market={market}&interval={interval}&apikey={API_KEY}&outputsize={outputsize}")
    response = requests.get(url)
    data = response.json()

    if "Time Series (Digital Currency Intraday)" in data:
        time_series = data["Time Series (Digital Currency Intraday)"]
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df = df.rename(columns={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. volume': 'volume'
        })
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()  # Sort by date
        return df.astype(float)
    else:
        raise ValueError(f"Error fetching data: {data.get('Error Message', 'Unknown error')}")

if __name__ == "__main__":
    # Example: Fetch BTC/USD data
    symbol = 'BTC'
    market = 'USD'
    df = fetch_crypto_data(symbol, market, interval='5min', outputsize='compact')
    df.to_csv(f'data/raw/{symbol}_data.csv')
    print(f"Data for {symbol}/{market} saved successfully!")
