import pandas as pd
import os

def add_features(data):
    """
    Add technical indicators to the cryptocurrency data.

    :param data: DataFrame with raw cryptocurrency data
    :return: DataFrame with additional features
    """
    data['ma_10'] = data['Close'].rolling(window=10).mean()
    data['ma_50'] = data['Close'].rolling(window=50).mean()
    data['rsi'] = 100 - (100 / (1 + data['Close'].diff().clip(lower=0).rolling(14).mean() /
                                data['Close'].diff().clip(upper=0).abs().rolling(14).mean()))
    data['volatility'] = data['Close'].rolling(window=10).std()
    return data.dropna()

def preprocess_data(input_path, output_path):
    """
    Preprocess raw cryptocurrency data.

    :param input_path: Path to raw data CSV
    :param output_path: Path to save processed data CSV
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} not found.")
    
    raw_data = pd.read_csv(input_path, index_col=0, parse_dates=True)
    processed_data = add_features(raw_data)
    processed_data.to_csv(output_path)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    input_dir = 'data/raw/'
    output_dir = 'data/processed/'
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.csv'):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)
            preprocess_data(input_path, output_path)