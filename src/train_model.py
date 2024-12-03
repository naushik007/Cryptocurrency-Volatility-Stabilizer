import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def prepare_lstm_data(data, target_column='close', lookback=60):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    X, y = [], []
    for i in range(lookback, len(scaled_data)):
        X.append(scaled_data[i-lookback:i])
        y.append(scaled_data[i, data.columns.get_loc(target_column)])
    return np.array(X), np.array(y), scaler

if __name__ == "__main__":
    data = pd.read_csv('data/processed/btc_data_processed.csv', index_col=0, parse_dates=True)
    X, y, scaler = prepare_lstm_data(data[['close', 'ma_10', 'ma_50', 'rsi']])

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, batch_size=32, epochs=10, validation_split=0.2)
    model.save('models/lstm_model.h5')
