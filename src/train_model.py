import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os

def prepare_lstm_data(data, target_column='Close', lookback=60):
    """
    Prepare LSTM input and output data.

    :param data: DataFrame with features and target column
    :param target_column: Column to predict
    :param lookback: Number of time steps to look back
    :return: Tuple of (X, y, scaler)
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    X, y = [], []
    for i in range(lookback, len(scaled_data)):
        X.append(scaled_data[i-lookback:i])
        y.append(scaled_data[i, data.columns.get_loc(target_column)])
    return np.array(X), np.array(y), scaler

def build_lstm_model(input_shape):
    """
    Build and compile an LSTM model.

    :param input_shape: Shape of the input data
    :return: Compiled LSTM model
    """
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

if __name__ == "__main__":
    input_dir = 'data/processed/'
    model_dir = 'models/'
    os.makedirs(model_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.csv'):
            data = pd.read_csv(os.path.join(input_dir, file_name), index_col=0, parse_dates=True)
            X, y, scaler = prepare_lstm_data(data[['Close', 'ma_10', 'ma_50', 'rsi', 'volatility']])
            
            model = build_lstm_model(input_shape=(X.shape[1], X.shape[2]))
            model.fit(X, y, batch_size=32, epochs=10, validation_split=0.2)
            model.save(os.path.join(model_dir, f"{file_name.split('.')[0]}_lstm_model.h5"))
            print(f"Model for {file_name} saved.")
