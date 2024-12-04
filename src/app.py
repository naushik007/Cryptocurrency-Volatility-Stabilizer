import os
from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from portfolio import portfolio_optimization

app = Flask(__name__)

@app.route('/')
def home():
    """
    Default route to indicate the API is running.
    """
    return jsonify({"message": "Cryptocurrency Volatility Stabilizer API is running. Use the /predict endpoint."})

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict future returns and optimize the portfolio based on the input data.

    :return: JSON response with predictions and optimized weights
    """
    try:
        # Parse the request JSON
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided."}), 400

        model_path = data.get('model_path')
        input_data = data.get('input_data')

        # Validate the input
        if not model_path or not os.path.exists(model_path):
            return jsonify({"error": "Model path is missing or invalid."}), 400
        if not input_data or not isinstance(input_data, list):
            return jsonify({"error": "Input data is missing or invalid."}), 400

        # Convert input_data to NumPy array
        input_data = np.array(input_data)

        # Load the model
        model = tf.keras.models.load_model(model_path)

        # Predict future returns
        predicted_returns = model.predict(input_data)

        # Optimize the portfolio
        weights = portfolio_optimization(predicted_returns)

        return jsonify({
            "predicted_returns": predicted_returns.tolist(),
            "weights": weights.tolist()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
