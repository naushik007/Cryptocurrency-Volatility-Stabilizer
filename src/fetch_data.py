import requests
import pandas as pd

API_KEY = 'FLC20O90UELOZGTS'

def fetch_crypto_data(symbol, market='USD', interval='1min'):
    url = f"https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol={symbol}&market={market}&interval={interval}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    time_series = data['Time Series (Digital Currency Intraday)']
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df = df.rename(columns={
        '1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'
    })
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df.astype(float)

if __name__ == "__main__":
    btc_data = fetch_crypto_data('BTC')
    btc_data.to_csv('data/raw/btc_data.csv', index=True)
