import pandas as pd

def add_features(data):
    data['ma_10'] = data['close'].rolling(window=10).mean()
    data['ma_50'] = data['close'].rolling(window=50).mean()
    data['rsi'] = 100 - (100 / (1 + data['close'].diff().clip(lower=0).rolling(14).mean() /
                                data['close'].diff().clip(upper=0).abs().rolling(14).mean()))
    return data.dropna()

if __name__ == "__main__":
    btc_data = pd.read_csv('data/raw/btc_data.csv', index_col=0, parse_dates=True)
    btc_data = add_features(btc_data)
    btc_data.to_csv('data/processed/btc_data_processed.csv')
